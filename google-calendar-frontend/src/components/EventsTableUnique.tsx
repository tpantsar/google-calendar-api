import { useState } from 'react'
import '../styles/EventsTable.css'
import Event from '../types/Event'

type IEventsTableUnique = {
  events: Event[]
  filter: string
  setFilter: React.Dispatch<React.SetStateAction<string>>
}

/* A table of unique events on the calendar */
const EventsTableUnique = ({
  events,
  filter,
  setFilter,
}: IEventsTableUnique) => {
  const [sortColumn, setSortColumn] = useState<string>('summary')
  const [sortDirection, setSortDirection] = useState<boolean>(false) // true for ascending, false for descending

  // Filter events based on the filter state
  const filteredEvents = events.filter((event) =>
    event.summary.toLowerCase().includes(filter.toLowerCase())
  )

  // Find unique events on the calendar based on the event summary
  const uniqueEvents = filteredEvents.reduce((acc: Event[], event: Event) => {
    const existingEvent = acc.find((e) => e.summary === event.summary)
    if (!existingEvent) {
      acc.push(event)
    }
    return acc
  }, [])

  // Calculate the number of events for each unique event
  uniqueEvents.forEach((event) => {
    const count = events.filter((e) => e.summary === event.summary).length
    event.count = count
  })

  // Calculate the number of hours spent on each unique event
  uniqueEvents.forEach((event) => {
    const hours = events
      .filter((e) => e.summary === event.summary)
      .reduce((acc, e) => acc + e.duration, 0)
    event.hours = parseFloat(hours.toFixed(2))
  })

  // Sort unique events based on the current sort column and direction
  uniqueEvents.sort((a, b) => {
    if (sortColumn === 'summary') {
      return sortDirection
        ? a.summary.localeCompare(b.summary)
        : b.summary.localeCompare(a.summary)
    } else if (sortColumn === 'count') {
      return sortDirection ? a.count - b.count : b.count - a.count
    } else if (sortColumn === 'hours') {
      return sortDirection ? a.hours - b.hours : b.hours - a.hours
    }
    return 0
  })

  console.log('Unique events:', uniqueEvents.length)

  const handleSummaryClick = (summary: string) => {
    setFilter(summary)
  }

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortDirection(!sortDirection)
    } else {
      setSortColumn(column)
      setSortDirection(true)
    }
  }

  return (
    <table className="event-table">
      <thead>
        <tr>
          <th>
            Summary
            <button onClick={() => handleSort('summary')}>
              {sortColumn === 'summary' && (sortDirection ? '▼' : '▲')}
            </button>
          </th>
          <th>
            Events
            <button onClick={() => handleSort('count')}>
              {sortColumn === 'count' && (sortDirection ? '▼' : '▲')}
            </button>
          </th>
          <th>
            Hours
            <button onClick={() => handleSort('hours')}>
              {sortColumn === 'hours' && (sortDirection ? '▼' : '▲')}
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        {uniqueEvents.map((event) => (
          <tr key={event.id}>
            <td>
              <span
                onClick={() => handleSummaryClick(event.summary)}
                className="summary-text"
              >
                {event.summary}
              </span>
            </td>
            <td>{event.count}</td>
            <td>{event.hours}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

EventsTableUnique.displayName = 'EventsTableUnique'
export default EventsTableUnique
