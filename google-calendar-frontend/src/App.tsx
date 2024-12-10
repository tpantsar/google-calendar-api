import { useEffect, useState } from 'react'
import './App.css'
/* Components */
import Calendars from './components/Calendars'
import Events from './components/Events'
import Filter from './components/Filter'
import EventForm from './components/EventForm'
/* Services */
import calendarService from './services/calendars'
import eventService from './services/events'
/* Types */
import Calendar from './types/Calendar'
import Event from './types/Event'

function App() {
  const [calendars, setCalendars] = useState<Calendar[]>([])
  const [selectedCalendarId, setSelectedCalendarId] = useState<string>('')
  const [events, setEvents] = useState<Event[]>([])
  const [eventsFilter, setEventsFilter] = useState<string>('')

  // Fetch google calendar events and set them to state
  useEffect(() => {
    calendarService
      .getAll()
      .then((calendars: Calendar[]) => setCalendars(calendars))
  }, [])

  const getCalendarEvents = (calendarId: string) => {
    eventService.getAll(calendarId).then((events: Event[]) => {
      const updatedEvents = events.map((event) => {
        event.isFuture = new Date(event.start.dateTime) > new Date() // Check if the event is in the future
        return event
      })
      localStorage.setItem('events', JSON.stringify(updatedEvents))
      setEvents(updatedEvents)
      setSelectedCalendarId(calendarId)
    })
  }

  return (
    <div className="App">
      <header className="App-header">
        <EventForm
          selectedCalendarId={selectedCalendarId}
          setEvents={setEvents}
        />
        <Calendars
          calendars={calendars}
          selectedCalendarId={selectedCalendarId}
          setSelectedCalendarId={setSelectedCalendarId}
          getCalendarEvents={getCalendarEvents}
        />
        <Filter filter={eventsFilter} setFilter={setEventsFilter} />
        <Events
          calendarId={selectedCalendarId}
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
