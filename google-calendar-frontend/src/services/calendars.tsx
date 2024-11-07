import axios from 'axios'
import Calendar from '../types/Calendar'

const baseUrl = '/api/calendars'

const getAll = (): Promise<Calendar[]> => {
  const request = axios.get(baseUrl)
  return request.then((response) => response.data)
}

export default { getAll }
