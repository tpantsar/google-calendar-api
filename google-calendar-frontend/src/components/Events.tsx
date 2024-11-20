import React, { useState } from 'react'
import eventService from '../services/Events'
import Event from '../types/Event'
import EventsTableAll from './EventsTableAll'
import EventsTableUnique from './EventsTableUnique'

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
  const [showAllEvents, setShowAllEvents] = useState(true)

  const toggleAllEvents = () => setShowAllEvents(!showAllEvents)

  console.log('Calendar ID:', calendarId)

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

  return (
    <>
      <button onClick={toggleAllEvents}>
        {showAllEvents ? 'Show Unique Events' : 'Show All Events'}
      </button>
      {showAllEvents ? (
        <>
          <EventsTableAll
            events={events}
            filter={filter}
            setFilter={setFilter}
            deleteEvent={deleteEvent}
          />
        </>
      ) : (
        <EventsTableUnique
          events={events}
          filter={filter}
          setFilter={setFilter}
          setShowAllEvents={setShowAllEvents}
        />
      )}
    </>
  )
}

Events.displayName = 'Events'
export default Events
