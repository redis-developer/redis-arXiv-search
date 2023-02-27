export type SearchStates = string[]

export type OnSearchStateChange = (index: number, newText: string) => void
export type OnSearchItemRemove = (index: number) => void
