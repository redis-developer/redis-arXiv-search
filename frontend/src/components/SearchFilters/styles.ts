import styled from 'styled-components'

export const SelectControlsWrapper = styled.div`
  position: sticky;
  z-index: 3;
  top: 0;
  left: 0;
  right: 0;

  height: 60px;
  line-height: 60px;
  padding: 0 16px;
  background-color: #eee;

  display: flex;
`

export const SelectControl = styled.div`
  cursor: pointer;
  user-select: none;
`
