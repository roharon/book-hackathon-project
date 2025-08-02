# Chapter 3: 주변 대학의 학생식당 메뉴 모아보기

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=flat&logo=sqlalchemy&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 3 프로젝트

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [설치 및 실행](#-설치-및-실행)
- [API 엔드포인트](#-api-엔드포인트)
- [학습 포인트](#-학습-포인트)
- [문제 해결](#-문제-해결)

## 📋 프로젝트 개요

여러 대학교의 학생식당 메뉴 정보를 통합적으로 관리하고 조회할 수 있는 API 서비스입니다. 이 프로젝트는 FastAPI와 PostgreSQL을 사용하여 구축되었으며, Docker를 통한 컨테이너화 환경에서 실행됩니다.

## 🎯 기능

- 대학교별 학생식당 메뉴 조회
- 메뉴 이미지 업로드 및 관리
- 대학교 및 식당 정보 관리
- RESTful API를 통한 데이터 접근

## Chapter 3에서 학습하는 내용

이 프로젝트를 통해 다음과 같은 해커톤 핵심 기술들을 학습할 수 있습니다:

### 1. 아이디어 도출 기법
- **마인드 맵 기법**: 중심 주제에서 연관 아이디어로 확장
- **스캠퍼(SCAMPER) 기법**: 기존 아이디어를 체계적으로 개선
- **스마트(SMART) 기법**: 구체적이고 측정 가능한 목표 설정

### 2. 기술 스택 선정
- FastAPI 프레임워크 도입 이유와 장점
- PostgreSQL 데이터베이스 선택 근거
- Docker를 활용한 개발 환경 표준화

### 3. 서비스 아키텍처 설계
- RESTful API 설계 원칙
- 데이터베이스 모델링
- 컨테이너 기반 마이크로서비스 구조

### 4. 협업 및 배포
- GitHub Actions CI/CD 파이프라인 구성
- API 문서 자동화
- 팀 협업을 위한 코드 구조화

## 🛠️ 기술 스택

- **Backend**: FastAPI 0.100.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.18
- **Containerization**: Docker & Docker Compose
- **Package Management**: pipenv
- **API Documentation**: FastAPI 자동 생성 문서 (Swagger UI)

## 프로젝트 구조

```
UniversityCafeteriaMenu/
├── app/
│   ├── api/                    # API 라우터 및 엔드포인트
│   │   ├── endpoints/
│   │   │   └── menus.py       # 메뉴 관련 API
│   │   ├── api.py             # 메인 API 라우터
│   │   └── deps.py            # 의존성 관리
│   ├── core/
│   │   └── config.py          # 애플리케이션 설정
│   ├── crud/                  # 데이터베이스 CRUD 연산
│   │   ├── crud_cafeterias.py
│   │   ├── crud_menus.py
│   │   └── crud_universities.py
│   ├── db/                    # 데이터베이스 설정
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py         # DB 초기화
│   ├── models/                # SQLAlchemy 모델
│   │   ├── university.py      # 대학교 모델
│   │   ├── cafeteria.py       # 식당 모델
│   │   ├── menu.py            # 메뉴 모델
│   │   └── menu_image.py      # 메뉴 이미지 모델
│   ├── schemas/               # Pydantic 스키마
│   │   ├── university.py
│   │   ├── cafeteria.py
│   │   └── menu.py
│   ├── main.py                # FastAPI 애플리케이션 진입점
│   └── Dockerfile             # 백엔드 컨테이너 설정
├── docker-compose.yml         # 전체 서비스 오케스트레이션
├── Pipfile                    # pipenv 의존성 정의
├── Pipfile.lock              # 의존성 버전 잠금
└── requirements.txt          # pip 의존성 (Docker용)
```

## 데이터베이스 스키마

### University (대학교)
- `id`: 기본키
- `name`: 대학교명
- `created_at`, `updated_at`: 생성/수정 시각

### Cafeteria (식당)
- `id`: 기본키
- `university_id`: 대학교 외래키
- `name`: 식당명
- `description`: 식당 설명
- `created_at`, `updated_at`: 생성/수정 시각

### Menu (메뉴)
- `id`: 기본키
- `cafeteria_id`: 식당 외래키
- `description`: 메뉴 설명
- `price`: 가격
- `provides_at`: 제공 일시
- `created_at`, `updated_at`: 생성/수정 시각

### MenuImage (메뉴 이미지)
- `id`: 기본키
- `menu_id`: 메뉴 외래키
- `image_url`: 이미지 URL
- `created_at`, `updated_at`: 생성/수정 시각

## 📖 설치 및 실행

### 사전 요구사항

- Docker Desktop
- Python 3.11+ (로컬 개발 시)
- pipenv (로컬 개발 시)

### 1. 프로젝트 클론

```bash
git clone https://github.com/roharon/book-hackathon-project.git
cd book-hackathon-project/UniversityCafeteriaMenu
```

### 2. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가합니다:

```env
# PostgreSQL 설정
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=app

# 애플리케이션 설정
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@db:5432/app
```

### 3. Docker를 사용한 실행 (권장)

```bash
# 서비스 빌드 및 시작
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build
```

### 4. 로컬 개발 환경 설정 (선택사항)

```bash
# pipenv를 사용한 가상환경 생성 및 의존성 설치
pipenv install

# 가상환경 활성화
pipenv shell

# PostgreSQL이 로컬에서 실행 중이어야 함
# 애플리케이션 실행
cd app
python main.py
```

### 5. 서비스 확인

- **API 서버**: http://localhost:8000
- **API 문서 (Swagger UI)**: http://localhost:8000/docs
- **API 문서 (ReDoc)**: http://localhost:8000/redoc
- **PostgreSQL**: localhost:5432

## 📚 API 엔드포인트

### 메뉴 조회
```http
GET /universities/{university_id}/cafeterias/menus
```
특정 대학교의 모든 식당 메뉴를 조회합니다.

**응답 예시:**
```json
[
  {
    "id": 1,
    "description": "비빔밥\n핫도그",
    "price": 3500,
    "cafeteria": {
      "id": 1,
      "name": "본관 학생식당",
      "description": "학생식당입니다."
    }
  }
]
```

### 메뉴 이미지 업로드
```http
POST /menus/{menu_id}/image
```
특정 메뉴에 이미지를 추가합니다.

**요청 본문:**
```json
{
  "image_url": "https://example.com/menu-image.jpg"
}
```

### 메뉴 생성 (이벤트)
```http
POST /menus/event
```
새로운 메뉴를 생성합니다. (크롤링 기능 예정)

## 개발 시 참고사항

### 1. 코드 구조 이해

이 프로젝트는 FastAPI의 권장 구조를 따릅니다:

- **Models**: SQLAlchemy ORM 모델 (데이터베이스 테이블 정의)
- **Schemas**: Pydantic 모델 (API 입출력 검증)
- **CRUD**: 데이터베이스 연산 로직 분리
- **API**: 엔드포인트별 라우터 분리

### 2. 데이터베이스 마이그레이션

현재는 애플리케이션 시작 시 자동으로 테이블이 생성됩니다. 프로덕션 환경에서는 Alembic을 사용한 마이그레이션을 권장합니다.

### 3. 환경별 설정

- 개발: Docker Compose를 사용한 로컬 개발
- 배포: GitHub Actions를 통한 CI/CD (Chapter 3에서 설명)

## 💡 학습 포인트

### 해커톤에서의 활용 팁

### 1. 빠른 프로토타이핑
- FastAPI의 자동 문서 생성 기능으로 API 스펙 공유
- Docker Compose로 팀원 간 개발 환경 통일
- SQLAlchemy ORM으로 빠른 데이터 모델링

### 2. 기능 확장 아이디어
- 메뉴 추천 알고리즘 추가
- 실시간 메뉴 업데이트 (웹 크롤링)
- 사용자 리뷰 및 평점 시스템
- 모바일 앱 연동을 위한 Push 알림

### 3. 기술적 개선 방향
- Redis를 활용한 캐싱 시스템
- Celery를 사용한 비동기 작업 처리
- AWS RDS, S3 등 클라우드 서비스 연동

## 🔧 문제 해결

### Docker 관련 이슈

**문제**: 컨테이너가 시작되지 않는 경우
```bash
# 로그 확인
docker-compose logs

# 컨테이너 재시작
docker-compose down
docker-compose up --build
```

**문제**: 데이터베이스 연결 오류
```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose ps

# 데이터베이스 헬스체크 대기
docker-compose up --wait
```

### 개발 환경 이슈

**문제**: pipenv 의존성 설치 실패
```bash
# pip 업그레이드
pip install --upgrade pip

# pipenv 재설치
pip install --upgrade pipenv

# 의존성 다시 설치
pipenv install
```

**문제**: 포트 충돌
```bash
# 사용 중인 포트 확인 (macOS/Linux)
lsof -i :8000
lsof -i :5432

# 다른 포트로 변경
# docker-compose.yml 파일에서 포트 번호 수정
```

## 학습 체크리스트

이 프로젝트를 완료한 후 다음 사항들을 확인해보세요:

- [ ] FastAPI 기본 구조와 의존성 주입 이해
- [ ] SQLAlchemy ORM을 사용한 데이터베이스 모델링
- [ ] Docker Compose를 활용한 멀티 컨테이너 환경 구성
- [ ] RESTful API 설계 원칙 적용
- [ ] Pydantic을 사용한 데이터 검증
- [ ] 환경 변수를 통한 설정 관리
- [ ] API 문서 자동 생성 및 활용

## 다음 단계

Chapter 3을 완료한 후에는 다음 장으로 진행하여 더 고급 주제들을 학습할 수 있습니다:

- **Chapter 4**: OCR API와 메신저 연동을 활용한 식단표 서비스
- **Chapter 5**: OpenAPI를 활용한 캠핑장 검색 서비스
- **Chapter 6**: AWS Lambda를 사용한 서버리스 아키텍처

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/)
- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)

## 책 정보

- **제목**: 해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지
- **저자**: 노아론
- **출판사**: 로드북
- **구매링크**: 
  - [교보문고](https://product.kyobobook.co.kr/detail/S000217089414)
  - [예스24](https://www.yes24.com/product/goods/149385474)
  - [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)
