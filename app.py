from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret-key-demo"  # sau này đổi

# ================== USERS ==================
USERS = [
    {"id": 1, "name": "Thầy Giới", "email": "gioi@admin", "credit": 100, "role": "admin"},
    {"id": 2, "name": "Giáo viên A", "email": "a@gv.vn", "credit": 20, "role": "user"},
    {"id": 3, "name": "Giáo viên B", "email": "b@gv.vn", "credit": 10, "role": "user"},
]

# ================== APPS ==================
APPS = [
    {"key": "tao-de-thi", "name": "Tạo đề thi", "icon": "📘", "cost": 5},
    {"key": "soan-giao-an", "name": "Soạn giáo án", "icon": "📗", "cost": 3},
    {"key": "viet-sang-kien", "name": "Viết sáng kiến", "icon": "✍️", "cost": 4},
    {"key": "tao-game", "name": "Tạo game", "icon": "🎮", "cost": 2},
]

# ================== HÀM TIỆN ÍCH ==================
def get_current_user():
    email = session.get("user_email")
    return next((u for u in USERS if u["email"] == email), None)

# ================== LOGIN ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        email = request.form.get("email")
        user = next((u for u in USERS if u["email"] == email), None)
        if user:
            session["user_email"] = user["email"]
            return redirect(url_for("dashboard"))
        else:
            message = "Email không tồn tại trong hệ thống"

    return f"""
        <h2>ĐĂNG NHẬP</h2>
        <form method="post">
            Email:
            <input name="email" required>
            <button type="submit">Đăng nhập</button>
        </form>
        <p style='color:red;'>{message or ''}</p>
    """

# ================== LOGOUT ==================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================== DASHBOARD ==================
@app.route("/")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        apps=APPS,
        user=user
    )

# ================== TRANG APP ==================
@app.route("/app/<app_key>", methods=["GET", "POST"])
def app_page(app_key):
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    app_info = next((a for a in APPS if a["key"] == app_key), None)
    if not app_info:
        return "Ứng dụng không tồn tại", 404

    message = None
    result = None

    if request.method == "POST":
        cost = app_info["cost"]

        if user["credit"] < cost:
            message = f"❌ Không đủ điểm (cần {cost} điểm)."
        else:
            user["credit"] -= cost
            content = request.form.get("content", "")
            result = f"Đã xử lý nội dung: {content}"
            message = f"✅ Đã trừ {cost} điểm. Còn lại {user['credit']} điểm."

    return render_template(
        "app_page.html",
        app=app_info,
        result=result,
        message=message,
        user=user
    )

# ================== ADMIN ==================
@app.route("/admin/users", methods=["GET", "POST"])
def admin_users():
    user = get_current_user()
    if not user or user["role"] != "admin":
        return "Không có quyền truy cập", 403

    if request.method == "POST":
        user_id = int(request.form.get("user_id"))
        change = int(request.form.get("change"))

        u = next((x for x in USERS if x["id"] == user_id), None)
        if u:
            u["credit"] += change
            if u["credit"] < 0:
                u["credit"] = 0

        return redirect(url_for("admin_users"))

    return render_template(
        "admin_users.html",
        users=USERS
    )

# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True)
