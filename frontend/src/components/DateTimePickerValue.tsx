import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import dayjs, { Dayjs } from 'dayjs'
import { useState } from 'react'

interface DateTimePickerValueProps {
  label: string
  initialValue?: string
}

// https://mui.com/x/react-date-pickers/date-time-picker/
export default function DateTimePickerValue({
  label,
  initialValue,
}: DateTimePickerValueProps) {
  // dayjs('2022-04-17T15:30')
  const defaultInitialValue = initialValue ? dayjs(initialValue) : null
  const [value, setValue] = useState<Dayjs | null>(defaultInitialValue)

  console.log('value:', value?.toISOString())

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DateTimePicker
        label={label}
        value={value}
        onChange={(newValue) => setValue(newValue)}
      />
    </LocalizationProvider>
  )
}
