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
export async function put(
  path,
  body,
) {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      method: 'PUT',

      headers: {
        'Content-Type':
          'application/json',
      },

      body: JSON.stringify(body),
    },
  )

  if (!response.ok) {
    const data =
      await response.json()

    throw new Error(
      data.detail ??
        `API request failed: ${response.status}`,
    )
  }

  return await response.json()
}
export async function remove(
  path,
) {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      method: 'DELETE',
    },
  )

  if (!response.ok) {
    let message = `API request failed: ${response.status}`

    try {
      const body =
        await response.json()

      message =
        body.detail ?? message
    }
    catch {
      //
      // Ignore
      //
    }

    throw new Error(message)
  }
}
