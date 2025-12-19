from flask import Flask, render_template, request

app = Flask(__name__)

# ====== USER GIẢ LẬP (TEST LOGIC) ======
CURRENT_USER = {
    "id": 1,
    "name": "Giáo viên A",
    "credit": 20   # số điểm hiện có
}

# ====== DANH SÁCH ỨNG DỤNG ======
APPS = [
    {"key": "tao-de-thi", "name": "Tạo đề thi", "icon": "📘", "cost": 5},
    {"key": "soan-giao-an", "name": "Soạn giáo án", "icon": "📗", "cost": 3},
    {"key": "viet-sang-kien", "name": "Viết sáng kiến", "icon": "✍️", "cost": 4},
    {"key": "tao-game", "name": "Tạo game", "icon": "🎮", "cost": 2},
]

# ====== DASHBOARD ======
@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        apps=APPS,
        user=CURRENT_USER
    )

# ====== TRANG APP ======
@app.route("/app/<app_key>", methods=["GET", "POST"])
def app_page(app_key):
    app_info = next((a for a in APPS if a["key"] == app_key), None)
    if not app_info:
        return "Ứng dụng không tồn tại", 404

    message = None
    result = None

    # ====== CHỈ KHI BẤM NÚT "TẠO" ======
    if request.method == "POST":
        cost = app_info["cost"]

        # 1. Kiểm tra đủ điểm không
        if CURRENT_USER["credit"] < cost:
            message = f"❌ Không đủ điểm. Cần {cost} điểm để sử dụng."
        else:
            # 2. TRỪ ĐIỂM (CHỈ Ở ĐÂY)
            CURRENT_USER["credit"] -= cost

            # 3. XỬ LÝ NỘI DUNG (TẠM THỜI CHƯA GẮN AI)
            user_input = request.form.get("content", "")
            result = f"Nội dung đã xử lý: {user_input}"

            message = f"✅ Đã trừ {cost} điểm. Điểm còn lại: {CURRENT_USER['credit']}"

    return render_template(
        "app_page.html",
        app=app_info,
        result=result,
        message=message,
        user=CURRENT_USER
    )

if __name__ == "__main__":
    app.run(debug=True)
