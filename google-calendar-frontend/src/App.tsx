import { useEffect, useState } from 'react'
import './App.css'
/* Components */
import Calendars from './components/Calendars'
import Events from './components/Events'
import EventTypesList from './components/EventTypesList'
import Filter from './components/Filter'
/* Services */
import calendarService from './services/Calendars'
import eventService from './services/Events'
/* Types */
import Calendar from './types/Calendar'
import Event from './types/Event'

function App() {
  const [calendars, setCalendars] = useState<Calendar[]>([])
  const [calendarId, setCalendarId] = useState<string>('')
  const [events, setEvents] = useState<Event[]>([])
  const [eventsFilter, setEventsFilter] = useState<string>('')

  // Fetch google calendar events and set them to state
  useEffect(() => {
    calendarService
      .getAll()
      .then((calendars: Calendar[]) => setCalendars(calendars))
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
        <Calendars calendars={calendars} fetchEvents={fetchEvents} />
        <EventTypesList events={events} setFilter={setEventsFilter} />
        <Filter filter={eventsFilter} setFilter={setEventsFilter} />
        <Events
          calendarId={calendarId}
          events={events}
          filter={eventsFilter}
          setFilter={setEventsFilter}
          setEvents={setEvents}
        />
      </header>
    </div>
  )
}

export default App
