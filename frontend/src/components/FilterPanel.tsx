import './FilterPanel.css'

interface FilterPanelProps {
  languages: string[]
  topics: string[]
  selectedLanguage: string
  selectedTopic: string
  onLanguageChange: (language: string) => void
  onTopicChange: (topic: string) => void
  onClearFilters: () => void
}

export default function FilterPanel({
  languages,
  topics,
  selectedLanguage,
  selectedTopic,
  onLanguageChange,
  onTopicChange,
  onClearFilters,
}: FilterPanelProps) {
  const hasFilters = selectedLanguage || selectedTopic

  return (
    <div className="filter-panel">
      <h3>Filters</h3>

      <div className="filter-group">
        <label htmlFor="language-select">Language</label>
        <select
          id="language-select"
          value={selectedLanguage}
          onChange={(e) => onLanguageChange(e.target.value)}
          className="filter-select"
        >
          <option value="">All Languages</option>
          {languages.map((lang) => (
            <option key={lang} value={lang}>
              {lang}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="topic-select">Category</label>
        <select
          id="topic-select"
          value={selectedTopic}
          onChange={(e) => onTopicChange(e.target.value)}
          className="filter-select"
        >
          <option value="">All Categories</option>
          {topics.map((topic) => (
            <option key={topic} value={topic}>
              {topic}
            </option>
          ))}
        </select>
      </div>

      {hasFilters && (
        <button className="clear-button" onClick={onClearFilters}>
          Clear Filters
        </button>
      )}
    </div>
  )
}
