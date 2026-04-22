import cgi
import html
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

print("Content-type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()

raw_n1 = form.getvalue("num1", form.getvalue("n1", "0"))
raw_n2 = form.getvalue("num2", form.getvalue("n2", "0"))

try:
    n1 = int(raw_n1)
    n2 = int(raw_n2)
    result = n1 + n2
    message = f"{n1} + {n2} = {result}"
    status = "Расчёт выполнен"
except (TypeError, ValueError):
    n1 = html.escape(str(raw_n1))
    n2 = html.escape(str(raw_n2))
    message = f"Не удалось сложить значения: {n1} и {n2}."
    status = "Ошибка ввода"

print(
    f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Результат расчёта</title>
    <style>
        body {{
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            font-family: "Trebuchet MS", "Segoe UI", sans-serif;
            background: linear-gradient(180deg, #fff8ec 0%, #f4ecdd 100%);
            color: #1f2933;
        }}
        .card {{
            width: min(520px, calc(100% - 32px));
            padding: 32px;
            border-radius: 28px;
            background: rgba(255, 251, 245, 0.92);
            border: 1px solid rgba(104, 84, 55, 0.16);
            box-shadow: 0 22px 50px rgba(76, 53, 31, 0.14);
        }}
        .eyebrow {{
            margin: 0 0 8px;
            color: #b95c2e;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.75rem;
            font-weight: 700;
        }}
        h1 {{ margin: 0 0 14px; }}
        p {{ color: #5d6a74; line-height: 1.6; }}
        a {{
            display: inline-block;
            margin-top: 16px;
            padding: 12px 18px;
            border-radius: 16px;
            background: linear-gradient(135deg, #b95c2e, #d18147);
            color: #fff;
            text-decoration: none;
            font-weight: 700;
        }}
    </style>
</head>
<body>
    <div class="card">
        <p class="eyebrow">{status}</p>
        <h1>Калькулятор стоимости</h1>
        <p>{message}</p>
        <a href="/index.html">Вернуться на главную</a>
    </div>
</body>
</html>"""
)
