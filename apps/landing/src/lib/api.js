const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

export async function fetchPublicProfiles() {
  const response = await fetch(`${API_BASE}/api/profiles`)
  if (!response.ok) {
    throw new Error('Failed to fetch profiles')
  }
  return response.json()
}
