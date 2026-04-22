import cgi
import math
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

print("Content-type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()

d = float(form.getvalue("dist", 0))
w = float(form.getvalue("width", 1))
a = float(form.getvalue("a_const", 0.2))
b_f = float(form.getvalue("b_fitts", 0.1))
n = int(form.getvalue("n_options", 1))
b_h = float(form.getvalue("b_hick", 0.15))

fitts_time = a + b_f * math.log2(d / w + 1)
hick_time = b_h * math.log2(n + 1)

print(
    f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Результаты HCI-расчёта</title>
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
            width: min(620px, calc(100% - 32px));
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
        .result {{
            padding: 18px;
            margin-top: 14px;
            border-radius: 18px;
            background: #fffdfa;
            border: 1px solid rgba(104, 84, 55, 0.16);
        }}
        p {{ color: #5d6a74; line-height: 1.6; }}
        a {{
            display: inline-block;
            margin-top: 18px;
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
        <p class="eyebrow">HCI-аналитика</p>
        <h1>Результаты расчёта</h1>
        <div class="result">
            <p><strong>Закон Фиттса:</strong> {fitts_time:.4f} сек.</p>
            <p><strong>Закон Хика:</strong> {hick_time:.4f} сек.</p>
        </div>
        <a href="/practice3.html">Вернуться к диагностике</a>
    </div>
</body>
</html>"""
)
