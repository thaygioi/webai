from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Web AI của tôi đã chạy thành công 🚀"

if __name__ == "__main__":
    app.run()
