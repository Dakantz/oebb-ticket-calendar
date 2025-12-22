import { DataSource, Repository } from "typeorm"
import type { Infocards } from './models/ticket_model';
import { fromTicketData, Ticket } from './models/db_model';

import StealthPlugin from 'puppeteer-extra-plugin-stealth'
import ical, { ICalCalendarMethod } from 'ical-generator';

import { fetchTicketsIntoDB } from "./scraper";

import express from "express";




const TicketsSourceDB = new DataSource({
    type: "sqlite",
    database: process.env.DB_FILE || "tickets.sqlite",
    entities: [Ticket],
})

try {
    await TicketsSourceDB.initialize()
    console.log("Data Source has been initialized!")
} catch (error) {
    console.error("Error during Data Source initialization", error)
}
// await TicketsSourceDB.synchronize()
const ticketRepository = TicketsSourceDB.getRepository(Ticket)


const email = process.env.OEBB_EMAIL || ""
const password = process.env.OEBB_PASSWORD || ""


const app = express()
const port = process.env.PORT || 3000

app.get("/", (req, res) => {
    res.send("OEBB Ticket Scraper is running.")
})


app.get("/calendar", (req, res) => {

    res.writeHead(200, {
        'Content-Type': 'text/calendar; charset=utf-8',
        'Content-Disposition': 'attachment; filename="calendar.ics"',
    });

    const calendar = ical({ name: `${email}'s Calendar for OEBB` });
    calendar.method(ICalCalendarMethod.REQUEST);
    Ticket.find().then(tickets => {
        tickets.forEach(ticket => {
            calendar.createEvent({
                start: ticket.departureTime,
                end: ticket.arrivalTime,
                summary: `${ticket.from} nach ${ticket.to}`,
                location: `${ticket.from}`,
                id: ticket.identifier,
            });
            res.end(calendar.toString());
        });
    })


})

await fetchTicketsIntoDB(ticketRepository, email, password)
setInterval(async () => {
    await fetchTicketsIntoDB(ticketRepository, email, password)
}, 15 * 60 * 1000) // every 15 minutes

console.log("Scraper service is running, fetching tickets every 15 minutes.")


app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`)
})