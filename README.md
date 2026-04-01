# FinAgent - Browser Action Agent

A production-grade browser automation agent with Python backend and FastAPI.

## Project Structure

- `backend/` - FastAPI application with Playwright automation
- `bank_website/` - Dummy bank website for testing
- `docs/` - Documentation
- `scripts/` - Utility scripts

## Setup

1. Create virtual environment
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Install Playwright browsers: `playwright install`
4. Copy `.env.example` to `.env` and configure
5. Start bank website server
6. Start FastAPI backend

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.
