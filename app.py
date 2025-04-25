from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from chatbot import get_bot_reply
from resume_parser import extract_resume_text, parse_resume
from matcher import calculate_match_score

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return "Smart Recruitment AI is up and running!"

@app.route('/api/resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'Missing file field "resume" in form-data'}), 400

    file = request.files['resume']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: pdf, doc, docx'}), 400

    job_description = request.form.get('job_description', '')
    if not job_description:
        return jsonify({'error': 'Missing job_description field'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        text = extract_resume_text(filepath)
        parsed = parse_resume(text)
        score = calculate_match_score(text, job_description)

        return jsonify({
            'message': f'Resume uploaded successfully: {filename}',
            'parsed_resume': parsed,
            'match_score': f"{score}%"
        }), 200
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'Empty message'}), 400

    response = get_bot_reply(message)
    return jsonify({'reply': response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



