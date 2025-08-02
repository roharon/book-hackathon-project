# Chapter 2: 거래하기 안전한 SNS 마켓

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 2 프로젝트

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [설치 및 실행](#-설치-및-실행)
- [API 문서](#-api-문서)
- [학습 포인트](#-학습-포인트)
- [문제 해결](#-문제-해결)

## 📋 프로젝트 개요

SNS를 통해 이루어지는 중고거래의 안전성을 높이는 거래 플랫폼입니다. 이 프로젝트는 해커톤에서 **빠른 MVP 개발**과 **팀 협업**을 위한 기본 구조를 제공합니다.

### Chapter 2에서 배우는 내용

- **아이디어 도출 기법**: 마인드 맵, 스캠퍼(SCAMPER), 스마트(SMART) 기법 실습
- **기술 스택 선정**: 제한된 시간 내 최적의 기술 조합 선택
- **API 설계**: RESTful API 스펙 작성 및 팀 내 공유
- **데이터베이스 모델링**: SQLAlchemy ORM을 활용한 관계형 데이터 설계
- **협업 구조**: 팀 협업을 위한 프로젝트 구조 설계

### 해결하고자 하는 문제

- SNS 거래에서 발생하는 사기 및 신뢰성 문제
- 거래 과정의 투명성 부족
- 안전한 결제 시스템의 필요성

## 🎯 기능

### 핵심 기능
- **상품 등록 및 관리**: 판매자가 상품을 등록하고 관리
- **주문 시스템**: 구매자의 주문 처리 및 상태 관리
- **거래 추적**: 주문부터 완료까지 전 과정 추적

### 주요 특징
- **간단한 인증**: 해커톤에 적합한 단순화된 사용자 인증
- **RESTful API**: 표준화된 API 인터페이스
- **자동 문서화**: FastAPI 기반 자동 API 문서 생성

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 빠른 API 개발을 위한 모던 웹 프레임워크
- **SQLAlchemy**: Python ORM 라이브러리
- **SQLite**: 경량 데이터베이스 (개발 및 프로토타이핑용)
- **Uvicorn**: ASGI 서버

### 개발 도구
- **pipenv**: Python 패키지 관리 및 가상환경
- **Python 3.11**: 주요 개발 언어

### 선택 이유
- **SQLite 사용**: 별도 DB 서버 설정 없이 빠른 프로토타이핑 가능
- **FastAPI**: 자동 문서 생성으로 팀 협업 효율성 극대화
- **단순한 구조**: 해커톤 제한 시간 내 구현 가능한 최소 복잡도

## 📖 설치 및 실행

### 사전 요구사항

- Python 3.11+
- pip 또는 pipenv

### 1. 프로젝트 클론

```bash
git clone https://github.com/roharon/book-hackathon-project.git
cd book-hackathon-project/SnsMarket
```

### 2. 가상환경 설정 및 의존성 설치

#### pipenv 사용 (권장)

```bash
# pipenv 설치 (없는 경우)
pip install pipenv

# 가상환경 생성 및 의존성 설치
pipenv install

# 가상환경 활성화
pipenv shell
```

#### pip 사용

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install fastapi sqlalchemy sqlalchemy-utils uvicorn[standard]
```

### 3. 데이터베이스 초기화

```bash
# 데이터베이스 테이블 생성
python create_table.py
```

### 4. 애플리케이션 실행

```bash
# 개발 서버 시작
python -m uvicorn main:app --reload
```

### 5. 서비스 확인

- **API 서버**: http://localhost:8000
- **API 문서 (Swagger UI)**: http://localhost:8000/docs
- **API 문서 (ReDoc)**: http://localhost:8000/redoc

## 📚 API 문서

### 기본 엔드포인트

#### 상품 관리
```http
GET    /items/           # 전체 상품 목록 조회
POST   /items/           # 새 상품 등록
GET    /items/{item_id}  # 특정 상품 상세 조회
```

#### 주문 관리
```http
POST   /orders/          # 새 주문 생성
GET    /orders/{order_id} # 주문 상세 조회
```

### API 응답 예시

#### 상품 목록 조회
```json
[
  {
    "id": 1,
    "name": "아이폰 14 Pro",
    "description": "깔끔하게 사용한 아이폰입니다",
    "price": 800000,
    "seller_id": 1,
    "is_sold": false,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### 주문 생성
```json
{
  "item_id": 1,
  "buyer_id": 2,
  "quantity": 1
}
```

## 💡 학습 포인트

### 1. 해커톤 개발 방법론

**핵심 기능 우선 구현**
- 로그인/회원가입보다 거래 핵심 로직에 집중
- MVP(Minimum Viable Product) 개념 적용
- 시간 제약 내에서 동작하는 프로토타입 완성

**팀 협업 효율화**
- FastAPI 자동 문서로 백엔드-프론트엔드 협업 원활화
- 명확한 API 스펙 공유로 병렬 개발 가능
- 간단한 데이터 모델로 빠른 이해 및 구현

### 2. 기술적 학습 요소

**FastAPI 활용**
- 자동 API 문서 생성 기능
- Pydantic을 통한 데이터 검증
- 비동기 처리 지원

**SQLAlchemy ORM**
- 객체-관계 매핑 개념
- 데이터베이스 모델 설계
- 관계 설정 (일대다, 다대다)

**RESTful API 설계**
- HTTP 메서드별 용도 이해
- 리소스 기반 URL 설계
- 상태 코드 활용

### 3. 해커톤 전략

**시간 관리**
- 기능별 우선순위 설정
- 핵심 기능 완성 후 부가 기능 추가
- 지속적인 동작 가능한 버전 유지

**위험 관리**
- 검증된 기술 스택 사용
- 복잡한 기능보다 안정적 구현 우선
- 팀원 스킬에 맞는 기술 선택

## 🔧 문제 해결

### 환경 설정 문제

**문제**: pipenv 설치 실패
```bash
# 해결: pip 업그레이드 후 재시도
pip install --upgrade pip
pip install pipenv
```

**문제**: SQLite 데이터베이스 파일 접근 오류
```bash
# 해결: 현재 디렉토리에 쓰기 권한 확인
ls -la market.db
chmod 644 market.db  # 필요시 권한 조정
```

### 개발 중 문제

**문제**: FastAPI 서버 시작 실패
```bash
# 해결: 포트 충돌 확인 및 다른 포트 사용
uvicorn main:app --reload --port 8001
```

**문제**: 데이터베이스 테이블이 생성되지 않음
```bash
# 해결: create_table.py 실행 확인
python create_table.py
```

### API 호출 문제

**문제**: CORS 오류 발생
```python
# 해결: main.py에 CORS 설정 추가
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📁 프로젝트 구조

```
SnsMarket/
├── main.py                  # FastAPI 애플리케이션 진입점
├── create_table.py         # 데이터베이스 테이블 생성 스크립트
├── database.py             # 데이터베이스 연결 설정
├── Pipfile                 # pipenv 의존성 정의
├── Pipfile.lock           # 의존성 버전 고정
├── models/                 # SQLAlchemy 데이터 모델
│   ├── __init__.py
│   ├── items.py           # 상품 모델
│   ├── markets.py         # 마켓 모델  
│   ├── orders.py          # 주문 모델
│   └── users.py           # 사용자 모델
├── routers/               # FastAPI 라우터
│   ├── __init__.py
│   ├── items.py          # 상품 API 엔드포인트
│   └── orders.py         # 주문 API 엔드포인트
├── schemas/              # Pydantic 스키마
│   ├── items.py         # 상품 요청/응답 스키마
│   └── orders.py        # 주문 요청/응답 스키마
├── services/            # 비즈니스 로직
│   ├── auth.py         # 인증 서비스
│   ├── items.py        # 상품 서비스
│   └── orders.py       # 주문 서비스
└── exceptions/         # 커스텀 예외
    └── exceptions.py
```

## 🚀 다음 단계

Chapter 2를 완료한 후에는 다음 장으로 진행하여 더 고급 주제들을 학습할 수 있습니다:

- **Chapter 3**: FastAPI + PostgreSQL + Docker를 활용한 확장 가능한 서비스
- **Chapter 4**: AWS Lambda와 OCR을 활용한 서버리스 아키텍처  
- **Chapter 5**: OpenAPI 연동을 통한 외부 서비스 활용

## 📖 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/)
- [pipenv 사용법](https://pipenv.pypa.io/en/latest/)

## 📖 도서 정보

**『해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지』**
- **저자**: 노아론 (github.com/roharon)
- **출판사**: 로드북
- **출간일**: 2025년 7월 28일

### 구매 링크
- [교보문고](https://product.kyobobook.co.kr/detail/S000217089414)
- [예스24](https://www.yes24.com/product/goods/149385474)
- [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)

---

해커톤의 핵심은 **본질에 집중**하는 것입니다. 화려한 부가 기능보다는 여러분의 아이디어가 가진 고유한 가치를 명확하게 보여주는 핵심 기능에 집중해보세요!
