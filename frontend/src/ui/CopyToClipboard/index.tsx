import { Snackbar, Link } from '@mui/material'
import ShareIcon from '@mui/icons-material/Share';
import { useState } from 'react'
import { Root } from './styles';


const CopyToClipboardButton = () => {
  const [open, setOpen] = useState(false)

  const handleClick = () => {
    setOpen(true)
    navigator.clipboard.writeText(window.location.toString())
  }

  return (
    <>
      <Root onClick={handleClick}>
        <Link style={{paddingRight: '8px'}} component="button" underline="always">Share results </Link>
        <ShareIcon />
      </Root>

      <Snackbar
        open={open}
        onClose={() => setOpen(false)}
        autoHideDuration={2000}
        message="Copied to clipboard"
      />
    </>
  )
}
export default CopyToClipboardButton
