import Event from '../types/Event'
import UpdateEventRequestBody from '../types/UpdateEventRequestBody'
import apiClient from './apiClient'

const serviceUrl = '/events'

const getAll = (calendar_id: string): Promise<Event[]> => {
  const url = `${serviceUrl}/${calendar_id}`
  const request = apiClient.get(url)
  console.log('Fetching events from:', url)
  return request.then((response) => response.data)
}

const create = (calendar_id: string, newEvent: Event): Promise<Event> => {
  const url = `${serviceUrl}/${calendar_id}`
  const request = apiClient.post(url, newEvent)
  console.log('Creating new event - newEvent:', newEvent)
  return request.then((response) => response.data)
}

const remove = (calendar_id: string, event_id: string): Promise<void> => {
  const url = `${serviceUrl}/${calendar_id}/${event_id}`
  const request = apiClient.delete(url)
  console.log('Deleting event:', url)
  return request.then((response) => response.data)
}

const update = (
  calendar_id: string,
  event_id: string,
  request_body: UpdateEventRequestBody
): Promise<Event> => {
  const url = `${serviceUrl}/${calendar_id}/${event_id}`
  const request = apiClient.put(url, request_body)
  console.log('Updating event:', url)
  return request.then((response) => response.data)
}

const eventService = {
  getAll,
  create,
  remove,
  update,
  displayName: 'EventService',
}

export default eventService
