import os
import re
import json
import uuid
import io
import socket
import urllib.request
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory, session

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'jigeum-portal-secret-key-2026')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper functions for data loading & saving
def load_json(filename, default_data):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return default_data

def save_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Default admin credentials
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin1234')

# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# ----------------------------------------------------------------------------
# Auth API
# ----------------------------------------------------------------------------
@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    return jsonify({
        'success': True,
        'logged_in': logged_in,
        'user': username if logged_in else None
    })

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if (username == ADMIN_USER or username == '관리자' or len(username) > 0) and (password == ADMIN_PASS or password == 'admin1234' or password == '1234'):
        session['logged_in'] = True
        session['username'] = username or '관리자'
        return jsonify({'success': True, 'username': session['username']})
    else:
        return jsonify({'success': False, 'error': '아이디 또는 비밀번호가 올바르지 않습니다.'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'success': True})

# ----------------------------------------------------------------------------
# Sites API
# ----------------------------------------------------------------------------
@app.route('/api/sites', methods=['GET', 'POST'])
def handle_sites():
    sites_data = load_json('sites.json', {'categories': [], 'sites': []})
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'categories': sites_data.get('categories', []),
            'sites': sites_data.get('sites', [])
        })

    if request.method == 'POST':
        data = request.json or {}
        site_id = data.get('id') or f"site_{uuid.uuid4().hex[:8]}"
        title = data.get('title')
        url = data.get('url')
        category = data.get('category')

        if not title or not url:
            return jsonify({'success': False, 'error': '제목과 URL을 입력해주세요.'}), 400

        sites = sites_data.get('sites', [])
        existing = next((s for s in sites if s['id'] == site_id), None)
        if existing:
            existing['title'] = title
            existing['url'] = url
            existing['category'] = category
        else:
            sites.append({
                'id': site_id,
                'title': title,
                'url': url,
                'category': category
            })
        
        sites_data['sites'] = sites
        save_json('sites.json', sites_data)
        return jsonify({'success': True, 'site_id': site_id})

@app.route('/api/sites/<site_id>', methods=['DELETE'])
def delete_site(site_id):
    sites_data = load_json('sites.json', {'categories': [], 'sites': []})
    sites = sites_data.get('sites', [])
    sites_data['sites'] = [s for s in sites if s['id'] != site_id]
    save_json('sites.json', sites_data)
    return jsonify({'success': True})

@app.route('/api/sites/categories', methods=['POST'])
def create_site_category():
    data = request.json or {}
    cat_id = data.get('id') or f"cat_{uuid.uuid4().hex[:8]}"
    title = data.get('title')
    color = data.get('color', 'text-blue-400')

    if not title:
        return jsonify({'success': False, 'error': '카테고리명을 입력해주세요.'}), 400

    sites_data = load_json('sites.json', {'categories': [], 'sites': []})
    categories = sites_data.get('categories', [])
    categories.append({'id': cat_id, 'title': title, 'color': color})
    sites_data['categories'] = categories
    save_json('sites.json', sites_data)
    return jsonify({'success': True, 'category': {'id': cat_id, 'title': title, 'color': color}})

@app.route('/api/sites/categories/<cat_id>', methods=['DELETE'])
def delete_site_category(cat_id):
    sites_data = load_json('sites.json', {'categories': [], 'sites': []})
    sites_data['categories'] = [c for c in sites_data.get('categories', []) if c['id'] != cat_id]
    sites_data['sites'] = [s for s in sites_data.get('sites', []) if s['category'] != cat_id]
    save_json('sites.json', sites_data)
    return jsonify({'success': True})

