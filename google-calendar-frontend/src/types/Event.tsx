interface Event {
  id: string
  summary: string
  start: EventTime
  end: EventTime
  duration: number // Duration in hours
  formatted_start: string
  formatted_end: string
  htmlLink: string
  isFuture: boolean | false // Whether the event is in the future
}

interface EventTime {
  dateTime: string
  timeZone: string
}

export default Event