import React, { useEffect, useState } from 'react'
import eventService from '../services/events'
import '../styles/EventForm.css'
import '../styles/Notification.css'
import Event from '../types/Event'
import NotificationProps from '../types/NotificationProps'
import { formatDateForInput, roundToNearestInterval } from '../utils'
import Notification from './Notification'

type EventFormProps = {
  selectedCalendarId: string
  setEvents: React.Dispatch<React.SetStateAction<Event[]>>
}

const EventForm = ({ selectedCalendarId, setEvents }: EventFormProps) => {
  // Get summary and description from local storage if available
  useEffect(() => {
    const storedSummary = localStorage.getItem('form-summary')
    const storedDescription = localStorage.getItem('form-description')
    if (storedSummary) {
      setSummary(storedSummary)
    }
    if (storedDescription) {
      setDescription(storedDescription)
    }
  }, [])

  const timeZone = 'Europe/Helsinki'

  // Default to the current time minus 1 hour: 14:00 - 15:00
  const HOURS_TO_SUBTRACT = 1
  const initialEndDate = roundToNearestInterval(new Date(), 15)
  const initialStartDate = new Date(
    initialEndDate.getTime() - HOURS_TO_SUBTRACT * 60 * 60 * 1000
  )

  const [summary, setSummary] = useState('')
  const [description, setDescription] = useState('')
  const [startDate, setStartDate] = useState<string>(
    formatDateForInput(initialStartDate)
  )
  const [endDate, setEndDate] = useState<string>(
    formatDateForInput(initialEndDate)
  )
  const [notificationMessage, setNotificationMessage] =
    useState<NotificationProps['message']>(null)
  const [notificationType, setNotificationType] =
    useState<NotificationProps['type']>('default')

  let timeoutId: number
  const timeoutLength = 5000

  const setNotification = (
    message: NotificationProps['message'],
    type: NotificationProps['type']
  ) => {
    clearTimeout(timeoutId)
    setNotificationMessage(message)
    setNotificationType(type)

    timeoutId = window.setTimeout(() => {
      setNotificationMessage(null)
      setNotificationType('default')
    }, timeoutLength)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (selectedCalendarId === '') {
      setNotification('Select a calendar first', 'error')
      return
    }
    if (summary === '') {
      setNotification('Summary is required', 'error')
      return
    }

    const event = {
      start: {
        dateTime: startDate + ':00', // Add seconds for full ISO format
        timeZone: timeZone,
      },
      end: {
        dateTime: endDate + ':00', // Add seconds for full ISO format
        timeZone: timeZone,
      },
      summary: summary,
      description: description,
    } as Event

    eventService
      .create(selectedCalendarId, event)
      .then((newEvent: Event) => {
        console.log('Creating event:', newEvent)
        setEvents((events) => [...events, newEvent])
        setSummary('')
        setDescription('')
        setStartDate(formatDateForInput(initialStartDate))
        setEndDate(formatDateForInput(initialEndDate))
        setNotification('Event created successfully', 'success')
      })
      .catch((error: unknown) => {
        console.error('Error creating event:', error)
        setNotification('Error creating event', 'error')
      })
  }

  const handleSummaryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    event.preventDefault()
    setSummary(event.target.value)
    localStorage.setItem('form-summary', event.target.value)
  }

  const handleDescriptionChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    event.preventDefault()
    setDescription(event.target.value)
    localStorage.setItem('form-description', event.target.value)
  }

  return (
    <div className="form-container">
      <Notification message={notificationMessage} type={notificationType} />
      <form onSubmit={handleSubmit}>
        <label className="form-label" htmlFor="summary">
          Summary
        </label>
        <input
          className="form-input"
          type="text"
          id="summary"
          value={summary}
          onChange={(e) => handleSummaryChange(e)}
        />

        <label className="form-label" htmlFor="description">
          Description
        </label>
        <textarea
          className="form-textarea"
          id="description"
          value={description}
          onChange={(e) => handleDescriptionChange(e)}
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
            setSummary('')
            setDescription('')
            setStartDate(formatDateForInput(initialStartDate))
            setEndDate(formatDateForInput(initialEndDate))
          }}
        >
          Reset
        </button>
      </form>
    </div>
  )
}

EventForm.displayName = 'EventForm'
export default EventForm
