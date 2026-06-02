from flask import Flask, send_file, render_template
import markdown, yaml, os

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

course_data = None
with app.app_context():
    with open(os.path.join(base_dir, 'course.yaml'), 'r') as f:
        course_data = yaml.safe_load(f)

@app.context_processor
def inject_course_data():
    return {'course': course_data}

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/chapter/<int:chapter_number>')
def show_chapter(chapter_number):
    current_chapter = None
    for section in course_data['sections']:
        for chapter in section['chapters']:
            if chapter['chapter_number'] == chapter_number:
                current_chapter = chapter
    if current_chapter is None:
        return "Chapter not found", 404
        ##TODO Write a handling page for this
    file_path = os.path.join(base_dir, 'content', 'chapters', current_chapter['file'])
    with open(file_path, 'r') as f:
        content = markdown.markdown(f.read(), extensions=['tables'])
    all_chapters = []
    for section in course_data['sections']:
        for chapter in section['chapters']:
            all_chapters.append(chapter)
    index = all_chapters.index(current_chapter)
    prev_chapter = all_chapters[index - 1] if index > 0 else None
    next_chapter = all_chapters[index + 1] if index < len(all_chapters) - 1 else None
    return render_template('chapter.html', chapter=current_chapter, content=content, prev_chapter=prev_chapter, next_chapter=next_chapter)

@app.route('/lab/<int:chapter_number>')
def show_lab(chapter_number):
    current_lab = None
    for section in course_data['sections']:
        for chapter in section['chapters']:
            if chapter.get('has_lab') and chapter['chapter_number'] == chapter_number:
                current_lab = chapter
    if current_lab is None:
        return "Lab not Found", 404
        ##TODO Write a handling page for this
    file_path = os.path.join(base_dir, 'content', 'labs', current_lab['lab_file'])
    with open(file_path, 'r') as f:
        content = markdown.markdown(f.read(), extensions=['tables'])
    return render_template('lab.html', content=content, current_lab=current_lab)
        
if __name__ == "__main__":
    app.run(debug=True)