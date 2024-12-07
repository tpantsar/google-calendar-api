import { format } from 'date-fns-tz'

export const formatDateForInput = (date: Date): string => {
  return format(date, "yyyy-MM-dd'T'HH:mm")
}

// Round date to the nearest minutes specified in the intervalMinutes argument
export const roundToNearestInterval = (
  timestamp: Date,
  intervalMinutes: number = 15
): Date => {
  if (intervalMinutes > 60 || intervalMinutes <= 0) {
    throw new Error('intervalMinutes must be between 1 and 60')
  }

  const year = timestamp.getFullYear()
  const month = timestamp.getMonth() // Note: getMonth is 0-based (January = 0)
  const day = timestamp.getDate()
  const hour = timestamp.getHours()
  const minute = timestamp.getMinutes()

  // Calculate the nearest interval
  let nearestIntervalMinute =
    Math.round(minute / intervalMinutes) * intervalMinutes
  let newHour = hour
  let newDay = day
  let newMonth = month
  let newYear = year

  // Handle overflow if nearestIntervalMinute >= 60
  if (nearestIntervalMinute >= 60) {
    nearestIntervalMinute = 0
    newHour += 1

    // Handle overflow if hour >= 24
    if (newHour >= 24) {
      newHour = 0
      newDay += 1

      // Check if day exceeds the last day of the current month
      const lastDayOfMonth = new Date(newYear, newMonth + 1, 0).getDate()
      if (newDay > lastDayOfMonth) {
        newDay = 1
        newMonth += 1

        // Handle overflow if month > 11
        if (newMonth > 11) {
          newMonth = 0
          newYear += 1
        }
      }
    }
  }

  // Return the new rounded date
  return new Date(
    newYear,
    newMonth,
    newDay,
    newHour,
    nearestIntervalMinute,
    0,
    0
  )
}
