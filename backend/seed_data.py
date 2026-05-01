from app import create_app, db
from app.models import Repo

app = create_app()

with app.app_context():
    # Clear existing data
    db.session.query(Repo).delete()
    db.session.commit()

    test_repos = [
        {
            'repo_id': 1,
            'name': 'Express.js',
            'url': 'https://github.com/expressjs/express',
            'description': 'Fast, unopinionated, minimalist web framework for Node.js',
            'language': 'JavaScript',
            'topics': ['web-framework', 'nodejs', 'javascript'],
            'stars': 64000,
            'forks': 15000,
        },
        {
            'repo_id': 2,
            'name': 'Django',
            'url': 'https://github.com/django/django',
            'description': 'The Web framework for perfectionists with deadlines.',
            'language': 'Python',
            'topics': ['web-framework', 'python', 'orm'],
            'stars': 78000,
            'forks': 31000,
        },
        {
            'repo_id': 3,
            'name': 'React',
            'url': 'https://github.com/facebook/react',
            'description': 'A JavaScript library for building user interfaces with components.',
            'language': 'JavaScript',
            'topics': ['ui-library', 'javascript', 'frontend'],
            'stars': 218000,
            'forks': 45000,
        },
        {
            'repo_id': 4,
            'name': 'FastAPI',
            'url': 'https://github.com/tiangolo/fastapi',
            'description': 'Modern, fast (high-performance) web framework for building APIs',
            'language': 'Python',
            'topics': ['api-framework', 'python', 'web-framework', 'async'],
            'stars': 75000,
            'forks': 6000,
        },
        {
            'repo_id': 5,
            'name': 'Vue.js',
            'url': 'https://github.com/vuejs/vue',
            'description': 'The Progressive JavaScript Framework.',
            'language': 'JavaScript',
            'topics': ['frontend-framework', 'javascript', 'ui'],
            'stars': 208000,
            'forks': 33000,
        },
        {
            'repo_id': 6,
            'name': 'TensorFlow',
            'url': 'https://github.com/tensorflow/tensorflow',
            'description': 'An Open Source Machine Learning Framework',
            'language': 'Python',
            'topics': ['machine-learning', 'deep-learning', 'ai', 'tensorflow'],
            'stars': 185000,
            'forks': 74000,
        },
        {
            'repo_id': 7,
            'name': 'Go',
            'url': 'https://github.com/golang/go',
            'description': 'The Go programming language',
            'language': 'Go',
            'topics': ['programming-language', 'go', 'compiler'],
            'stars': 121000,
            'forks': 18000,
        },
        {
            'repo_id': 8,
            'name': 'Docker',
            'url': 'https://github.com/moby/moby',
            'description': 'Moby Project - a collaborative project for the container ecosystem',
            'language': 'Go',
            'topics': ['containers', 'docker', 'devops', 'infrastructure'],
            'stars': 68000,
            'forks': 19000,
        },
        {
            'repo_id': 9,
            'name': 'SQLAlchemy',
            'url': 'https://github.com/sqlalchemy/sqlalchemy',
            'description': 'The Python SQL Toolkit and Object Relational Mapper',
            'language': 'Python',
            'topics': ['orm', 'database', 'sql', 'python'],
            'stars': 9000,
            'forks': 1400,
        },
        {
            'repo_id': 10,
            'name': 'Kubernetes',
            'url': 'https://github.com/kubernetes/kubernetes',
            'description': 'Production-Grade Container Orchestration',
            'language': 'Go',
            'topics': ['containers', 'orchestration', 'devops', 'kubernetes'],
            'stars': 110000,
            'forks': 40000,
        },
        {
            'repo_id': 11,
            'name': 'Next.js',
            'url': 'https://github.com/vercel/next.js',
            'description': 'The React Framework for Production',
            'language': 'JavaScript',
            'topics': ['react-framework', 'javascript', 'fullstack', 'frontend'],
            'stars': 126000,
            'forks': 26000,
        },
        {
            'repo_id': 12,
            'name': 'MongoDB',
            'url': 'https://github.com/mongodb/mongo',
            'description': 'The MongoDB Database',
            'language': 'C++',
            'topics': ['database', 'nosql', 'mongodb'],
            'stars': 26000,
            'forks': 5900,
        },
        {
            'repo_id': 13,
            'name': 'PostgreSQL',
            'url': 'https://github.com/postgres/postgres',
            'description': 'The World\'s Most Advanced Open Source Relational Database',
            'language': 'C',
            'topics': ['database', 'sql', 'postgresql', 'relational'],
            'stars': 14000,
            'forks': 4200,
        },
        {
            'repo_id': 14,
            'name': 'Flask',
            'url': 'https://github.com/pallets/flask',
            'description': 'The Python micro framework for building web applications.',
            'language': 'Python',
            'topics': ['web-framework', 'python', 'microframework'],
            'stars': 68000,
            'forks': 18000,
        },
        {
            'repo_id': 15,
            'name': 'Rust',
            'url': 'https://github.com/rust-lang/rust',
            'description': 'Empowering everyone to build reliable and efficient software.',
            'language': 'Rust',
            'topics': ['programming-language', 'systems-programming', 'compiler'],
            'stars': 98000,
            'forks': 13000,
        },
    ]

    print('Seeding database with test repositories...')
    for repo_data in test_repos:
        try:
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
            print(f'[+] Added {repo_data["name"]}')
        except Exception as e:
            db.session.rollback()
            print(f'[-] Failed to add {repo_data["name"]}: {e}')

    print('Database seeding complete!')
    print(f'Total repos added: {Repo.query.count()}')
