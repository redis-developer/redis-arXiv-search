import { ClearButton, Root, TextArea } from "./styles"
import ClearIcon from "@material-ui/icons/Clear";
import { ReactElement } from "react";

interface Props {
  value: string
  placeholder: string
  height?: number
  onChange: any
  onCancelSearch: any
  isCancelEnabled: boolean
}

export const MultilineSearchField = ({
  value,
  placeholder,
  height = 200,
  onChange,
  onCancelSearch,
  isCancelEnabled
}: Props) => {

  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(event.target.value)
  };

  return (
    <Root height={height}>
      <TextArea
        {...{
          placeholder,
          onChange: handleTextChange
        }}
      >
        {value}
      </TextArea>
      {isCancelEnabled
        &&
        <ClearButton onClick={onCancelSearch}>
          <ClearIcon />
        </ClearButton>
      }
    </Root>
  )
}
