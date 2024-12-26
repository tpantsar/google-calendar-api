import { describe, expect, it } from 'vitest'
import { roundToNearestInterval } from '../src/utils'

describe('dateWithRoundedMinutes', () => {
  it('should throw when roundMinutes is zero', () => {
    const date = new Date('2023-10-10T10:05:00')
    expect(() => roundToNearestInterval(date, 0)).toThrow(
      'intervalMinutes must be between 1 and 60'
    )
  })

  it('should throw when roundMinutes is negative', () => {
    const date = new Date('2023-10-10T10:05:00')
    expect(() => roundToNearestInterval(date, -5)).toThrow(
      'intervalMinutes must be between 1 and 60'
    )
  })

  it('should throw when roundMinutes is over 60', () => {
    const date = new Date('2023-10-10T10:05:00')
    expect(() => roundToNearestInterval(date, 65)).toThrow(
      'intervalMinutes must be between 1 and 60'
    )
  })

  it('should round up to the nearest 5 minutes increment', () => {
    const date = new Date('2023-10-10T10:12:00')
    const roundedDate = roundToNearestInterval(date, 5)
    expect(roundedDate.getMinutes()).toBe(10)
  })

  it('should round up to the nearest 15 minutes increment', () => {
    const date = new Date('2023-10-10T17:23:00')
    const roundedDate = roundToNearestInterval(date, 15)
    expect(roundedDate.getMinutes()).toBe(30)
    expect(roundedDate.getHours()).toBe(17)
  })

  it('should round down to the nearest 15 minutes increment', () => {
    const date = new Date('2023-10-10T17:22:00')
    const roundedDate = roundToNearestInterval(date, 15)
    expect(roundedDate.getMinutes()).toBe(15)
    expect(roundedDate.getHours()).toBe(17)
  })

  it('should round up to the next hour if minutes exceed 60', () => {
    const date = new Date('2023-10-10T10:58:00')
    const roundedDate = roundToNearestInterval(date, 15)
    expect(roundedDate.getMinutes()).toBe(0)
    expect(roundedDate.getHours()).toBe(11)
  })

  it('should handle rounding correctly at the end of the day', () => {
    const date = new Date('2023-10-10T23:59:00')
    const roundedDate = roundToNearestInterval(date, 15)
    expect(roundedDate.getMinutes()).toBe(0)
    expect(roundedDate.getHours()).toBe(0)
    expect(roundedDate.getDate()).toBe(11)
  })

  it('should handle rounding correctly at the end of the month', () => {
    const date = new Date('2023-10-31T23:59:00')
    const roundedDate = roundToNearestInterval(date, 15)
    console.log('roundedDate', roundedDate)
    expect(roundedDate.getMinutes()).toBe(0)
    expect(roundedDate.getHours()).toBe(0)
    expect(roundedDate.getDate()).toBe(1)
    expect(roundedDate.getMonth()).toBe(10) // November is month 10 in JavaScript
  })

  it('should handle rounding correctly at the end of the year', () => {
    const date = new Date('2023-12-31T23:59:00')
    const roundedDate = roundToNearestInterval(date, 15)
    expect(roundedDate.getMinutes()).toBe(0)
    expect(roundedDate.getHours()).toBe(0)
    expect(roundedDate.getDate()).toBe(1)
    expect(roundedDate.getMonth()).toBe(0)
    expect(roundedDate.getFullYear()).toBe(2024)
  })
})
