import { Entity, PrimaryGeneratedColumn, Column, BaseEntity } from "typeorm"
import type { Infocard } from "./ticket_model"

@Entity()
export class Ticket extends BaseEntity {
    @PrimaryGeneratedColumn()
    id: number

    @Column()
    identifier: string


    @Column()
    departureTime: Date

    @Column()
    arrivalTime: Date

    @Column()
    from: string
    @Column()
    to: string

    @Column("simple-json")
    info: Infocard
}

export function fromTicketData(data: Infocard): Ticket {
    const ticket = new Ticket()
    ticket.identifier = data.id || "unknown"
    ticket.departureTime = new Date(data.datetimeDeparture || "")
    ticket.arrivalTime = new Date(data.datetimeArrival || "")
    ticket.from = data.connection?.from?.name || "unknown"
    ticket.to = data.connection?.to?.name || "unknown"
    ticket.info = data
    return ticket
}