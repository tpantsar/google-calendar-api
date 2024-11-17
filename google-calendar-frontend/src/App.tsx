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

type IEventsProps = {
  calendarId: string,
  events: Event[],
  filter: string,
  setFilter: React.Dispatch<React.SetStateAction<string>>,
  setEvents: React.Dispatch<React.SetStateAction<Event[]>>
}

const Events = ({ calendarId, events, filter, setFilter, setEvents }: IEventsProps) => {
  const [sort, setSort] = useState<boolean>(false)
  const [showFutureEvents, setShowFutureEvents] = useState<boolean>(false)
  
  console.log('Calendar ID:', calendarId)
  const toggleFutureEvents = () => setShowFutureEvents(!showFutureEvents)
  
  // Filter events based on the filter and showFutureEvents state
  const filteredEvents = events.filter((event) => 
    event.summary.toLowerCase().includes(filter.toLowerCase()) && 
    (showFutureEvents || !event.isFuture)
  )

  // Sort events by start date
  if (sort) {
    filteredEvents.sort((a, b) => new Date(a.start.dateTime).getTime() - new Date(b.start.dateTime).getTime())
  }

  const deleteEvent = (event: Event) => {
    const result = window.confirm(`Delete event: ${event.summary}?`)
    if (result) {
      eventService.remove(calendarId, event.id).then(() => {
        console.log('Event deleted:', event.id)
        const updatedEvents = events.filter((eventItem) => eventItem.id !== event.id)
        setEvents(updatedEvents)
      })
      .catch((error) => console.error('Error deleting event:', error))
    }
  }

  const handleSummaryClick = (summary: string) => {
    setFilter(summary);
  };

  return (
    <>
      <div className="flex-container">
        <h2>Events: {filteredEvents.length}</h2>
        <h2>Types: {new Set(filteredEvents.map(event => event.summary)).size}</h2>
        <h2>Hours: {filteredEvents.reduce((acc, event) => acc + event.duration, 0).toFixed(2)}</h2>
      </div>
      <div className="flex-container">
        <h3>Future events: {events.filter(event => event.isFuture).length}</h3>
        <button onClick={toggleFutureEvents}>
          {showFutureEvents ? 'Hide' : 'Show'}
        </button>
      </div>
      <table className="event-table">
        <thead>
          <tr>
            <th>Summary</th>
            <th>
              Start
              <button onClick={() => setSort(!sort)}>Sort</button>
            </th>
            <th>End</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          {filteredEvents.map((event) => (
            <tr key={event.id}>
              <td>
                <i onClick={() => deleteEvent(event)} className="icon-trashcan fa-solid fa-trash-can"></i>
                <a href={event.htmlLink} target='_blank'>
                  <i className="icon-arrow fa-solid fa-arrow-up-right-from-square"></i>
                </a>
                <span onClick={() => handleSummaryClick(event.summary)} style={{ cursor: 'pointer', color: 'blue' }}>
                  {event.summary}
                </span>
                <span>{event.isFuture ? ' (Future event)' : ''}</span>
              </td>
              <td>{event.formatted_start}</td>
              <td>{event.formatted_end}</td>
              <td>{event.duration}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

function App() {
  const [calendars, setCalendars] = useState<Calendar[]>([])
  const [calendarId, setCalendarId] = useState<string>('')
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
      setCalendarId(calendarId)
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
        <Events calendarId={calendarId} events={events} filter={eventsFilter} setFilter={setEventsFilter} setEvents={setEvents} />
      </header>
    </div>
  )
}

export default App
