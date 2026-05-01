from flask import Blueprint, request, jsonify, send_file
from app import db
from app.database import search_repos, get_languages, get_topics, get_repo_by_id
from app.utils import download_github_repo
from app.semantic_search import SemanticSearchEngine
import os
import io

bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize semantic search (lazy loaded only if needed)
_semantic_search_engine = None

def get_semantic_search():
    global _semantic_search_engine
    if _semantic_search_engine is None:
        try:
            _semantic_search_engine = SemanticSearchEngine()
        except Exception as e:
            return None
    return _semantic_search_engine

@bp.route('/search', methods=['GET'])
def search():
    """
    Search repositories by keyword with optional language and topic filters.
    Query params:
      - query: keyword search term (required)
      - language: filter by programming language (optional)
      - topic: filter by topic/category (optional)
      - limit: number of results (default: 5)
      - semantic: use semantic search instead of keyword matching (default: false)
    """
    query = request.args.get('query', '')
    language = request.args.get('language')
    topic = request.args.get('topic')
    limit = request.args.get('limit', 5, type=int)
    use_semantic = request.args.get('semantic', 'false').lower() == 'true'

    if not query:
        return jsonify({'error': 'query parameter is required'}), 400

    # Use semantic search if requested
    if use_semantic:
        semantic_engine = get_semantic_search()
        if semantic_engine is None:
            return jsonify({
                'error': 'Semantic search not available. Please configure an embeddings provider.'
            }), 503

        try:
            results = semantic_engine.search(query, language, topic, limit)
            return jsonify({'repos': results})
        except Exception as e:
            return jsonify({'error': f'Semantic search error: {str(e)}'}), 500

    # Use keyword search (default)
    results = search_repos(query, language, topic, limit)
    return jsonify({'repos': results})

@bp.route('/languages', methods=['GET'])
def languages():
    """Get all available programming languages."""
    langs = get_languages()
    return jsonify({'languages': langs})

@bp.route('/topics', methods=['GET'])
def topics():
    """Get all available topics/categories."""
    topics_list = get_topics()
    return jsonify({'topics': topics_list})

@bp.route('/repos/<int:repo_id>/download', methods=['POST'])
def download_repo(repo_id):
    """
    Download a repository as a ZIP file.
    The repo must exist in the database.
    """
    repo = get_repo_by_id(repo_id)
    if not repo:
        return jsonify({'error': 'Repository not found'}), 404

    try:
        zip_buffer = download_github_repo(repo.url)
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{repo.name}.zip'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/config', methods=['GET'])
def config():
    """
    Get configuration information about the search service.
    Returns available search modes and embedding providers.
    """
    embeddings_provider = os.getenv('EMBEDDINGS_PROVIDER', 'openai').lower()
    semantic_available = get_semantic_search() is not None

    config_info = {
        'search_modes': {
            'keyword': {
                'available': True,
                'description': 'Fast keyword matching search'
            },
            'semantic': {
                'available': semantic_available,
                'description': 'Semantic search using embeddings',
                'provider': embeddings_provider if semantic_available else None,
                'reason': None if semantic_available else 'Embeddings provider not configured'
            }
        },
        'embeddings_providers': {
            'openai': {
                'name': 'OpenAI',
                'description': 'Uses OpenAI API (requires API key)',
                'env_vars': ['OPENAI_API_KEY'],
                'installation': 'pip install openai'
            },
            'ollama': {
                'name': 'Ollama',
                'description': 'Local embeddings using Ollama',
                'env_vars': ['OLLAMA_BASE_URL', 'OLLAMA_MODEL'],
                'installation': 'Download from ollama.ai',
                'default_model': 'nomic-embed-text'
            },
            'local': {
                'name': 'Local (sentence-transformers)',
                'description': 'Local embeddings using sentence-transformers',
                'env_vars': ['LOCAL_EMBEDDINGS_MODEL'],
                'installation': 'pip install sentence-transformers',
                'default_model': 'all-MiniLM-L6-v2'
            }
        }
    }

    return jsonify(config_info)

def register_blueprints(app):
    app.register_blueprint(bp)
