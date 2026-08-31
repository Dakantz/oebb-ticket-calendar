import base64
import re
from datetime import date
from email import message_from_bytes
from email.policy import default as email_policy

import httpx

from . import config

GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"
SEARCH_QUERY = 'subject:"ÖBB Buchung"'

MONTHS = {
    "Jan": 1, "Feb": 2, "Mär": 3, "Apr": 4, "Mai": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Okt": 10, "Nov": 11, "Dez": 12,
}

LEG_RE = re.compile(
    r"^(?P<from>.+?) > (?P<to>.+?)\n"
    r".*Fahrt(en)? für (?P<person>.+?)\n"
    r"gilt: (?P<d1>\d{1,2})\. (?P<m1>\w+) ?-? ?(?P<d2>\d{1,2})?\.? ?(?P<m2>\w+)? (?P<year>\d{4})\n"
    r"Meine Buchung: (?P<link>\S+)",
    re.MULTILINE,
)
BOOKING_CODE_RE = re.compile(r"Buchungscode:\s*(.+)")


def refresh_access_token(refresh_token: str) -> str:
    resp = httpx.post(
        config.GOOGLE_TOKEN_URI,
        data={
            "client_id": config.GOOGLE_CLIENT_ID,
            "client_secret": config.GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def _fetch_message_text(client: httpx.Client, message_id: str) -> str:
    resp = client.get(f"{GMAIL_API}/messages/{message_id}", params={"format": "raw"})
    resp.raise_for_status()
    raw = base64.urlsafe_b64decode(resp.json()["raw"])
    msg = message_from_bytes(raw, policy=email_policy)
    body = msg.get_body(preferencelist=("plain", "html"))
    if body is None:
        return ""
    return body.get_content()


def _parse_legs(text: str) -> list[dict]:
    legs = []
    for m in LEG_RE.finditer(text):
        year = int(m["year"])
        month1 = MONTHS.get(m["m1"])
        month2 = MONTHS.get(m["m2"]) if m["m2"] else month1
        day2 = int(m["d2"]) if m["d2"] else int(m["d1"])
        if month1 is None or month2 is None:
            continue
        start = date(year, month1, int(m["d1"]))
        end = date(year, month2, day2)
        legs.append(
            {
                "from": m["from"].strip(),
                "to": m["to"].strip(),
                "person": m["person"].strip(),
                "start": start,
                "end": end,
                "link": m["link"].strip(),
            }
        )
    return legs


def fetch_bookings(refresh_token: str) -> list[dict]:
    """Returns a flat list of legs: {message_id, from, to, person, start, end, link, booking_code}."""
    access_token = refresh_access_token(refresh_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    bookings = []
    with httpx.Client(headers=headers, timeout=30) as client:
        resp = client.get(f"{GMAIL_API}/messages", params={"q": SEARCH_QUERY})
        resp.raise_for_status()
        message_ids = [m["id"] for m in resp.json().get("messages", [])]

        for message_id in message_ids:
            text = _fetch_message_text(client, message_id)
            code_match = BOOKING_CODE_RE.search(text)
            booking_code = code_match.group(1).strip() if code_match else message_id
            for leg in _parse_legs(text):
                leg["message_id"] = message_id
                leg["booking_code"] = booking_code
                bookings.append(leg)
    return bookings
