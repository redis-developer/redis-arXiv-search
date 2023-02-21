
// import Bar from "material-ui-search-bar";
// import ClearIcon from "@material-ui/icons/Clear";
// import grey from '@material-ui/core/colors/grey';
import { OnSearchItemRemove, OnSearchStateChange } from "../../types/search";
import { MultilineSearchField } from "../MultilineSearchField";

interface Props {
  index: number;
  text: string;
  onSearchStateChange: OnSearchStateChange;
  isRemovalEnabled: boolean;
  onSearchItemRemove: OnSearchItemRemove;
}

export const SearchBar = ({
  index,
  text,
  onSearchStateChange,
  isRemovalEnabled,
  onSearchItemRemove
}: Props) => {
  const handleItemRemove = () => isRemovalEnabled && onSearchItemRemove(index)

  const classes: {[key: string]: string} = {}

  if (!isRemovalEnabled) {
    classes.iconButton ='search_bar__button--hidden'
  }

  return (
    <div>
      {/* <Bar
        placeholder="Enter paper's title, abstract or any other text related to this paper"
        value={text}
        onChange={(newValue) => onSearchStateChange(index, newValue)}
        searchIcon={<ClearIcon />}
        onRequestSearch={handleItemRemove} // allow only to delete now
        onCancelSearch={handleItemRemove}

        style={{
          margin: '20px 0',
          boxShadow: '0px 2px 6px 0px rgb(0 0 0 / 20%), 0px 1px 1px 0px rgb(0 0 0 / 14%), 0px 1px 3px 0px rgb(0 0 0 / 12%)'
        }}
        classes={classes}
      /> */}
      <MultilineSearchField
        placeholder="Enter paper's title, abstract or any other text related to this paper"
        value={text}
        onChange={(newValue: string) => onSearchStateChange(index, newValue)}
        onCancelSearch={handleItemRemove}
        isCancelEnabled={isRemovalEnabled}
      />
    </div>
  )
}
