export interface Infocards {
  infocards: Infocard[]
}

export interface Infocard {
  acquisitionInfo: AcquisitionInfo
  atLeastOneTicketIsRetrieved: boolean
  datetimeArrival?: string
  datetimeDeparture?: string
  datetimeValidFrom: string
  deviceId?: string
  datetimeValidTo: string
  from?: From
  id: string
  passengers: Passenger[]
  state: string
  to?: To
  type: string
  validTo: string
  bookingCode: string
  insured: boolean
  orderItemType: string
  productDescriptions: ProductDescription[]
  sortDate: string
  relevantReductions: any[]
  connection?: Connection
  validityInfo: ValidityInfo
  entrypoint?: Entrypoint
}

export interface AcquisitionInfo {
  type: string
}

export interface From {
  name: string
  number: number
}

export interface Passenger {
  id: number
  technicalId: string
  type: string
  colorId: string
  birthDate: string
  firstName: string
  lastName: string
  me: boolean
  remembered: boolean
  relations: any[]
  position: number
  _order_index: number
  nameChangeable: boolean
  passengerDeletable: boolean
  cards: Card[]
  challengedFlags: ChallengedFlags
}

export interface Card {
  image: string
  cardId: number
  isChallenged: boolean
  isFamily: boolean
  isDiscountCard: boolean
  isMergeableIntoCustomerAccount: boolean
  isSelectable: boolean
  motorailTrainRelevance: string
  name: string
  numberRequired: boolean
  cardNumber: string
}

export interface ChallengedFlags {
  hasHandicappedPass: boolean
  hasAssistanceDog: boolean
  hasWheelchair: boolean
  hasAttendant: boolean
}

export interface To {
  name: string
  number: number
}

export interface ProductDescription {
  instanceId?: string
  productType: string
  name: Name
}

export interface Name {
  de: string
  en?: string
  it?: string
}

export interface Connection {
  from: From2
  to: To2
  sections: Section[]
  switches: number
  duration: number
  pastConnection: boolean
}

export interface From2 {
  name: string
  esn: number
  departure: string
}

export interface To2 {
  name: string
  esn: number
  arrival: string
}

export interface Section {
  from: From3
  to: To3
  duration: number
  category: Category
  type: string
  hasRealtime: boolean
}

export interface From3 {
  name: string
  esn: number
  departure: string
}

export interface To3 {
  name: string
  esn: number
  arrival: string
}

export interface Category {
  name: string
  number: string
  shortName: string
  displayName: string
  longName: LongName
  backgroundColor: string
  fontColor: string
  barColor: string
  place: Place
  journeyPreviewIconId: string
  journeyPreviewIconColor: string
  assistantIconId: string
  train: boolean
  parallelLongName: any
  parallelDisplayName: string
  backgroundColorDisabled: string
  fontColorDisabled: string
  barColorDisabled: string
}

export interface LongName {
  de: string
  en: string
  it: string
}

export interface Place {
  de: string
  en: string
  it: string
}

export interface ValidityInfo {
  category: Category2
  trafficType: string
  durationLabel: DurationLabel
  duration: Duration
}

export interface Category2 {
  de: string
  en: string
  it: string
}

export interface DurationLabel {
  de: string
  en: string
  it: string
}

export interface Duration {
  de: string
  en: string
  it: string
}

export interface Entrypoint {
  title: Title
}

export interface Title {
  de: string
  en: string
  it: string
}
