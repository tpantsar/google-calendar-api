import axios from 'axios'
import Event from '../types/Event'
import UpdateEventRequestBody from '../types/UpdateEventRequestBody'

const baseUrl = '/api/events'

const getAll = (calendar_id: string): Promise<Event[]> => {
  const url = `${baseUrl}/${calendar_id}`
  const request = axios.get(url)
  console.log('Fetching events from:', url)
  return request.then((response) => response.data)
}

const create = (calendar_id: string, newObject: Event): Promise<Event> => {
  const url = `${baseUrl}/${calendar_id}`
  const request = axios.post(url, newObject)
  console.log('Creating new event:', url)
  return request.then((response) => response.data)
}

const remove = (calendar_id: string, event_id: string): Promise<void> => {
  const url = `${baseUrl}/${calendar_id}/${event_id}`
  const request = axios.delete(url)
  console.log('Deleting event:', url)
  return request.then((response) => response.data)
}

const update = (
  calendar_id: string,
  event_id: string,
  request_body: UpdateEventRequestBody
): Promise<Event> => {
  const url = `${baseUrl}/${calendar_id}/${event_id}`
  const request = axios.put(url, request_body)
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
