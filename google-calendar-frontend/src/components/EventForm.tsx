import React, { useState } from 'react'
import eventService from '../services/events'
import Event from '../types/Event'

type IEventsProps = {
  calendarId: string
  setEvents: React.Dispatch<React.SetStateAction<Event[]>>
}

const EventForm = ({ calendarId, setEvents }: IEventsProps) => {
  const [summary, setSummary] = useState<string>('')
  const [description, setDescription] = useState<string>('')

  const createEvent = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    console.log('summary:', summary)
    console.log('description:', description)

    if (calendarId === '') {
      alert('Select a calendar first')
      return
    }

    if (summary === '') {
      alert('Summary is required')
      return
    }

    const newEvent = {
      start: {
        dateTime: new Date().toISOString(),
        timeZone: 'Europe/Helsinki',
      },
      end: {
        dateTime: new Date().toISOString(),
        timeZone: 'Europe/Helsinki',
      },
      summary: summary,
      description: description,
    } as Event

    eventService
      .create(calendarId, newEvent)
      .then((event: Event) => {
        console.log('Event created:', event)
        setEvents((events) => [...events, event])
        setSummary('')
        setDescription('')
      })
      .catch((error: unknown) => console.error('Error creating event:', error))
  }

  return (
    <div className="event-form">
      <form onSubmit={createEvent}>
        <div className="flex-container">
          <label htmlFor="summary">Summary:</label>
          <input
            type="text"
            id="summary"
            name="summary"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
          />
        </div>
        <div className="flex-container">
          <label htmlFor="description">Description:</label>
          <input
            type="text"
            id="description"
            name="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <button type="submit">Create</button>
      </form>
    </div>
  )
}

EventForm.displayName = 'EventForm'
export default EventForm
