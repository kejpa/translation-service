const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function get(path) {
  const response = await fetch(`${API_BASE_URL}${path}`,)

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`,)
  }

  return await response.json()
}

export async function postFormData(path, formData,) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST', body: formData,
  },)

  if (!response.ok) {
    const body = await response.json()

    throw new Error(body.detail ?? `API request failed: ${response.status}`,)
  }
  return await response.json()
}
