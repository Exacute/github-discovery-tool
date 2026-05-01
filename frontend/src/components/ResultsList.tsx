import ResultCard from './ResultCard'
import './ResultsList.css'

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

interface ResultsListProps {
  repos: Repo[]
}

export default function ResultsList({ repos }: ResultsListProps) {
  return (
    <div className="results-list">
      {repos.map((repo) => (
        <ResultCard
          key={repo.id}
          id={repo.id}
          name={repo.name}
          url={repo.url}
          description={repo.description}
          language={repo.language}
          topics={repo.topics}
          stars={repo.stars}
          forks={repo.forks}
        />
      ))}
    </div>
  )
}
