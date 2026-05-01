const API_BASE_URL = 'http://localhost:5000/api'

interface SearchResponse {
  repos: Array<{
    id: number
    repo_id: number
    name: string
    url: string
    description: string
    language: string
    topics: string[]
    stars: number
    forks: number
  }>
}

export const apiClient = {
  async search(query: string, language?: string, topic?: string) {
    const params = new URLSearchParams({ query })
    if (language) params.append('language', language)
    if (topic) params.append('topic', topic)

    const response = await fetch(`${API_BASE_URL}/search?${params}`)
    if (!response.ok) throw new Error('Search failed')

    const data: SearchResponse = await response.json()
    return data.repos
  },

  async getLanguages() {
    const response = await fetch(`${API_BASE_URL}/languages`)
    if (!response.ok) throw new Error('Failed to fetch languages')

    const data = await response.json()
    return data.languages
  },

  async getTopics() {
    const response = await fetch(`${API_BASE_URL}/topics`)
    if (!response.ok) throw new Error('Failed to fetch topics')

    const data = await response.json()
    return data.topics
  },

  async downloadRepo(repoId: number, repoName: string) {
    const response = await fetch(`${API_BASE_URL}/repos/${repoId}/download`, {
      method: 'POST',
    })
    if (!response.ok) throw new Error('Download failed')

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${repoName}.zip`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  },
}
