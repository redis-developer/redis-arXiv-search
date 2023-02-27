type ParsedURLSearchParams = { [key: string]: string | string[] }

export const parseURLSearchParams = (params: URLSearchParams): ParsedURLSearchParams => {
  const result: ParsedURLSearchParams = {}

  Array.from(params.entries()).forEach(param => {
    const key = param[0]
    const value = param[1]

    if (result[key] !== undefined) {
      if (Array.isArray(result[key])) {
        (result[key] as string[]).push(value)
      } else {
        result[key] = [result[key] as string, value]
      }
    } else {
      result[key] = value
    }
  })

  return result
}


export const ensureArray = (value: string | string[]): string[] => Array.isArray(value) ? value : [value]


export const getArrayParam = (params: ParsedURLSearchParams, key: string, defaultValue?: any) => {
  const value = params[key] || defaultValue || []

  return ensureArray(value)
}