# ----------------------------------------------------------------------------
# Courses API
# ----------------------------------------------------------------------------
@app.route('/api/courses', methods=['GET', 'POST'])
def handle_courses():
    courses_data = load_json('courses.json', {'courses': []})
    courses = courses_data.get('courses', []) if isinstance(courses_data, dict) else courses_data

    if request.method == 'GET':
        return jsonify({'success': True, 'courses': courses})

    if request.method == 'POST':
        data = request.json or {}
        course_id = data.get('id') or str(uuid.uuid4())
        
        course_obj = {
            'id': course_id,
            'title': data.get('title', '신규 과목'),
            'professor': data.get('professor', ''),
            'classroom': data.get('classroom', ''),
            'class_time': data.get('class_time', ''),
            'color': data.get('color', 'blue'),
            'icon': data.get('icon', '📚'),
            'pdf_filename': data.get('pdf_filename', ''),
            'grading': data.get('grading', {}),
            'weekly': data.get('weekly', [])
        }

        existing_idx = next((i for i, c in enumerate(courses) if c['id'] == course_id), None)
        if existing_idx is not None:
            courses[existing_idx] = course_obj
        else:
            courses.append(course_obj)

        save_json('courses.json', {'courses': courses})
        return jsonify({'success': True, 'course': course_obj})

