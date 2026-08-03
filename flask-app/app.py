from flask import Flask, send_file, render_template, url_for
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

    file_path = os.path.join(base_dir, 'content', 'chapters', current_chapter['file'])
    with open(file_path, 'r') as f:
        content = markdown.markdown(f.read(), extensions=['tables', 'fenced_code', 'codehilite'])

    all_chapters = []
    for section in course_data['sections']:
        for chapter in section['chapters']:
            all_chapters.append(chapter)

    index = all_chapters.index(current_chapter)

    # Previous URL
    if index == 0:
        prev_url = None
        prev_label = None
    else:
        prev_chapter = all_chapters[index - 1]
        if prev_chapter.get('has_lab'):
            prev_url = url_for('show_lab', chapter_number=prev_chapter['chapter_number'])
            prev_label = f"Lab {prev_chapter['chapter_number']}: {prev_chapter['title']}"
        else:
            prev_url = url_for('show_chapter', chapter_number=prev_chapter['chapter_number'])
            prev_label = prev_chapter['title']

    # Next URL
    if current_chapter.get('has_lab'):
        next_url = url_for('show_lab', chapter_number=current_chapter['chapter_number'])
        next_label = f"Lab {current_chapter['chapter_number']}: {current_chapter['title']}"
    elif index < len(all_chapters) - 1:
        next_chapter = all_chapters[index + 1]
        next_url = url_for('show_chapter', chapter_number=next_chapter['chapter_number'])
        next_label = next_chapter['title']
    else:
        next_url = None
        next_label = None

    return render_template('chapter.html',
        chapter=current_chapter,
        content=content,
        prev_url=prev_url,
        prev_label=prev_label,
        next_url=next_url,
        next_label=next_label)

@app.route('/lab/<int:chapter_number>')
def show_lab(chapter_number):
    current_lab = None
    for section in course_data['sections']:
        for chapter in section['chapters']:
            if chapter.get('has_lab') and chapter['chapter_number'] == chapter_number:
                current_lab = chapter
    if current_lab is None:
        return "Lab not found", 404

    file_path = os.path.join(base_dir, 'content', 'labs', current_lab['lab_file'])
    with open(file_path, 'r') as f:
        content = markdown.markdown(f.read(), extensions=['tables', 'fenced_code', 'codehilite'])

    all_chapters = []
    for section in course_data['sections']:
        for chapter in section['chapters']:
            all_chapters.append(chapter)

    index = all_chapters.index(current_lab)

    prev_url = url_for('show_chapter', chapter_number=current_lab['chapter_number'])
    prev_label = current_lab['title']

    if index < len(all_chapters) - 1:
        next_chapter = all_chapters[index + 1]
        next_url = url_for('show_chapter', chapter_number=next_chapter['chapter_number'])
        next_label = next_chapter['title']
    else:
        next_url = None
        next_label = None

    return render_template('lab.html',
        current_lab=current_lab,
        content=content,
        prev_url=prev_url,
        prev_label=prev_label,
        next_url=next_url,
        next_label=next_label)

@app.route('/grade/<int:lab_number>')
def grade_lab_route(lab_number):
    from grading.grade_lab import grade_lab
    result = grade_lab(lab_number)
    if result is None:
        return "Grading Failed", 500
    return render_template('results.html', result=result, lab_number=lab_number)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)