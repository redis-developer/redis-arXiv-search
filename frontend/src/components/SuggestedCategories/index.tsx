import { Link } from "@mui/material"
import { CATEGORY_HUMAN_NAMES } from '../../constants/search_filter';

export const SuggestedCategories = ({options, onClick}: {options: string[], onClick: () => void}) => {
  if (options.length === 0) return <></>

  return (
    <div className="pt-2">
      <a style={{backgroundColor: "#FFD801"}}>We found suggested categories for your query:</a> <br /> {options.map(slug =>
        <div>{slug} ({CATEGORY_HUMAN_NAMES[slug as keyof typeof CATEGORY_HUMAN_NAMES]})</div>
      )} <br />
      <Link component="button" underline="hover" onClick={onClick}>Apply them</Link>
    </div>
  )
}

