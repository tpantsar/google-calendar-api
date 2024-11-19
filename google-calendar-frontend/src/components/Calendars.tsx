import '../styles/Calendars.css'
import Calendar from '../types/Calendar'

type ICalendarsProps = {
  calendars: Calendar[]
  fetchEvents: (calendarId: string) => void
}

const Calendars = ({ calendars, fetchEvents }: ICalendarsProps) => {
  return (
    <>
      <h1>Calendars</h1>
      <ul className="calendar-list">
        {calendars.map((calendar) => (
          <li key={calendar.id} onClick={() => fetchEvents(calendar.id)}>
            <a href="#">{calendar.summary}</a>
          </li>
        ))}
      </ul>
    </>
  )
}

Calendars.displayName = 'Calendars'
export default Calendars
