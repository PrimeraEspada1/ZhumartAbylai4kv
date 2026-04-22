import json
import os
import sys
import urllib.error
import urllib.request


GROQ_API_KEY = "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"


if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def print_json(payload, status=200):
    print(f"Status: {status}")
    print("Content-Type: application/json; charset=utf-8")
    print()
    print(json.dumps(payload, ensure_ascii=False))


def load_request_data():
    try:
        length = int(os.environ.get("CONTENT_LENGTH", "0"))
    except ValueError:
        length = 0

    raw_body = sys.stdin.read(length) if length > 0 else ""
    if not raw_body:
        return {}

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return {}


api_key = os.environ.get("GROQ_API_KEY", "").strip() or GROQ_API_KEY
if not api_key:
    print_json(
        {
            "reply": "Чат-бот пока не настроен: не найден ключ для доступа к Groq API."
        },
        status=500,
    )
    raise SystemExit

request_data = load_request_data()
user_message = str(request_data.get("message", "")).strip()

if not user_message:
    print_json({"reply": "Напишите вопрос о ремонте, диагностике или апгрейде компьютера."}, status=400)
    raise SystemExit

system_prompt = (
    "Ты полезный консультант сайта по ремонту и обслуживанию компьютеров. "
    "Отвечай на русском языке. Давай понятные, практичные и безопасные советы по темам: "
    "перегрев, шум, синий экран, медленная работа ПК, выбор SSD, RAM, блока питания, чистка, "
    "профилактика, диагностика ноутбуков и сборок. "
    "Если проблема может привести к потере данных или риску для электроники, сначала советуй резервную копию "
    "и безопасную диагностику. Не выдумывай выполненные действия. Не обещай точный ремонт без осмотра. "
    "Структурируй ответ кратко: причина, что проверить, что сделать дальше."
)

payload = {
    "model": "llama-3.1-8b-instant",
    "temperature": 0.4,
    "max_tokens": 500,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ],
}

request = urllib.request.Request(
    "https://api.groq.com/openai/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        groq_data = json.loads(response.read().decode("utf-8"))
except urllib.error.HTTPError as error:
    error_body = error.read().decode("utf-8", errors="ignore")
    details = error_body[:400]
    try:
        parsed_error = json.loads(error_body)
        details = (
            parsed_error.get("error", {}).get("message")
            or parsed_error.get("message")
            or details
        )
    except json.JSONDecodeError:
        pass
    print_json(
        {
            "reply": "Не удалось получить ответ от AI-сервиса.",
            "details": details,
        },
        status=502,
    )
    raise SystemExit
except Exception as error:
    print_json(
        {
            "reply": "Ошибка подключения к AI-сервису.",
            "details": str(error),
        },
        status=502,
    )
    raise SystemExit

reply = (
    groq_data.get("choices", [{}])[0]
    .get("message", {})
    .get("content", "Не удалось сформировать ответ.")
    .strip()
)

print_json({"reply": reply})
