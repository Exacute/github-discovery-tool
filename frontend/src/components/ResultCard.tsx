import { apiClient } from '../api/client'
import './ResultCard.css'

interface ResultCardProps {
  id: number
  name: string
  url: string
  description: string
  language: string
  topics: string[]
  stars: number
  forks: number
}

export default function ResultCard({
  id,
  name,
  url,
  description,
  language,
  topics,
  stars,
  forks,
}: ResultCardProps) {
  const handleDownload = async () => {
    try {
      await apiClient.downloadRepo(id, name)
    } catch (error) {
      console.error('Download failed:', error)
      alert('Failed to download repository')
    }
  }

  const truncateDescription = (text: string, maxLength: number = 200) => {
    if (!text) return ''
    return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text
  }

  return (
    <div className="result-card">
      <div className="card-header">
        <h2 className="repo-name">
          <a href={url} target="_blank" rel="noopener noreferrer">
            {name}
          </a>
        </h2>
        {language && <span className="language-badge">{language}</span>}
      </div>

      {description && (
        <p className="repo-description">{truncateDescription(description)}</p>
      )}

      <div className="card-meta">
        <div className="meta-item">
          <span className="meta-icon">⭐</span>
          <span className="meta-value">{stars.toLocaleString()} stars</span>
        </div>
        <div className="meta-item">
          <span className="meta-icon">🍴</span>
          <span className="meta-value">{forks.toLocaleString()} forks</span>
        </div>
      </div>

      {topics.length > 0 && (
        <div className="topics">
          {topics.map((topic) => (
            <span key={topic} className="topic-pill">
              {topic}
            </span>
          ))}
        </div>
      )}

      <div className="card-actions">
        <a href={url} target="_blank" rel="noopener noreferrer" className="btn btn-view">
          View on GitHub
        </a>
        <button onClick={handleDownload} className="btn btn-download">
          Download as ZIP
        </button>
      </div>
    </div>
  )
}
