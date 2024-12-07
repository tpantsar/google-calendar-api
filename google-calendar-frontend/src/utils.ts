import { format } from 'date-fns-tz'

export const formatDateForInput = (date: Date): string => {
  return format(date, "yyyy-MM-dd'T'HH:mm")
}

// Round date to the nearest minutes specified in the roundMinutes argument
export const dateWithRoundedMinutes = (
  date: Date,
  roundMinutes: number
): Date => {
  const incrementedDate = new Date(date.getTime() + roundMinutes * 60 * 1000)
  const minutes = incrementedDate.getMinutes()
  const roundedMinutes = Math.ceil(minutes / 15) * 15
  incrementedDate.setMinutes(roundedMinutes, 0, 0)
  return incrementedDate
}
