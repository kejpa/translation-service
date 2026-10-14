export function objectToRows(  data,  labelMap = {},  valueMap = {},) {
  return Object.entries(data).map(
    ([key, value]) => ({
      label: labelMap[key] ?? key,
      value: valueMap[key]?.(value) ?? value,
    }),
  )
}
