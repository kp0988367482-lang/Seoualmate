const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  })

  const isJson = response.headers.get('content-type')?.includes('application/json')
  const data = isJson ? await response.json() : null

  if (!response.ok) {
    throw new Error(data?.detail || `Request failed (${response.status})`)
  }

  return data
}

export function login(credentials) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  })
}

export function fetchPublicProfiles() {
  return request('/api/profiles')
}

export function fetchDashboard(token) {
  return request('/api/dashboard', {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function fetchUsers(token) {
  return request('/api/users', {
    headers: { Authorization: `Bearer ${token}` },
  })
}
