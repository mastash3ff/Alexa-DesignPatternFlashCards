# Design Pattern Flash Cards

![Deploy](https://github.com/mastash3ff/Alexa-DesignPatternFlashCards/actions/workflows/deploy.yml/badge.svg)

An Alexa flash card game covering all 23 Gang of Four design patterns. Alexa reads a pattern definition; you name the pattern.

## Usage

**Invocation:** `design pattern flash cards`

| Say... | Response |
|--------|----------|
| "Alexa, open design pattern flash cards" | Starts a shuffled run through all 23 patterns |
| The pattern name (e.g. "Abstract Factory") | Marks correct or incorrect, advances to next card |
| "I don't know" | Reveals the answer and advances |
| "Repeat" | Re-reads the current definition |
| "Start over" | Reshuffles and restarts from card 1 |
| "Help" | Explains how to play |
| "Stop" / "Exit" | Ends the skill |

## How to play

Alexa reads a GoF pattern definition. Say the pattern name to answer. All 23 patterns are presented in random order. Your score is announced when the last card is reached.

## Development

**Stack:** Python 3.12 · ASK SDK v2 · AWS Lambda (us-east-1)

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
PYTHONPATH=. pytest tests/ -v

# Deploy — automatic on push to master via GitHub Actions
```

## Project structure

```
lambda_function.py      Intent handlers and game logic
data.py                 Pattern bank (all 23 GoF patterns)
requirements.txt        ask-sdk-core dependency
tests/test_skill.py     Unit tests
.github/workflows/      CI/CD — tests gate deployment to Lambda
```
