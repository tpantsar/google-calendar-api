import Event from '../types/Event'

type ICalendarsProps = {
  events: Event[]
  setFilter: React.Dispatch<React.SetStateAction<string>>
}

const EventTypes = ({ events, setFilter }: ICalendarsProps) => {
  // Find unique events on the calendar based on the event summary
  const uniqueEvents = events.reduce((acc: Event[], event: Event) => {
    const existingEvent = acc.find((e) => e.summary === event.summary)
    if (!existingEvent) {
      acc.push(event)
    }
    return acc
  }, [])

  // Calculate the number of events for each unique event
  uniqueEvents.forEach((event) => {
    const count = events.filter((e) => e.summary === event.summary).length
    event.count = count
  })

  // Calculate the number of hours spent on each unique event
  uniqueEvents.forEach((event) => {
    const hours = events
      .filter((e) => e.summary === event.summary)
      .reduce((acc, e) => acc + e.duration, 0)
    event.hours = parseFloat(hours.toFixed(2))
  })

  // Sort unique events by the number of hours in descending order
  uniqueEvents.sort((a, b) => b.hours - a.hours)

  console.log('Unique events:', uniqueEvents.length)
  const title = `Select event (${uniqueEvents.length})`

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedEventId = event.target.value
    const selectedEvent = uniqueEvents.find((e) => e.id === selectedEventId)
    if (selectedEvent) {
      setFilter(selectedEvent.summary)
    }
  }

  return (
    <select className="calendar-dropdown" onChange={handleChange}>
      <option value="">- {title} -</option>
      {uniqueEvents.map((event) => (
        <option key={event.id} value={event.id}>
          {event.hours}&nbsp;&nbsp;&nbsp;&nbsp;{event.summary}
        </option>
      ))}
    </select>
  )
}

EventTypes.displayName = 'EventTypes'
export default EventTypes
