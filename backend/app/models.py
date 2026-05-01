from app import db
from datetime import datetime

class Repo(db.Model):
    __tablename__ = 'repos'

    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.BigInteger, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(50))
    topics = db.Column(db.JSON, default=list)
    stars = db.Column(db.Integer, default=0)
    forks = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime)
    indexed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'repo_id': self.repo_id,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'language': self.language,
            'topics': self.topics,
            'stars': self.stars,
            'forks': self.forks,
        }
