import { useEffect } from 'react'
import '../styles/Calendars.css'
import Calendar from '../types/Calendar'

type CalendarsProps = {
  calendars: Calendar[]
  selectedCalendarId: string
  setSelectedCalendarId: (calendarId: string) => void
  getCalendarEvents: (calendarId: string) => void
}

const Calendars = ({
  calendars,
  selectedCalendarId,
  setSelectedCalendarId,
  getCalendarEvents,
}: CalendarsProps) => {
  // Set selected calendar id from local storage if available
  useEffect(() => {
    const selectedCalendarId = localStorage.getItem('selectedCalendarId')
    if (selectedCalendarId) {
      setSelectedCalendarId(selectedCalendarId)
    }
  }, [setSelectedCalendarId])

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const calendarId = event.target.value
    setSelectedCalendarId(calendarId)
    getCalendarEvents(calendarId)
    localStorage.setItem('selectedCalendarId', calendarId)
  }

  const refreshCalendarEvents = () => {
    if (selectedCalendarId) {
      console.log('Refreshing events for calendar:', selectedCalendarId)
      getCalendarEvents(selectedCalendarId)
    }
  }

  return (
    <div className="flex-container">
      <select
        className="calendar-dropdown"
        value={selectedCalendarId}
        onChange={handleChange}
      >
        <option value="">- Select a calendar -</option>
        {calendars.map((calendar) => (
          <option key={calendar.id} value={calendar.id}>
            {calendar.summary}
          </option>
        ))}
      </select>
      <button onClick={refreshCalendarEvents}>Refresh</button>
    </div>
  )
}

Calendars.displayName = 'Calendars'
export default Calendars
