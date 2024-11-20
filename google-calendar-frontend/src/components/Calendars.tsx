import '../styles/Calendars.css'
import Calendar from '../types/Calendar'

type ICalendarsProps = {
  calendars: Calendar[]
  fetchEvents: (calendarId: string) => void
}

const Calendars = ({ calendars, fetchEvents }: ICalendarsProps) => {
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    fetchEvents(event.target.value)
  }

  return (
    <select className="calendar-dropdown" onChange={handleChange}>
      <option value="">- Select a calendar -</option>
      {calendars.map((calendar) => (
        <option key={calendar.id} value={calendar.id}>
          {calendar.summary}
        </option>
      ))}
    </select>
  )
}

Calendars.displayName = 'Calendars'
export default Calendars
