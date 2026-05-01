import requests
import io
import zipfile
from urllib.parse import urlparse

def download_github_repo(github_url):
    """
    Download a GitHub repository as a ZIP file.
    Takes a GitHub URL like https://github.com/owner/repo
    Returns a BytesIO object containing the ZIP file.
    """
    parsed = urlparse(github_url)
    path_parts = parsed.path.strip('/').split('/')

    if len(path_parts) < 2:
        raise ValueError('Invalid GitHub URL')

    owner = path_parts[0]
    repo = path_parts[1].replace('.git', '')

    zip_url = f'https://api.github.com/repos/{owner}/{repo}/zipball/main'

    try:
        response = requests.get(zip_url, timeout=30)
        if response.status_code == 404:
            zip_url = f'https://api.github.com/repos/{owner}/{repo}/zipball/master'
            response = requests.get(zip_url, timeout=30)

        if response.status_code != 200:
            raise Exception(f'Failed to download repo: HTTP {response.status_code}')

        return io.BytesIO(response.content)

    except requests.RequestException as e:
        raise Exception(f'Failed to download repository: {str(e)}')
