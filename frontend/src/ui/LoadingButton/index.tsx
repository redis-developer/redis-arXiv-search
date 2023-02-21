
import {
  Button,
  CircularProgress
} from '@mui/material';
import { ReactElement } from 'react';

interface Props {
  children: ReactElement | string,
  onClick: () => void,
  loading?: boolean;
}

export const LoadingButton = ({ loading, children, ...props }: Props) => {
  const innerContent = loading ? <CircularProgress color="inherit" size={20} /> : children

  return (
    <Button
      variant="contained"
      size="large"
      style={{ width: '150px', height: '42px' }} //hardcoded for now, can be extracted later
      {...props}
    >
      {innerContent}
    </Button>
  )
}
