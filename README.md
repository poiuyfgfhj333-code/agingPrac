# 🚀 개인 통합 포털 대시보드 (My Portal Dashboard)

`https://jigeum.pythonanywhere.com/` 사이트의 소스 코드 및 데이터 전체를 깃허브(GitHub)에 업로드하고 배포할 수 있도록 구성된 풀스택 웹 애플리케이션 프로젝트입니다.

---

## 🌟 주요 기능 (Features)

1. **서버 하드웨어 모니터링 (Home Tab)**
   - Monitorix 에이전트 연동 실시간 하드웨어 그래프 모니터링 (LM-Sensors, NVIDIA GPU, Disk Drive)
   - 1일 / 1주 / 1달 / 1년 간격 선택 및 자동 새로고침 (30초/1분/5분)
   - 고해상도 그래프 확대 보기 모달

2. **자주 가는 사이트 북마크 허브 (Site Tab)**
   - 4대 카테고리 (LMS, 부경대 포털, 학과별 홈페이지, 연구 관련) 북마크
   - 실시간 사이트 검색 및 추가/수정/삭제 모드

3. **수강 강의 및 7일 주간 시간표 (Course Tab)**
   - 연동 강의시간표 자동 파싱 및 연속 교시 블록 셀 병합 (1~7일 전체)
   - 강의계획서 PDF 파일 업로드 및 자동 텍스트 추출 (PyPDF / pdfplumber)
   - 과목별 성적 반영 비율, 평가 방법 및 1~16주차 상세 강의계획서 모달

4. **학사 및 개인 일정 관리 캘린더 (Schedule Tab)**
   - 월간(Month) / 주간(Week) 뷰 전환 지원
   - 카테고리별 일정 필터링 및 부경대 LMS 학사 일정 연동
   - 일정 등록/수정/삭제 및 종일 일정 옵션

5. **관리자 로그인 & 보안**
   - 사용자 인증 상태 관리 및 모바일 QR 코드 접속 가이드

---

## 📁 프로젝트 구조 (Project Structure)

```
jigeum-portal/
├── app.py                 # Flask 백엔드 서버 (REST API & 라우팅)
├── wsgi.py                # WSGI 배포 엔트리 포인트 (PythonAnywhere, Gunicorn 등)
├── requirements.txt       # Python 의존성 패키지 목록
├── README.md              # 프로젝트 안내 및 GitHub 업로드 가이드
├── .gitignore             # Git 제외 파일 설정
├── templates/
│   └── index.html         # 대시보드 메인 HTML 템플릿
├── static/
│   ├── css/
│   │   └── style.css      # 커스텀 스타일시트
│   └── js/
│       └── app.js         # 대시보드 프론트엔드 애플리케이션 로직
├── data/
│   ├── sites.json         # 북마크 사이트 데이터
│   ├── courses.json       # 수강 과목 및 강의계획서 데이터
│   ├── schedules.json     # 일정 관리 데이터
│   └── categories.json    # 일정 카테고리 데이터
└── uploads/               # 업로드된 강의계획서 PDF 저장 폴더
```

---

## 💻 로컬 실행 방법 (How to Run Locally)

### 1. 레포지토리 클론 및 이동
```bash
git clone https://github.com/사용자이름/레포지토리이름.git
cd jigeum-portal
```

### 2. 가상환경 생성 및 의존성 설치
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Flask 서버 실행
```bash
python app.py
```
브라우저에서 `http://localhost:5000` 접속 후 사용합니다.

---

## 📤 깃허브(GitHub)에 업로드하는 방법

### 1단계: Git 저장소 초기화 및 커밋
터미널에서 이 프로젝트 폴더(`jigeum-portal`)로 이동 후 실행:

```bash
git init
git add .
git commit -m "Initial commit: My Portal Dashboard full source and data"
```

### 2단계: GitHub 새 레포지토리 생성
1. [GitHub](https://github.com/) 접속 후 **New repository** 클릭
2. Repository name 입력 (예: `jigeum-portal`)
3. Public 선택 후 **Create repository** 클릭

### 3단계: GitHub에 코드 푸시 (Push)
```bash
git branch -M main
git remote add origin https://github.com/본인계정명/jigeum-portal.git
git push -u origin main
```

---

## 🌐 PythonAnywhere에 재배포하는 방법

1. PythonAnywhere 대시보드에서 **Bash console** 열기
2. 깃허브 코드 클론:
   ```bash
   git clone https://github.com/본인계정명/jigeum-portal.git
   ```
3. **Web** 탭 -> **WSGI configuration file** 편집:
   ```python
   import sys
   path = '/home/본인아이디/jigeum-portal'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
4. **Reload** 버튼 클릭
