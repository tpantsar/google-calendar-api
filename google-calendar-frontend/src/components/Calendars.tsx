import { useState } from 'react'
import '../styles/Calendars.css'
import Calendar from '../types/Calendar'

type ICalendarsProps = {
  calendars: Calendar[]
  fetchEvents: (calendarId: string) => void
}

const Calendars = ({ calendars, fetchEvents }: ICalendarsProps) => {
  const [selectedCalendarId, setSelectedCalendarId] = useState<string>('')

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const calendarId = event.target.value
    setSelectedCalendarId(calendarId)
    fetchEvents(calendarId)
  }

  const handleRefresh = () => {
    if (selectedCalendarId) {
      console.log('Refreshing events for calendar:', selectedCalendarId)
      fetchEvents(selectedCalendarId)
    }
  }

  return (
    <div className="flex-container">
      <select className="calendar-dropdown" onChange={handleChange}>
        <option value="">- Select a calendar -</option>
        {calendars.map((calendar) => (
          <option key={calendar.id} value={calendar.id}>
            {calendar.summary}
          </option>
        ))}
      </select>
      <button onClick={handleRefresh}>Refresh</button>
    </div>
  )
}

Calendars.displayName = 'Calendars'
export default Calendars
