export function objectToRows(data, labelMap = {}) {
  return Object.entries(data).map(
    ([key, value]) => ({
      label: labelMap[key] ?? key,
      value,
    }),
  )
}
