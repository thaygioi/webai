from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ================== ADMIN CỐ ĐỊNH ==================
ADMIN_EMAIL = "gioi@admin"

# ================== USERS GIẢ LẬP ==================
USERS = [
    {"id": 1, "name": "Giáo viên A", "email": "a@gv.vn", "credit": 20},
    {"id": 2, "name": "Giáo viên B", "email": "b@gv.vn", "credit": 10},
]

# User đang đăng nhập (giả lập)
CURRENT_USER = USERS[0]  # Giáo viên A

# ================== APPS ==================
APPS = [
    {"key": "tao-de-thi", "name": "Tạo đề thi", "icon": "📘", "cost": 5},
    {"key": "soan-giao-an", "name": "Soạn giáo án", "icon": "📗", "cost": 3},
    {"key": "viet-sang-kien", "name": "Viết sáng kiến", "icon": "✍️", "cost": 4},
    {"key": "tao-game", "name": "Tạo game", "icon": "🎮", "cost": 2},
]

# ================== DASHBOARD ==================
@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        apps=APPS,
        user=CURRENT_USER
    )

# ================== TRANG APP ==================
@app.route("/app/<app_key>", methods=["GET", "POST"])
def app_page(app_key):
    app_info = next((a for a in APPS if a["key"] == app_key), None)
    if not app_info:
        return "Ứng dụng không tồn tại", 404

    message = None
    result = None

    if request.method == "POST":
        cost = app_info["cost"]

        if CURRENT_USER["credit"] < cost:
            message = f"❌ Không đủ điểm (cần {cost} điểm)."
        else:
            CURRENT_USER["credit"] -= cost
            user_input = request.form.get("content", "")
            result = f"Đã xử lý nội dung: {user_input}"
            message = f"✅ Đã trừ {cost} điểm. Còn lại {CURRENT_USER['credit']} điểm."

    return render_template(
        "app_page.html",
        app=app_info,
        result=result,
        message=message,
        user=CURRENT_USER
    )

# ================== ADMIN - QUẢN LÝ USER ==================
@app.route("/admin/users", methods=["GET", "POST"])
def admin_users():
    # Kiểm tra admin (giai đoạn này dùng giả lập)
    if CURRENT_USER["email"] != USERS[0]["email"]:
        return "Không có quyền truy cập", 403

    if request.method == "POST":
        user_id = int(request.form.get("user_id"))
        change = int(request.form.get("change"))

        user = next((u for u in USERS if u["id"] == user_id), None)
        if user:
            user["credit"] += change
            if user["credit"] < 0:
                user["credit"] = 0

        return redirect(url_for("admin_users"))

    # GIAO DIỆN TEXT ĐƠN GIẢN
    html = "<h2>TRANG QUẢN TRỊ – QUẢN LÝ NGƯỜI DÙNG</h2>"
    html += "<p><b>Admin:</b> Thầy Giới</p><hr>"

    for u in USERS:
        html += f"""
        <form method="post" style="margin-bottom:15px;">
            <b>{u['name']}</b> ({u['email']})<br>
            Điểm hiện có: <b>{u['credit']}</b><br>
            <input type="hidden" name="user_id" value="{u['id']}">
            Cộng / trừ điểm:
            <input type="number" name="change" value="0">
            <button type="submit">Cập nhật</button>
        </form>
        <hr>
        """

    return html

# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True)
