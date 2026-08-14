import type { Browser } from 'puppeteer';
import puppeteer from 'puppeteer-extra';

import { DataSource, Repository } from "typeorm"
import type { Infocards } from './models/ticket_model';
import { fromTicketData, Ticket } from './models/db_model';

import StealthPlugin from 'puppeteer-extra-plugin-stealth'

const TicketsSourceDB = new DataSource({
    type: "sqlite",
    database: "tickets.sqlite",
    entities: [Ticket],
})

try {
    await TicketsSourceDB.initialize()
    console.log("Data Source has been initialized!")
} catch (error) {
    console.error("Error during Data Source initialization", error)
}
await TicketsSourceDB.synchronize()
const ticketRepository = TicketsSourceDB.getRepository(Ticket)

const asyncTimeout = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const email = ""
const password = ""

const screenshotPath = process.env.SCREENSHOT_PATH || "/screenshots"
async function scrapeTickets(page: puppeteer.Page) {

    await page.setViewport({ 'width': 1280, 'height': 800 })

    page.on("response", (resp) => {
        // console.log("Response:", resp.url());
        if (resp.url().endsWith("/infocards/by-ids/tickets")) {
            resp.text().then(text => {
                // console.log("Response text:", text);
            });
            (async () => {
                let data = await resp.json()
                // console.log("Response data:", data);
                let ticket_data = data as Infocards
                for (let ticket_info of ticket_data.infocards) {
                    let ticket = fromTicketData(ticket_info)
                    console.log("Parsed ticket:", ticket)
                    let existing_ticket = await repo.findOneBy({ identifier: ticket.identifier })
                    if (existing_ticket) {
                        console.log(`Ticket with identifier ${ticket.identifier} already exists in DB, skipping.`)
                    } else {
                        await repo.save(ticket)
                        console.log(`Saved ticket with identifier ${ticket.identifier} to DB.`)
                    }
                }


            })().catch(err => console.error(err));
        }
    })

    await page.goto("https://shop.oebbtickets.at/de/ticket")
    await page.screenshot({ 'path': `${screenshotPath}/oebb_preloading.png` })
    await page.waitForSelector(".account-button")
    await page.screenshot({ path: `${screenshotPath}/oebb.png`, fullPage: true })
    await page.click(".account-button")
    await asyncTimeout(2000)
    await page.type('#username', email)
    await page.type('#password', password)
    await asyncTimeout(5000)
    await page.screenshot({ 'path': `${screenshotPath}/oebb_logging_in.png` })
    await page.click('#kc-login')
    await page.screenshot({ 'path': `${screenshotPath}/oebb_logged_in.png`, fullPage: true })
    await asyncTimeout(1000)
    await page.waitForSelector(".tickets-button")
    console.log("Logged in successfully.")
    await asyncTimeout(1000)
    await page.click(".tickets-button")
    await asyncTimeout(2000)
    console.log("Navigated to tickets page.")
    while (true) {
        try {
            await page.waitForSelector(".more-button", { timeout: 5000 })
            await page.click(".more-button")
            console.log("Clicked load more button.")
            await asyncTimeout(2000)
        } catch (e) {
            console.log("No more load more button, exiting loop.")
            break
        }
    }

    await page.waitForSelector(".tab-label-archived-tickets")
    await page.click(".tab-label-archived-tickets")
    await asyncTimeout(1000)

    while (true) {
        try {
            await page.waitForSelector(".more-button", { timeout: 5000 })
            await page.click(".more-button")
            console.log("Clicked load more button.")
            await asyncTimeout(2000)
        } catch (e) {
            console.log("No more load more button, exiting loop.")
            break
        }
    }

    await page.screenshot({ 'path': `${screenshotPath}/oebb_archived_tickets.png`, fullPage: true })


    await browser.close()
    console.log(`All done, check the screenshot. ✨`)
}
export async function fetchTicketsIntoDB(repo: Repository<Ticket>, email: string, password: string) {

    // add stealth plugin and use defaults (all evasion techniques)
    puppeteer.use(StealthPlugin())

    // puppeteer usage as normal
    let browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox']
    });
    console.log('Running extraction..')
    const page = await browser.newPage()
    try {
        await scrapeTickets(page)
    }catch (err) {
        console.error("Error during scraping:", err)
        await page.screenshot({ 'path': `${screenshotPath}/oebb_error.png`, fullPage: true })
    } finally {
        await browser.close()
    }
}
