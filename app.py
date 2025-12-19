from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    apps = [
        {"name": "Tạo đề thi", "icon": "📘"},
        {"name": "Soạn giáo án", "icon": "📗"},
        {"name": "Viết sáng kiến", "icon": "✍️"},
        {"name": "Tạo game", "icon": "🎮"},
    ]
    return render_template("dashboard.html", apps=apps)

if __name__ == "__main__":
    app.run()
