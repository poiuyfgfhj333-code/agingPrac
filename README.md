# 🚀 개인 통합 포털 대시보드 (My Portal Dashboard)

> 🌐 **라이브 대시보드 사이트 바로가기**  
> - **GitHub Pages (라이브 호스팅):** [https://poiuyfgfhj333-code.github.io/agingPrac/](https://poiuyfgfhj333-code.github.io/agingPrac/)  
> - **PythonAnywhere 서버:** [https://jigeum.pythonanywhere.com/](https://jigeum.pythonanywhere.com/)  

---

## ⚡ GitHub Pages 라이브 사이트 활성화 방법 (GitHub 1초 설정)

깃허브 저장소 방문자가 링크를 클릭해 사이트를 바로 볼 수 있도록 GitHub Pages를 활성화하는 방법입니다.

1. 본인 저장소([https://github.com/poiuyfgfhj333-code/agingPrac](https://github.com/poiuyfgfhj333-code/agingPrac)) 상단의 **⚙️ Settings** 탭 클릭
2. 좌측 메뉴에서 **Pages** 클릭
3. **Build and deployment** 항목 아래 **Branch**를 `None` -> `main` 으로 변경 후 **Save** 클릭
4. 약 1분 후 `https://poiuyfgfhj333-code.github.io/agingPrac/` 링크로 접속하면 웹사이트가 그대로 실시간 구동됩니다!

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
├── index.html             # GitHub Pages 및 웹 메인 엔트리 포인트
├── app.py                 # Flask 백엔드 서버 (REST API & 라우팅)
├── wsgi.py                # WSGI 배포 엔트리 포인트 (PythonAnywhere, Gunicorn 등)
├── requirements.txt       # Python 의존성 패키지 목록
├── README.md              # 프로젝트 안내 및 GitHub 업로드 가이드
├── .gitignore             # Git 제외 파일 설정
├── templates/
│   └── index.html         # Flask 템플릿
├── static/
│   ├── css/
│   │   └── style.css      # 커스텀 스타일시트
│   └── js/
│       └── app.js         # 대시보드 프론트엔드 애플리케이션 로직 (정적 JSON 자동 폴백 지원)
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
git clone https://github.com/poiuyfgfhj333-code/agingPrac.git
cd agingPrac
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
