import React, { useState } from 'react'
import eventService from '../services/events'
import '../styles/EventForm.css'
import Event from '../types/Event'

type IEventFormProps = {
  calendarId: string
  setEvents: React.Dispatch<React.SetStateAction<Event[]>>
}

const EventForm = ({ calendarId, setEvents }: IEventFormProps) => {
  const [summary, setSummary] = useState('')
  const [description, setDescription] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const setNotification = (message: string, type: 'error' | 'success') => {
    if (type === 'error') {
      setError(message)
      setSuccess('')
    } else {
      setSuccess(message)
      setError('')
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    console.log('summary:', summary)
    console.log('description:', description)

    if (calendarId === '') {
      setNotification('Select a calendar first', 'error')
      return
    }

    if (summary === '') {
      setNotification('Summary is required', 'error')
      return
    }

    const hoursToSubtract = 1
    const event = {
      start: {
        dateTime: new Date(
          new Date().getTime() - hoursToSubtract * 60 * 60 * 1000
        ).toISOString(),
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
      .create(calendarId, event)
      .then((event: Event) => {
        console.log('Event created:', event)
        setEvents((events) => [...events, event])
        setSummary('')
        setDescription('')
        setNotification('Event created successfully', 'success')
      })
      .catch((error: unknown) => {
        console.error('Error creating event:', error)
        setNotification('Error creating event', 'error')
      })
  }

  return (
    <div className="form-container">
      {error && <div className="notification-error">{error}</div>}
      {success && <div className="notification-success">{success}</div>}
      <form onSubmit={handleSubmit}>
        <label className="form-label" htmlFor="summary">
          Summary
        </label>
        <input
          className="form-input"
          type="text"
          id="summary"
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
        />

        <label className="form-label" htmlFor="description">
          Description
        </label>
        <textarea
          className="form-textarea"
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>

        <label className="form-label" htmlFor="startDate">
          Start Date
        </label>
        <input
          className="form-input"
          type="datetime-local"
          id="startDate"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />

        <label className="form-label" htmlFor="endDate">
          End Date
        </label>
        <input
          className="form-input"
          type="datetime-local"
          id="endDate"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />

        <button className="form-button" type="submit">
          Create
        </button>
        <button
          className="form-button form-button-cancel"
          type="button"
          onClick={() => {
            // Handle cancel logic here
          }}
        >
          Cancel
        </button>
      </form>
    </div>
  )
}

EventForm.displayName = 'EventForm'
export default EventForm
