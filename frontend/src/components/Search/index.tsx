
import { OnSearchItemRemove, OnSearchStateChange, SearchStates } from "../../types/search";

import { SearchBar } from '../../ui/SearchBar'

interface Props {
  searchStates: SearchStates
  onSearchStateChange: OnSearchStateChange
  onSearchItemRemove: OnSearchItemRemove
}

export const Search = ({ searchStates, ...props }: Props) => {

  return (
    <div>
      {searchStates.map(
        (searchState, index) =>
          <SearchBar
            key={index}
            index={index}
            text={searchState}
            isRemovalEnabled={searchStates.length > 1}
            {...props}
          />
      )}
    </div>
  )
}
