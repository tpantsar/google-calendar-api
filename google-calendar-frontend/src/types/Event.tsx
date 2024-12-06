interface Event {
  // Required API properties from Google Calendar
  id: string
  summary: string
  description: string
  start: EventTime
  end: EventTime
  htmlLink: string

  // Computed properties on backend
  formatted_start: string
  formatted_end: string
  duration: number // Duration in hours

  // Computed properties on frontend
  isFuture: boolean | false // Whether the event is in the future
  count: number | 0 // Number of events with the same summary
  hours: number | 0 // Number of hours spent on all events of this type
}

interface EventTime {
  dateTime: string
  timeZone: string
}

export default Event
