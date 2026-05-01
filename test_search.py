#!/usr/bin/env python
"""Test script for search functionality."""

import sys
import requests
from app import create_app

BASE_URL = "http://localhost:5000/api"

def test_keyword_search():
    """Test keyword search."""
    print("\n=== Testing Keyword Search ===")
    try:
        response = requests.get(f"{BASE_URL}/search?query=web")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Results: {len(data['repos'])} repos found")
        if data['repos']:
            for repo in data['repos'][:2]:
                print(f"  - {repo['name']} ({repo['language']}) - {repo['stars']} stars")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_language_filter():
    """Test language filtering."""
    print("\n=== Testing Language Filter ===")
    try:
        response = requests.get(f"{BASE_URL}/search?query=web&language=Python")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Results: {len(data['repos'])} Python repos found")
        if data['repos']:
            for repo in data['repos'][:2]:
                print(f"  - {repo['name']} ({repo['language']})")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_topic_filter():
    """Test topic filtering."""
    print("\n=== Testing Topic Filter ===")
    try:
        response = requests.get(f"{BASE_URL}/search?query=&topic=web-framework")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Results: {len(data.get('repos', []))} repos with web-framework topic")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_languages():
    """Test getting available languages."""
    print("\n=== Testing Get Languages ===")
    try:
        response = requests.get(f"{BASE_URL}/languages")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Languages: {', '.join(data['languages'])}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_topics():
    """Test getting available topics."""
    print("\n=== Testing Get Topics ===")
    try:
        response = requests.get(f"{BASE_URL}/topics")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Topics: {', '.join(data['topics'][:10])}...")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_config():
    """Test getting configuration."""
    print("\n=== Testing Configuration Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/config")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Search modes:")
        for mode, info in data['search_modes'].items():
            status = "✓" if info['available'] else "✗"
            print(f"  {status} {mode}: {info['description']}")
            if mode == 'semantic' and not info['available']:
                print(f"    → {info['reason']}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_semantic_search():
    """Test semantic search (if available)."""
    print("\n=== Testing Semantic Search ===")
    try:
        response = requests.get(f"{BASE_URL}/search?query=web&semantic=true")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Results: {len(data['repos'])} repos found")
            if data['repos']:
                for repo in data['repos'][:2]:
                    print(f"  - {repo['name']} ({repo['language']})")
            return True
        elif response.status_code == 503:
            print(f"Semantic search not available (provider not configured)")
            return True
        else:
            print(f"Error: {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("GitHub Discovery Tool - Search Tests")
    print("=" * 50)

    # Check if server is running
    try:
        requests.get(BASE_URL, timeout=2)
    except:
        print("\n❌ Flask server is not running!")
        print("Start it with: python run.py")
        sys.exit(1)

    print("\n✓ Flask server is running")

    results = []
    results.append(("Keyword Search", test_keyword_search()))
    results.append(("Language Filter", test_language_filter()))
    results.append(("Topic Filter", test_topic_filter()))
    results.append(("Get Languages", test_languages()))
    results.append(("Get Topics", test_topics()))
    results.append(("Configuration", test_config()))
    results.append(("Semantic Search", test_semantic_search()))

    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
