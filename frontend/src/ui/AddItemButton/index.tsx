import { Root, IconWrapper } from "./styles";
import AddIcon from '@mui/icons-material/Add';

interface Props {
  text: string;
  onClick: () => void
}

export const AddItemButton = ({ text, ...props }: Props) => {

  return (
    <Root {...props}>
      <IconWrapper>
        <AddIcon />
      </IconWrapper>

      <div>
        {text}
      </div>
    </Root>
  )
}
