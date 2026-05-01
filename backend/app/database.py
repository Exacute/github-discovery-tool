from app import db
from app.models import Repo
from sqlalchemy import func, or_

def search_repos(query, language=None, topic=None, limit=5):
    """
    Search repositories by keyword with optional filters for language and topic.
    Results are sorted by stars (descending).
    """
    sql_query = db.session.query(Repo)

    if query and query.strip():
        # Split query into words and search for any match
        search_pattern = f"%{query}%"
        sql_query = sql_query.filter(
            or_(
                Repo.name.ilike(search_pattern),
                Repo.description.ilike(search_pattern),
                Repo.topics.contains(f'"{query.lower()}"')
            )
        )

    if language:
        sql_query = sql_query.filter(Repo.language.ilike(language))

    if topic:
        # Filter by topic - case-insensitive
        sql_query = sql_query.filter(Repo.topics.contains(f'"{topic.lower()}"'))

    results = sql_query.order_by(Repo.stars.desc()).limit(limit).all()
    return [repo.to_dict() for repo in results]

def get_languages():
    """Get all distinct languages from indexed repos."""
    languages = db.session.query(Repo.language).distinct().filter(
        Repo.language != None
    ).all()
    return sorted([lang[0] for lang in languages if lang[0]])

def get_topics():
    """Get all distinct topics from indexed repos."""
    topics_data = db.session.query(Repo.topics).all()
    topics_set = set()
    for row in topics_data:
        if row[0]:
            topics_set.update(row[0])
    return sorted(list(topics_set))

def get_repo_by_id(repo_id):
    """Get a single repository by ID."""
    repo = db.session.query(Repo).filter(Repo.id == repo_id).first()
    return repo

def add_repo(repo_data):
    """Add a new repository to the database."""
    repo = Repo(
        repo_id=repo_data['repo_id'],
        name=repo_data['name'],
        url=repo_data['url'],
        description=repo_data.get('description'),
        language=repo_data.get('language'),
        topics=repo_data.get('topics', []),
        stars=repo_data.get('stars', 0),
        forks=repo_data.get('forks', 0),
        last_updated=repo_data.get('last_updated'),
    )
    db.session.add(repo)
    db.session.commit()
    return repo
