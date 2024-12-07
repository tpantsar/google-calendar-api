import { format, toZonedTime } from 'date-fns-tz'
import React, { useState } from 'react'
import eventService from '../services/events'
import '../styles/EventForm.css'
import '../styles/Notification.css'
import Event from '../types/Event'
import EventTime from '../types/EventTime'
import NotificationProps from '../types/NotificationProps'
import Notification from './Notification'

type IEventFormProps = {
  calendarId: string
  setEvents: React.Dispatch<React.SetStateAction<Event[]>>
}

const EventForm = ({ calendarId, setEvents }: IEventFormProps) => {
  const formatDateTime = (
    date: Date,
    timeZone: string
  ): EventTime['dateTime'] => {
    const zonedDate = toZonedTime(date, timeZone)
    const dateTime = format(zonedDate, "yyyy-MM-dd'T'HH:mm:ssXXX")
    return dateTime
  }

  const timeZone = 'Europe/Helsinki'

  const HOURS_TO_SUBTRACT = 1
  const initialStartDate = formatDateTime(
    new Date(new Date().getTime() - HOURS_TO_SUBTRACT * 60 * 60 * 1000),
    timeZone
  )
  const initialEndDate = formatDateTime(new Date(), timeZone)

  const [summary, setSummary] = useState('')
  const [description, setDescription] = useState('')
  const [startDate, setStartDate] =
    useState<EventTime['dateTime']>(initialStartDate)
  const [endDate, setEndDate] = useState<EventTime['dateTime']>(initialEndDate)
  const [notificationMessage, setNotificationMessage] =
    useState<NotificationProps['message']>(null)
  const [notificationType, setNotificationType] =
    useState<NotificationProps['type']>('default')

  let timeoutId: number
  let timeoutLength = 5000

  console.log('initialStartDate:', initialStartDate)
  console.log('initialEndDate:', initialEndDate)

  const setNotification = (
    message: NotificationProps['message'],
    type: NotificationProps['type']
  ) => {
    clearTimeout(timeoutId)
    setNotificationMessage(message)
    setNotificationType(type)

    timeoutId = setTimeout(() => {
      setNotificationMessage(null)
      setNotificationType('default')
    }, timeoutLength)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    console.log('summary:', summary)
    console.log('description:', description)
    console.log('startDate:', startDate)
    console.log('endDate:', endDate)

    if (calendarId === '') {
      setNotification('Select a calendar first', 'error')
      return
    }

    if (summary === '') {
      setNotification('Summary is required', 'error')
      return
    }

    const event = {
      start: {
        dateTime: startDate,
        timeZone: timeZone,
      },
      end: {
        dateTime: endDate,
        timeZone: timeZone,
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
