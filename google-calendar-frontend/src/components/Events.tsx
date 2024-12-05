import React, { useState } from 'react'
import eventService from '../services/events'
import Event from '../types/Event'
import EventsTableAll from './EventsTableAll'
import EventsTableUnique from './EventsTableUnique'
import UpdateEventRequestBody from '../types/UpdateEventRequestBody'

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
  const [showAllEvents, setShowAllEvents] = useState(false)

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

  const updateEvent = (event: Event, request_body: UpdateEventRequestBody) => {
    console.log(
      `updateEvent: event.id = ${event.id} calendarId = ${calendarId}, request_body = ${JSON.stringify(
        request_body
      )}`
    )
    const result = window.confirm(`Update event: ${event.summary}?`)
    if (result) {
      eventService
        .update(calendarId, event.id, request_body)
        .then((updatedEvent: Event) => {
          console.log('Event updated:', updatedEvent)
          const updatedEvents = events.map((e) =>
            e.id === updatedEvent.id ? updatedEvent : e
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
        {showAllEvents ? 'Unique Events' : 'All Events'}
      </button>
      {showAllEvents ? (
        <>
          <EventsTableAll
            events={events}
            filter={filter}
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
