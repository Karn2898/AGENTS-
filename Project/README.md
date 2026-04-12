# Project Agent

This folder contains a small smolagents-based web search agent.

## Files

- `agent.py`: runnable web research agent template

## Run

Set the model configuration if needed:

- `SMOLAGENTS_MODEL_ID`
- `SMOLAGENTS_PROVIDER`
- `SMOLAGENTS_MAX_TOKENS`
- `SMOLAGENTS_MAX_STEPS`
- `SMOLAGENTS_VERBOSITY`

Example:

```bash
python Project/agent.py "Find three recent AI agent frameworks and summarize them"
```

If you run it without arguments, it uses a default web research prompt.
