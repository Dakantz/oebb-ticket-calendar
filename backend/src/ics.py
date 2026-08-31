from datetime import date, timedelta


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def build_ics(legs: list[dict]) -> str:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//oebb-ticket-calendar//DE", "CALSCALE:GREGORIAN"]
    for leg in legs:
        dtend = leg["end"] + timedelta(days=1)  # ICS all-day DTEND is exclusive
        lines += [
            "BEGIN:VEVENT",
            f"UID:{leg['message_id']}-{leg['from']}-{leg['to']}-{leg['start']}@oebb-ticket-calendar",
            f"DTSTART;VALUE=DATE:{leg['start'].strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{dtend.strftime('%Y%m%d')}",
            f"SUMMARY:{_escape('ÖBB: ' + leg['from'] + ' -> ' + leg['to'])}",
            f"DESCRIPTION:{_escape('Buchungscode: ' + leg['booking_code'] + chr(10) + 'Fahrgast: ' + leg['person'] + chr(10) + leg['link'])}",
            f"URL:{leg['link']}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"
