from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from django.apps import AppConfig
import os

app = Flask(__name__)

# SQLite 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///problems.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 고유 ID
    title = db.Column(db.String(100), nullable=False)   # 문제 제목
    description = db.Column(db.Text, nullable=False) #문제 설명
    options = db.Column(db.Text, nullable=True) # 선택지 (콤마로 구분된 문자열)
    image_path = db.Column(db.String(200), nullable=True) # 이미지 경로
    category = db.Column(db.String(50), nullable=False)  # 카테고리
    difficulty = db.Column(db.String(20), nullable=False) # 난이도(쉬움/중간/어려움)
    tags = db.Column(db.String(200), nullable=True) # 태그 (쉼표로 구분)

# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # 문제 목록 가져오기
    problems = Problem.query.all() # 데이터베이스에서 문제 목록 가져오기
    return render_template('user_problem.html', problems=problems)


@app.route('/upload', methods=['POST'])
def upload_problem():
    title = request.form['title']
    description = request.form['description']
    options = request.form.getlist('options')
    category = request.form['category']
    difficulty = request.form['difficulty']
    tags = request.form['tags']

    # 이미지 파일 저장
    image_file = request.files.get('image')
    image_path = None
    if image_file:
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_filename)
        image_path = image_filename

    # 선택지를 텍스트로 변환 (최대 4개)
    options_text = ", ".join(options[:4])

    # 새로운 문제 데이터베이스에 저장
    new_problem = Problem(
        title=title,
        description=description,
        options=options_text,
        image_path=image_path,
        category=category,
        difficulty=difficulty,
        tags=tags
    )
    db.session.add(new_problem)
    db.session.commit()

    return jsonify({"message": "문제가 성공적으로 업로드되었습니다.", "problem_id": new_problem.id}), 201

# 업로드된 문제 목록 보기
@app.route('/problems', methods=['GET'])
def get_problems():
    problems = Problem.query.all()
    problems_data = []
    for problem in problems:
        problems_data.append({
            'id': problem.id,
            'title': problem.title,
            'description': problem.description,
            'options': problem.options.split(', ') if problem.options else [],
            'image_path': problem.image_path,
            'category': problem.category,
            'difficulty': problem.difficulty,
            'tags': problem.tags
        })
    return jsonify(problems_data)

@app.route('/problem/<int:problem_id>', methods=['GET'])
def get_problem(problem_id):
    problem = Problem.query.get(problem_id)  # ID로 문제 조회
    if problem:
        return jsonify({
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "options": problem.options.split(', ') if problem.options else [],
            "category": problem.category,
            "difficulty": problem.difficulty,
            "tags": problem.tags,
            "image_path": problem.image_path
        })
    else:
        return jsonify({"error": "문제를 찾을 수 없습니다."}), 404


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IBK_ossproject'

    def ready(self):
        import IBK_ossproject.signals

if __name__ == '__main__':
    app.run(debug=True)
