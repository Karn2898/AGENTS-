# Project Agent

This folder contains a small smolagents-based web search agent.

It now also includes a GAIA scoring API helper that supports all required routes:

- `GET /questions`
- `GET /random-question`
- `GET /files/{task_id}`
- `POST /submit`

## Files

- `agent.py`: runnable web research agent template
- `gaia_api.py`: helper CLI to fetch questions/files and submit answers

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

With extra context:

```bash
python Project/agent.py "Compare two search libraries" --context "Focus on Python support and maintenance activity"
```

If you run it without arguments, it uses a default web research prompt.

## GAIA Scoring API Workflow

Base API docs:

- https://agents-course-unit4-scoring.hf.space/docs

### 1) Fetch Questions

```bash
python Project/gaia_api.py questions
```

Fetch one random question:

```bash
python Project/gaia_api.py random
```

### 2) Download Task File

```bash
python Project/gaia_api.py file <task_id> --output Project/data/<task_id>_file.bin
```

### 3) Submit Answers

Create an answers JSON file in either format:

```json
{
	"task_001": "answer text",
	"task_002": 42
}
```

or

```json
[
	{"task_id": "task_001", "submitted_answer": "answer text"},
	{"task_id": "task_002", "submitted_answer": 42}
]
```

Submit it:

```bash
python Project/gaia_api.py submit \
	--username <your_hf_username> \
	--agent-code-path Project/agent.py \
	--answers-path Project/answers.json
```

### 4) Optional: Auto-answer One Random Question with Local Agent

```bash
python Project/gaia_api.py solve-random
```

Answer and submit in one step:

```bash
python Project/gaia_api.py solve-random-and-submit \
	--username <your_hf_username> \
	--agent-code-path Project/agent.py
```

## Exact-Match Submission Note

The scorer compares answers in exact-match mode. The helper strips a leading `FINAL ANSWER:` prefix if present, but you should still prompt your agent to output only the answer text and nothing else.
