import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Union


BASE_URL = "https://agents-course-unit4-scoring.hf.space"

# Prompt that forces answer-only output to match the exact-match scorer.
EXACT_MATCH_PROMPT = (
    "You are solving a GAIA evaluation task. Return only the final answer text with no prefix, "
    "no explanation, and no extra words. Do not include the phrase FINAL ANSWER."
)


def _request_json(method: str, path: str, payload: Dict[str, Any] | None = None) -> Any:
    url = urllib.parse.urljoin(BASE_URL, path)
    data = None
    headers = {"Accept": "application/json"}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url=url, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code} for {method} {path}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error for {method} {path}: {exc}") from exc


def get_questions() -> List[Dict[str, Any]]:
    return _request_json("GET", "/questions")


def get_random_question() -> Dict[str, Any]:
    return _request_json("GET", "/random-question")


def download_task_file(task_id: str, output_path: pathlib.Path) -> pathlib.Path:
    path = f"/files/{urllib.parse.quote(task_id)}"
    url = urllib.parse.urljoin(BASE_URL, path)

    request = urllib.request.Request(url=url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code} for GET {path}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error for GET {path}: {exc}") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)
    return output_path


def normalize_agent_answer(answer: Union[str, int, float]) -> Union[str, int, float]:
    if isinstance(answer, (int, float)):
        return answer

    cleaned = answer.strip()
    cleaned = re.sub(r"^\s*final\s*answer\s*:\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned


def load_answers_file(path: pathlib.Path) -> List[Dict[str, Union[str, int, float]]]:
    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        answers = [
            {"task_id": task_id, "submitted_answer": normalize_agent_answer(value)}
            for task_id, value in data.items()
        ]
        return answers

    if isinstance(data, list):
        normalized: List[Dict[str, Union[str, int, float]]] = []
        for item in data:
            if not isinstance(item, dict) or "task_id" not in item or "submitted_answer" not in item:
                raise ValueError(
                    "Each item in a list-based answers file must include task_id and submitted_answer"
                )
            normalized.append(
                {
                    "task_id": str(item["task_id"]),
                    "submitted_answer": normalize_agent_answer(item["submitted_answer"]),
                }
            )
        return normalized

    raise ValueError("Answers JSON must be either an object mapping task_id->answer or a list of answer items")


def submit_answers(username: str, agent_code: str, answers: List[Dict[str, Union[str, int, float]]]) -> Dict[str, Any]:
    payload = {
        "username": username,
        "agent_code": agent_code,
        "answers": answers,
    }
    return _request_json("POST", "/submit", payload)


def answer_random_question_with_agent() -> Dict[str, Union[str, Dict[str, Any]]]:
    # Import here so fetch/submit commands can run without smolagents installed.
    from agent import run_agent

    question = get_random_question()
    task_id = str(question.get("task_id", ""))
    if not task_id:
        raise RuntimeError("Random question payload does not contain task_id")

    task_text = question.get("question", json.dumps(question, ensure_ascii=True))
    prompt = f"{EXACT_MATCH_PROMPT}\n\nTask ID: {task_id}\nQuestion: {task_text}"
    answer = normalize_agent_answer(run_agent(prompt))

    return {
        "question": question,
        "answer": {"task_id": task_id, "submitted_answer": answer},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GAIA scoring API helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("questions", help="Fetch all filtered questions")
    subparsers.add_parser("random", help="Fetch one random question")

    file_parser = subparsers.add_parser("file", help="Download file for a task_id")
    file_parser.add_argument("task_id", help="Task ID whose file should be downloaded")
    file_parser.add_argument(
        "--output",
        required=True,
        help="Output file path, for example Project/data/task_file.bin",
    )

    submit_parser = subparsers.add_parser("submit", help="Submit answers JSON to /submit")
    submit_parser.add_argument("--username", required=True, help="Hugging Face username")
    submit_parser.add_argument(
        "--agent-code-path",
        required=True,
        help="Path to the Python file containing your agent code",
    )
    submit_parser.add_argument(
        "--answers-path",
        required=True,
        help="Path to answers JSON (dict task_id->answer OR list of {task_id, submitted_answer})",
    )

    solve_parser = subparsers.add_parser("solve-random", help="Use your local agent to answer one random question")
    solve_parser.add_argument(
        "--save",
        default=None,
        help="Optional file path to save the generated answer item as JSON",
    )

    solve_submit_parser = subparsers.add_parser(
        "solve-random-and-submit",
        help="Answer one random question with your agent and submit immediately",
    )
    solve_submit_parser.add_argument("--username", required=True, help="Hugging Face username")
    solve_submit_parser.add_argument(
        "--agent-code-path",
        required=True,
        help="Path to the Python file containing your agent code",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.command == "questions":
            print(json.dumps(get_questions(), indent=2, ensure_ascii=False))
            return 0

        if args.command == "random":
            print(json.dumps(get_random_question(), indent=2, ensure_ascii=False))
            return 0

        if args.command == "file":
            output = download_task_file(args.task_id, pathlib.Path(args.output))
            print(f"Downloaded to: {output}")
            return 0

        if args.command == "submit":
            agent_code = pathlib.Path(args.agent_code_path).read_text(encoding="utf-8")
            answers = load_answers_file(pathlib.Path(args.answers_path))
            response = submit_answers(args.username, agent_code, answers)
            print(json.dumps(response, indent=2, ensure_ascii=False))
            return 0

        if args.command == "solve-random":
            result = answer_random_question_with_agent()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            if args.save:
                pathlib.Path(args.save).write_text(
                    json.dumps(result["answer"], indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                print(f"Saved answer to: {args.save}")
            return 0

        if args.command == "solve-random-and-submit":
            result = answer_random_question_with_agent()
            agent_code = pathlib.Path(args.agent_code_path).read_text(encoding="utf-8")
            response = submit_answers(args.username, agent_code, [result["answer"]])
            print(json.dumps({"generated": result, "submission": response}, indent=2, ensure_ascii=False))
            return 0

    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
