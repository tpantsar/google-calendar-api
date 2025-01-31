import Calendar from '../types/Calendar'
import apiClient from './apiClient'

const serviceUrl = '/calendars'

const getAll = (): Promise<Calendar[]> => {
  const request = apiClient.get(serviceUrl)
  return request.then((response) => response.data)
}

const calendarService = {
  getAll,
  displayName: 'CalendarService',
}

export default calendarService
