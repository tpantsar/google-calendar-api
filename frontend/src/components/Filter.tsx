type FilterProps = {
  filter: string
  setFilter: React.Dispatch<React.SetStateAction<string>>
}

const Filter = ({ filter, setFilter }: FilterProps) => {
  return (
    <div className="flex-container">
      Filter events:{' '}
      <input value={filter} onChange={(e) => setFilter(e.target.value)} />
      <button onClick={() => setFilter('')}>Clear</button>
    </div>
  )
}

Filter.displayName = 'Filter'
export default Filter
