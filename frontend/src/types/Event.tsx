import EventTime from './EventTime'

interface Event {
  // Required API properties for request body
  start: EventTime
  end: EventTime

  // Optional API properties for request body
  id: string
  summary: string
  description: string
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

export default Event
