from flask import Flask, render_template, request

app = Flask(__name__)

APPS = [
    {"key": "tao-de-thi", "name": "Tạo đề thi", "icon": "📘"},
    {"key": "soan-giao-an", "name": "Soạn giáo án", "icon": "📗"},
    {"key": "viet-sang-kien", "name": "Viết sáng kiến", "icon": "✍️"},
    {"key": "tao-game", "name": "Tạo game", "icon": "🎮"},
]

@app.route("/")
def dashboard():
    return render_template("dashboard.html", apps=APPS)

@app.route("/app/<app_key>", methods=["GET", "POST"])
def app_page(app_key):
    app_info = next((a for a in APPS if a["key"] == app_key), None)
    if not app_info:
        return "Ứng dụng không tồn tại", 404

    result = None
    if request.method == "POST":
        user_input = request.form.get("content", "")
        result = f"Bạn đã nhập: {user_input}"

    return render_template("app_page.html", app=app_info, result=result)

if __name__ == "__main__":
    app.run(debug=True)
