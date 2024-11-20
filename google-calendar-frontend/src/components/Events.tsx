import React, { useState } from 'react'
import eventService from '../services/Events'
import '../styles/Events.css'
import Event from '../types/Event'

type IEventsProps = {
  calendarId: string
  events: Event[]
  filter: string
  setFilter: React.Dispatch<React.SetStateAction<string>>
  setEvents: React.Dispatch<React.SetStateAction<Event[]>>
}

const Events = ({
  calendarId,
  events,
  filter,
  setFilter,
  setEvents,
}: IEventsProps) => {
  const [sort, setSort] = useState<boolean>(false)
  const [showFutureEvents, setShowFutureEvents] = useState<boolean>(false)

  console.log('Calendar ID:', calendarId)
  const toggleFutureEvents = () => setShowFutureEvents(!showFutureEvents)

  // Filter events based on the filter and showFutureEvents state
  const filteredEvents = events.filter(
    (event) =>
      event.summary.toLowerCase().includes(filter.toLowerCase()) &&
      (showFutureEvents || !event.isFuture)
  )

  // Sort events by start date
  if (sort) {
    filteredEvents.sort(
      (a, b) =>
        new Date(a.start.dateTime).getTime() -
        new Date(b.start.dateTime).getTime()
    )
  }

  const deleteEvent = (event: Event) => {
    const result = window.confirm(`Delete event: ${event.summary}?`)
    if (result) {
      eventService
        .remove(calendarId, event.id)
        .then(() => {
          console.log('Event deleted:', event.id)
          const updatedEvents = events.filter(
            (eventItem) => eventItem.id !== event.id
          )
          setEvents(updatedEvents)
        })
        .catch((error: unknown) =>
          console.error('Error deleting event:', error)
        )
    }
  }

  const handleSummaryClick = (summary: string) => {
    setFilter(summary)
  }

  return (
    <>
      <div className="flex-container">
        <h2>Events: {filteredEvents.length}</h2>
        <h2>
          Types: {new Set(filteredEvents.map((event) => event.summary)).size}
        </h2>
        <h2>
          Hours:{' '}
          {filteredEvents
            .reduce((acc, event) => acc + event.duration, 0)
            .toFixed(2)}
        </h2>
        <div className="flex-container">
          <h3>
            Future events: {events.filter((event) => event.isFuture).length}
          </h3>
          <button onClick={toggleFutureEvents}>
            {showFutureEvents ? 'Hide' : 'Show'}
          </button>
        </div>
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
                <i
                  onClick={() => deleteEvent(event)}
                  className="icon-trashcan fa-solid fa-trash-can"
                ></i>
                <a href={event.htmlLink} target="_blank" rel="noreferrer">
                  <i className="icon-arrow fa-solid fa-arrow-up-right-from-square"></i>
                </a>
                <span
                  onClick={() => handleSummaryClick(event.summary)}
                  style={{ cursor: 'pointer', color: 'blue' }}
                >
                  {event.summary}
                </span>
                <span>{event.isFuture ? ' (Future event)' : ''}</span>
              </td>
              <td>{event.formatted_start}</td>
              <td>{event.formatted_end}</td>
              <td>{event.duration.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

Events.displayName = 'Events'
export default Events
