from flask import Flask, request, send_file, render_template, jsonify
import markdown, yaml, os

app = Flask (__name__)

@app.route("/")
def home():
    return render_template('/home.html')

with app.app_context():
    with open("course.yaml", 'r') as f:
        course_data = yaml.safe_load(f)

if __name__ == "__main__":
    app.run(debug=True)