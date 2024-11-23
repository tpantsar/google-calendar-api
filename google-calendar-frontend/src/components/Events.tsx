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

  const updateEvent = (event: Event, newSummary: string) => {
    const result = window.confirm(`Update event: ${event.summary}?`)
    if (result) {
      eventService
        .update(calendarId, event.id, { ...event, summary: newSummary })
        .then((updatedEvent: Event) => {
          console.log('Event updated:', updatedEvent)
          const updatedEvents = events.map((eventItem) =>
            eventItem.id === updatedEvent.id ? updatedEvent : eventItem
          )
          setEvents(updatedEvents)
        })
        .catch((error: unknown) =>
          console.error('Error updating event:', error)
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
            updateEvent={updateEvent}
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
