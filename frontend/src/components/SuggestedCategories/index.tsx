import { Link } from "@mui/material"
import { Root } from './styles'
import { CATEGORY_HUMAN_NAMES } from '../../constants/search_filter';

export const SuggestedCategories = ({ options, onClick }: { options: string[], onClick: () => void }) => {
  if (options.length === 0) return <></>

  return (
    <Root>
      <b>We found suggested categories for your query:</b> <br />
      {['asd', 'asdasd'].map(slug =>
        <div>{slug} ({CATEGORY_HUMAN_NAMES[slug as keyof typeof CATEGORY_HUMAN_NAMES]})</div>
      )} <br />
      <Link component="button" underline="hover" onClick={onClick}>Click here to pply them</Link>
    </Root>
  )
}

