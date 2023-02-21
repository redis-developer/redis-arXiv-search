import {
  OutlinedInput,
  InputLabel,
  MenuItem,
  FormControl,
  ListItemText,
  Button,
  Checkbox,
  Tooltip,
  Select,
  SelectChangeEvent,
  CircularProgress
} from '@mui/material';

import { CATEGORY_HUMAN_NAMES, YEAR_FILTER_OPTIONS } from '../../constants/search_filter';
import { SelectControlsWrapper, SelectControl } from './styles';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 150,
    },
  },
};

interface Props {
  years: string[];
  onYearSelection: (event: SelectChangeEvent<string[]>) => void;
  categories: string[];
  onCategorySelection: (event: SelectChangeEvent<string[]>) => void;
  matchExactCategories: boolean;
  onMatchExactCategoriesChange: () => void
}


export const SearchFilters = ({
  years,
  onYearSelection,
  categories,
  onCategorySelection,
  matchExactCategories,
  onMatchExactCategoriesChange
}: Props) => {

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap' }}>
      <FormControl sx={{ width: 150, mr: 1, mt: 1 }}>
        <InputLabel id="demo-multiple-checkbox-label">Year</InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={years}
          onChange={onYearSelection}
          input={<OutlinedInput label="Tag" />}
          renderValue={(selected) => selected.join(', ')}
          MenuProps={MenuProps}
        >
          {YEAR_FILTER_OPTIONS.map((year) => (
            <MenuItem key={year} value={year}>
              <Checkbox checked={years.indexOf(year) > -1} />
              <ListItemText primary={year} />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ m: 0, flex: 1, minWidth: 300, mt: 1 }}>
        <InputLabel id="demo-multiple-checkbox-label">Categories</InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={categories}
          onChange={onCategorySelection}
          input={<OutlinedInput label="Category" />}
          renderValue={(selected) => selected.join(', ')}
          MenuProps={MenuProps}
        >
          <SelectControlsWrapper>
            <div>
              Settings:
            </div>
            <SelectControl onClick={onMatchExactCategoriesChange}>
              <Checkbox checked={matchExactCategories} />Match exact combination of categories
            </SelectControl>

          </SelectControlsWrapper>
          {Object.entries(CATEGORY_HUMAN_NAMES).map(([slug, name]) => (
            <MenuItem key={slug} value={slug}>
              <Checkbox checked={categories.indexOf(slug) > -1} />
              <ListItemText primary={`${slug} (${name})`} />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  )
}
