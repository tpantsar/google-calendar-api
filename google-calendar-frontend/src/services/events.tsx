import axios from 'axios'
import Event from '../types/Event'

const baseUrl = '/api/events'

const getAll = (year: number, calendar_id: string): Promise<Event[]> => {
  const url = `${baseUrl}/${year}/${calendar_id}`
  const request = axios.get(url)
  console.log('Fetching events from:', url)
  return request.then((response) => response.data)
}

export default { getAll }
