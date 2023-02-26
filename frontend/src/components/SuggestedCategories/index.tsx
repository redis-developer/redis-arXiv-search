import { Link } from "@mui/material"
import { Root } from './styles'
import { CATEGORY_HUMAN_NAMES } from '../../constants/search_filter';

export const SuggestedCategories = ({ options, onClick }: { options: string[], onClick: () => void }) => {
  if (options.length === 0) return <></>

  return (
    <Root>
      <b>Suggested categories:</b> <br />
      {options.map(slug =>
        <div>{slug}</div>
      )} <br />
      <Link component="button" underline="hover" onClick={onClick}>Click here to apply them</Link>
    </Root>
  )
}

