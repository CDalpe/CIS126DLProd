from flask import Flask, send_file, render_template
import markdown, yaml, os

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template('/home.html')

with app.app_context():
    with open("course.yaml", 'r') as f:
        course_data = yaml.safe_load(f)

if __name__ == "__main__":
    app.run(debug=True)