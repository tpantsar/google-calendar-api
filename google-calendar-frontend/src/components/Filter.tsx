type IFilterProps = {
  filter: string
  setFilter: React.Dispatch<React.SetStateAction<string>>
}

const Filter = ({ filter, setFilter }: IFilterProps) => {
  return (
    <div>
      Filter events:{' '}
      <input value={filter} onChange={(e) => setFilter(e.target.value)} />
    </div>
  )
}

Filter.displayName = 'Filter'
export default Filter
