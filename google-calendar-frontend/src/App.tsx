import { useEffect, useState } from 'react'
import './App.css'
import calendarService from './services/calendars'
import eventService from './services/Events'
import Calendar from './types/Calendar'
import Event from './types/Event'

function App() {
  const [calendars, setCalendars] = useState<Calendar[]>([])
  const [events, setEvents] = useState<Event[]>([])

  // Fetch google calendar events and set them to state
  useEffect(() => {
    calendarService.getAll().then((calendars: Calendar[]) => setCalendars(calendars))
  }, [])

  const fetchEvents = (calendarId: string) => {
    const currentYear = new Date().getFullYear()
    eventService.getAll(currentYear, calendarId).then((events: Event[]) => {
      const updatedEvents = events.map((event) => {
        event.isFuture = new Date(event.start.dateTime) > new Date() // Check if the event is in the future
        return event
      })
      setEvents(updatedEvents)
    })
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Calendars</h1>
        <ul className="calendar-list">
          {calendars.map((calendar) => (
            <li key={calendar.id} onClick={() => fetchEvents(calendar.id)}>
              <a href="#">{calendar.summary}</a>
            </li>
          ))}
        </ul>
        <div>
          <h2>Events</h2>
        </div>
        <table className="event-table">
          <thead>
            <tr>
              <th>Summary</th>
              <th>Start</th>
              <th>End</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id}>
                <td>
                  <a href={event.htmlLink} target='_blank'>{event.summary}</a>
                  <span>{event.isFuture ? ' (Future event)' : ''}</span>
                </td>
                <td>{event.formatted_start}</td>
                <td>{event.formatted_end}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </header>
    </div>
  )
}

export default App