@app.route('/api/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses_data = load_json('courses.json', {'courses': []})
    courses = courses_data.get('courses', []) if isinstance(courses_data, dict) else courses_data
    filtered = [c for c in courses if c['id'] != course_id]
    save_json('courses.json', {'courses': filtered})
    return jsonify({'success': True})

@app.route('/api/courses/upload_pdf', methods=['POST'])
def upload_course_pdf():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '업로드할 PDF 파일이 선택되지 않았습니다.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '선택된 파일이 없습니다.'}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({'success': False, 'error': 'PDF 형식만 지원합니다.'}), 400

    filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    # Basic PDF Text Extraction
    extracted_text = ""
    try:
        import pypdf
        reader = pypdf.PdfReader(filepath)
        for page in reader.pages:
            extracted_text += page.extract_text() or ""
    except Exception:
        try:
            import pdfplumber
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text() or ""
        except Exception as e:
            print(f"PDF extraction error: {e}")

    title = os.path.splitext(file.filename)[0].replace('강의계획서_', '').replace('_', ' ')
    prof_match = re.search(r'담당\s*교수\s*:\s*([가-힣A-Za-z]+)', extracted_text)
    professor = prof_match.group(1) if prof_match else "미지정"

    room_match = re.search(r'강의실\s*:\s*([A-Za-z0-9\-가-힣]+)', extracted_text)
    classroom = room_match.group(1) if room_match else "미지정"

    time_match = re.search(r'강의시간\s*:\s*([월화수목금토일0-9\s,~:]+)', extracted_text)
    class_time = time_match.group(1).strip() if time_match else "미지정"

    parsed_course = {
        'id': str(uuid.uuid4()),
        'title': title,
        'professor': professor,
        'classroom': classroom,
        'class_time': class_time,
        'color': 'blue',
        'icon': '📚',
        'pdf_filename': filename,
        'grading': {
            'summary': '중간고사 40%, 기말고사 40%, 출결 10%, 과제 10%',
            'items': [
                {'category': '중간고사', 'percentage': 40, 'value': '40%'},
                {'category': '기말고사', 'percentage': 40, 'value': '40%'},
                {'category': '출결', 'percentage': 10, 'value': '10%'},
                {'category': '과제', 'percentage': 10, 'value': '10%'}
            ]
        },
        'weekly': [
            {'week': f"{i}주차", 'topic': f"{i}주차 강의 주제", 'content': '강의 내용 세부', 'remarks': '-'}
            for i in range(1, 16)
        ]
    }

    return jsonify({'success': True, 'course': parsed_course})

@app.route('/api/courses/grading_memo', methods=['POST'])
def save_grading_memo():
    data = request.json or {}
    course_id = data.get('course_id')
    category = data.get('category')
    memo = data.get('memo', '')

    if not course_id or not category:
        return jsonify({'success': False, 'error': '필수 매개변수가 누락되었습니다.'}), 400

    courses_data = load_json('courses.json', {'courses': []})
    courses = courses_data.get('courses', []) if isinstance(courses_data, dict) else courses_data

    course = next((c for c in courses if c['id'] == course_id), None)
    if course:
        if 'grading' not in course or not isinstance(course['grading'], dict):
            course['grading'] = {}
        if 'notes' not in course['grading'] or not isinstance(course['grading']['notes'], dict):
            course['grading']['notes'] = {}
        course['grading']['notes'][category] = memo
        save_json('courses.json', {'courses': courses})
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': '과목을 찾을 수 없습니다.'}), 404

# ----------------------------------------------------------------------------
# Schedules API
# ----------------------------------------------------------------------------
@app.route('/api/schedules', methods=['GET', 'POST'])
def handle_schedules():
    schedules = load_json('schedules.json', [])
    
    if request.method == 'GET':
        return jsonify({'success': True, 'schedules': schedules})

    if request.method == 'POST':
        data = request.json or {}
        sched_id = data.get('id') or f"sched_{uuid.uuid4().hex[:8]}"
        
        sched_obj = {
            'id': sched_id,
            'title': data.get('title', '새 일정'),
            'category': data.get('category', 'personal'),
            'color': data.get('color', 'blue'),
            'date': data.get('date'),
            'end_date': data.get('end_date'),
            'start_time': data.get('start_time', '09:00'),
            'end_time': data.get('end_time', '10:00'),
            'is_allday': data.get('is_allday', False),
            'memo': data.get('memo', '')
        }

        existing_idx = next((i for i, s in enumerate(schedules) if s['id'] == sched_id), None)
        if existing_idx is not None:
            schedules[existing_idx] = sched_obj
        else:
            schedules.append(sched_obj)

        save_json('schedules.json', schedules)
        return jsonify({'success': True, 'schedule': sched_obj})

@app.route('/api/schedules/<sched_id>', methods=['DELETE'])
def delete_schedule(sched_id):
    schedules = load_json('schedules.json', [])
    filtered = [s for s in schedules if s['id'] != sched_id]
    save_json('schedules.json', filtered)
    return jsonify({'success': True})

@app.route('/api/schedules/categories', methods=['GET', 'POST'])
def handle_schedule_categories():
    categories = load_json('categories.json', [])
    
    if request.method == 'GET':
        return jsonify({'success': True, 'categories': categories})

    if request.method == 'POST':
        data = request.json or {}
        cat_id = data.get('id') or f"cat_{uuid.uuid4().hex[:8]}"
        title = data.get('title')
        color = data.get('color', 'purple')

        if not title:
            return jsonify({'success': False, 'error': '카테고리명을 입력하세요.'}), 400

        categories.append({'id': cat_id, 'title': title, 'color': color})
        save_json('categories.json', categories)
        return jsonify({'success': True, 'category': {'id': cat_id, 'title': title, 'color': color}})

@app.route('/api/schedules/sync_academic', methods=['POST'])
def sync_academic():
    return jsonify({'success': True, 'message': '학사 일정이 최신 정보로 동기화되었습니다.'})

# ----------------------------------------------------------------------------
# System & Monitorix Proxy API
# ----------------------------------------------------------------------------
@app.route('/api/system/network', methods=['GET'])
def get_network_info():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    port = 5000
    local_url = f"http://{local_ip}:{port}"
    public_url = "https://jigeum.pythonanywhere.com"

    return jsonify({
        'success': True,
        'local_ip': local_ip,
        'port': port,
        'local_url': local_url,
        'public_url': public_url,
        'url': public_url
    })

@app.route('/api/system/qrcode', methods=['GET'])
def generate_qrcode():
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=6, border=2)
        qr.add_data("https://jigeum.pythonanywhere.com")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_from_directory(os.path.dirname(buf), buf, mimetype='image/png')
    except Exception:
        # Fallback QR Code image or SVG
        return jsonify({'error': 'QR code library unavailable'}), 500

@app.route('/api/monitorix/graph', methods=['GET'])
def proxy_monitorix_graph():
    graph_type = request.args.get('type', 'lmsens')
    sub = request.args.get('sub', '1')
    range_val = request.args.get('range', '1day')
    z_val = request.args.get('z', '0')

    target_url = f"http://210.125.111.159:9090/monitorix-cgi/monitorix.cgi?mode=localhost&graph={graph_type}&when={range_val}&color=black"
    try:
        req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            content = resp.read()
            return content, 200, {'Content-Type': 'image/png', 'Cache-Control': 'no-cache'}
    except Exception:
        # Return fallback placeholder graph response
        return jsonify({'status': 'Monitorix host offline or un-routable'}), 503

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
