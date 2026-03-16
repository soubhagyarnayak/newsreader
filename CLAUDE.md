# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python application that fetches, parses, and indexes news articles and web content for personal use. Sources include Hacker News, RSS feeds (with Times of India blog support), and Odia-language newspapers (Samaja, Dharitri).

## Architecture

**Message-driven**: `task_processor.py` is the main entry point. It listens on a RabbitMQ queue named `newsparser` and dispatches to handlers based on message content:
- `processHN` → `HackerNewsManager`
- `processOpEd` → `OpEdManager`
- `archive` → `Archiver`
- `purgeHN` → `HackerNewsManager.purge()`

**Storage**: PostgreSQL in production (configured in `config.py`), SQLite for tests.

**Key module responsibilities**:
- `pika_consumer.py` — RabbitMQ async consumer with auto-reconnect
- `hacker_news_parser.py` / `hacker_news_store.py` — scrape HN, persist with conflict handling
- `feed_fetcher.py` — generic RSS (lxml) and HTML (BeautifulSoup) fetching with tenacity retry
- `custom_feed_fetcher.py` / `custom_fetcher.py` — site-specific scrapers (TOI blogs, Odia newspapers)
- `oped_store.py` — category-based article storage
- `archiver.py` — date-organized archiving of newspaper pages
- `text_analyzer.py` — **stub only**, pending a gensim replacement

## Development Setup

**macOS prerequisites** (from README):
```bash
brew install postgresql curl-openssl openssl@1.1
export PATH="/usr/local/opt/curl-openssl/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"
export PKG_CONFIG_PATH="/usr/local/opt/openssl@1.1/lib/pkgconfig"
pip install -r requirements.txt
```

**Ubuntu prerequisites**:
```bash
sudo apt-get install libpq-dev libcurl4-openssl-dev libssl-dev
pip install -r requirements.txt
```

## Commands

**Run tests**:
```bash
pytest tests/
```

**Run a single test**:
```bash
pytest tests/test_feed_manager.py::TestFeedManager::test_add_feed
```

**Lint**:
```bash
flake8 --select=E9,F63,F7,F82 newsparser/
```

**Build Docker image**:
```bash
docker build -t newsreader .
```

**Run (Docker)**:
```bash
docker run newsreader
```

## Configuration

`newsparser/config.py` holds database credentials and the RabbitMQ connection string. The tests use SQLite via in-memory configuration — see `tests/context.py` for how the test path is set up and `tests/test_feed_manager.py` for the SQLite fixture pattern used in tests.

## Known Incomplete Areas

- `text_analyzer.py` methods (`get_summary`, `get_keywords`) are stubs — gensim was removed and has not been replaced.
- `custom_fetcher.py` contains `SambadaFetcher` which is unimplemented.
