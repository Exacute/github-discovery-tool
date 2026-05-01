import { useState, useEffect } from 'react'
import './App.css'
import SearchBar from './components/SearchBar'
import FilterPanel from './components/FilterPanel'
import ResultsList from './components/ResultsList'
import { apiClient } from './api/client'

interface Repo {
  id: number
  repo_id: number
  name: string
  url: string
  description: string
  language: string
  topics: string[]
  stars: number
  forks: number
}

function App() {
  const [query, setQuery] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('')
  const [selectedTopic, setSelectedTopic] = useState('')
  const [results, setResults] = useState<Repo[]>([])
  const [languages, setLanguages] = useState<string[]>([])
  const [topics, setTopics] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchFilters()
  }, [])

  const fetchFilters = async () => {
    try {
      const [langs, topicsList] = await Promise.all([
        apiClient.getLanguages(),
        apiClient.getTopics(),
      ])
      setLanguages(langs)
      setTopics(topicsList)
    } catch (err) {
      console.error('Failed to fetch filters:', err)
    }
  }

  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery)
    if (!searchQuery.trim()) {
      setResults([])
      setError('')
      return
    }

    setLoading(true)
    setError('')
    try {
      const data = await apiClient.search(
        searchQuery,
        selectedLanguage,
        selectedTopic
      )
      setResults(data)
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err)
      setError(`Failed to search repositories: ${errorMsg}\n\nMake sure Flask is running on http://localhost:5000`)
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLanguageChange = async (language: string) => {
    setSelectedLanguage(language)
    if (query.trim()) {
      setLoading(true)
      setError('')
      try {
        const data = await apiClient.search(query, language, selectedTopic)
        setResults(data)
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : String(err)
        setError(`Failed to search: ${errorMsg}`)
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
  }

  const handleTopicChange = async (topic: string) => {
    setSelectedTopic(topic)
    if (query.trim()) {
      setLoading(true)
      setError('')
      try {
        const data = await apiClient.search(query, selectedLanguage, topic)
        setResults(data)
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : String(err)
        setError(`Failed to search: ${errorMsg}`)
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
  }

  const handleClearFilters = async () => {
    setSelectedLanguage('')
    setSelectedTopic('')
    if (query.trim()) {
      setLoading(true)
      setError('')
      try {
        const data = await apiClient.search(query, '', '')
        setResults(data)
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : String(err)
        setError(`Failed to search: ${errorMsg}`)
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>GitHub Project Discovery</h1>
        <p>Find the perfect open-source project to use as a starting point</p>
      </header>

      <div className="app-container">
        <div className="search-section">
          <SearchBar onSearch={handleSearch} />
        </div>

        <div className="main-content">
          <aside className="sidebar">
            <FilterPanel
              languages={languages}
              topics={topics}
              selectedLanguage={selectedLanguage}
              selectedTopic={selectedTopic}
              onLanguageChange={handleLanguageChange}
              onTopicChange={handleTopicChange}
              onClearFilters={handleClearFilters}
            />
          </aside>

          <main className="results-section">
            {error && <div className="error-message">{error}</div>}
            {loading && <div className="loading">Searching repositories...</div>}
            {!loading && results.length === 0 && query && (
              <div className="no-results">No repositories found</div>
            )}
            {results.length > 0 && (
              <div className="results-info">Found {results.length} repositories</div>
            )}
            <ResultsList repos={results} />
          </main>
        </div>
      </div>
    </div>
  )
}

export default App
