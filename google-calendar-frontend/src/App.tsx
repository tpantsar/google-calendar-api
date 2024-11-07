import { useEffect, useState } from 'react'
import './App.css'
import calendarService from './services/calendars'
import Calendar from './types/Calendar'

function App() {
  const [calendars, setCalendars] = useState<Calendar[]>([])

  // Fetch google calendar events and set them to state
  useEffect(() => {
    calendarService.getAll().then((calendars: Calendar[]) => setCalendars(calendars))
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>Calendars</h1>
        <ul>
          {calendars.map((calendar) => (
            <li key={calendar.id}>{calendar.summary}</li>
          ))}
        </ul>
      </header>
    </div>
  )
}

export default App
