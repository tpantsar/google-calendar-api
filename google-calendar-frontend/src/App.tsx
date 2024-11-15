import { useEffect, useState } from 'react'
import './App.css'
import calendarService from './services/Calendars'
import eventService from './services/Events'
import Calendar from './types/Calendar'
import Event from './types/Event'

const Filter = ({ filter, setFilter }: { filter: string, setFilter: React.Dispatch<React.SetStateAction<string>> }) => {
  return (
    <div>
      Filter events: <input value={filter} onChange={(e) => setFilter(e.target.value)} />
    </div>
  )
}

const Events = ({ events, filter }: { events: Event[], filter: string }) => {
  const filteredEvents = events.filter((event) => event.summary.toLowerCase().includes(filter.toLowerCase()))
  const [sort, setSort] = useState<boolean>(false)

  // Sort events by start date
  if (sort) {
    filteredEvents.sort((a, b) => new Date(a.start.dateTime).getTime() - new Date(b.start.dateTime).getTime())
  }

  return (
    <>
      <h2>Events: {filteredEvents.length}</h2>
      <h2>Hours: {filteredEvents.reduce((acc, event) => acc + event.duration, 0)}</h2>
      <table className="event-table">
        <thead>
          <tr>
            <th>Summary</th>
            <th>
              Start
              <button onClick={() => setSort(!sort)}>Sort</button>
            </th>
            <th>End</th>
          </tr>
        </thead>
        <tbody>
          {filteredEvents.map((event) => (
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
    </>
  )
}

function App() {
  const [calendars, setCalendars] = useState<Calendar[]>([])
  const [events, setEvents] = useState<Event[]>([])
  const [eventsFilter, setEventsFilter] = useState<string>('')

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
        <Filter filter={eventsFilter} setFilter={setEventsFilter} />
        <Events events={events} filter={eventsFilter} />
      </header>
    </div>
  )
}

export default App
