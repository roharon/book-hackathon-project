# Chapter 9: 즐겨보는 블로그 글 모아보기

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Azure Functions](https://img.shields.io/badge/Azure-Functions-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Cosmos DB](https://img.shields.io/badge/Azure-Cosmos%20DB-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![RSS](https://img.shields.io/badge/RSS-Feed-FFA500?style=flat&logo=rss&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-5-E34F26?style=flat&logo=html5&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 9 프로젝트

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [설치 및 배포](#-설치-및-배포)
- [API 문서](#-api-문서)
- [학습 포인트](#-학습-포인트)
- [문제 해결](#-문제-해결)

## 📋 프로젝트 개요

이 프로젝트는 **"해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지"** Chapter 9에서 다루는 RSS 피드 기반 블로그 아티클 수집 서비스입니다. 

여러 블로그의 RSS 피드를 구독하고, 자동으로 새로운 글을 수집하여 한 곳에서 모아볼 수 있는 서비스를 구현합니다. Azure Functions를 활용한 서버리스 아키텍처로 비용 효율적이면서도 확장 가능한 솔루션을 제공합니다.

### 주요 기능

- **RSS 피드 구독 관리**: 블로그 RSS URL을 추가/삭제하여 구독 목록을 관리
- **자동 아티클 수집**: 타이머 기반으로 주기적(10분마다)으로 새로운 글을 자동 수집
- **통합 피드 제공**: 구독한 모든 블로그의 최신 글을 시간순으로 정렬하여 제공
- **웹 인터페이스**: 수집된 글 목록을 확인할 수 있는 간단한 웹 페이지
- **REST API**: 프로그래밍 방식으로 블로그 관리 및 피드 조회 가능

## 기술 스택

### 백엔드
- **Azure Functions**: 서버리스 컴퓨팅 플랫폼
- **Python 3.9+**: 메인 프로그래밍 언어
- **Azure Cosmos DB (MongoDB API)**: NoSQL 데이터베이스
- **feedparser**: RSS/Atom 피드 파싱 라이브러리
- **html2text**: HTML을 텍스트로 변환하는 라이브러리

### 프론트엔드
- **HTML/JavaScript**: 웹 인터페이스
- **Tailwind CSS**: 스타일링 프레임워크

### 인프라
- **Azure API Management**: API 게이트웨이 (선택사항)
- **Azure Application Insights**: 모니터링 및 로깅

## 서비스 아키텍처

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   웹 클라이언트   │────│  Azure Functions │────│  Cosmos DB      │
│                 │    │                  │    │  (MongoDB API)  │
└─────────────────┘    │  - HTTP 트리거    │    └─────────────────┘
                       │  - 타이머 트리거   │            │
┌─────────────────┐    │                  │            │
│   RSS 피드들     │────│                  │────────────┘
│  (외부 블로그)   │    └──────────────────┘
└─────────────────┘
```

## XML/RSS 피드 처리 방식

### RSS 피드 구조 이해
RSS(Really Simple Syndication) 피드는 XML 형식으로 블로그나 뉴스 사이트의 최신 콘텐츠를 구조화된 형태로 제공합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>블로그 제목</title>
    <description>블로그 설명</description>
    <link>https://example.com</link>
    <item>
      <title>글 제목</title>
      <description>글 내용 요약</description>
      <link>https://example.com/article</link>
      <pubDate>Tue, 10 Oct 2023 10:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
```

### 피드 파싱 및 처리
- **feedparser 라이브러리**: XML 구조를 Python 객체로 변환
- **중복 제거**: 이미 수집된 글은 게시 시간을 기준으로 필터링
- **HTML 정리**: html2text를 사용하여 HTML 태그를 제거하고 텍스트만 추출

## 설치 및 실행

### 사전 요구사항

1. **Python 3.9 이상**
2. **Azure Functions Core Tools**
   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```
3. **Azure CLI** (배포용)
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

### 로컬 개발 환경 설정

1. **프로젝트 클론 및 이동**
   ```bash
   git clone https://github.com/roharon/book-hackathon-project.git
   cd book-hackathon-project/RssFeed
   ```

2. **Python 가상환경 생성 및 활성화**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate    # Windows
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **환경 변수 설정**
   `local.settings.json` 파일에 다음 설정을 추가:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
       "COSMOS_CONNECTION_STRING": "your_cosmos_db_connection_string"
     }
   }
   ```

5. **로컬 실행**
   ```bash
   func start
   ```

### Azure Cosmos DB 설정

1. **Azure Portal에서 Cosmos DB 계정 생성**
   - API: MongoDB
   - 데이터베이스 이름: `RssFeed`
   - 컬렉션: `blogs`, `articles`

2. **연결 문자열 복사**
   - Azure Portal > Cosmos DB > 연결 문자열
   - MongoDB 연결 문자열을 `local.settings.json`에 추가

## API 문서

### 블로그 구독 추가
```http
POST /api/rss
Content-Type: application/json

{
  "blog_url": "https://example.com/rss"
}
```

### 구독 블로그 목록 조회
```http
GET /api/rss
```

### 블로그 구독 해제
```http
DELETE /api/rss/{blog_id}
```

### 피드 글 목록 조회
```http
GET /api/rss/feed
```

**응답 예시:**
```json
[
  {
    "title": "Azure Functions 사용법",
    "summary": "Azure Functions를 사용하여 서버리스 애플리케이션을 개발하는 방법...",
    "link": "https://example.com/azure-functions",
    "published_at": "2023-10-10T10:00:00+09:00"
  }
]
```

## 웹 인터페이스 사용법

1. **로컬 서버 실행**
   ```bash
   func start
   ```

2. **웹 페이지 접속**
   - `web/index.html` 파일을 브라우저에서 열기
   - 또는 정적 웹 서버로 서빙

3. **API URL 설정**
   - `index.html` 파일의 19번째 줄에서 API URL을 로컬 주소로 변경:
   ```javascript
   let url = "http://localhost:7071";
   ```

4. **블로그 구독 관리**
   - API를 직접 호출하거나 Postman 등의 도구 사용
   - 또는 추가적인 관리 인터페이스를 구현

## 배포

### Azure Functions 배포

1. **Azure 로그인**
   ```bash
   az login
   ```

2. **리소스 그룹 생성**
   ```bash
   az group create --name rg-rssfeed --location eastus
   ```

3. **Functions 앱 생성**
   ```bash
   az functionapp create \
     --resource-group rg-rssfeed \
     --consumption-plan-location eastus \
     --runtime python \
     --runtime-version 3.9 \
     --functions-version 4 \
     --name your-rssfeed-app \
     --storage-account yourstorageaccount
   ```

4. **배포**
   ```bash
   func azure functionapp publish your-rssfeed-app
   ```

### Azure API Management 설정 (선택사항)

API Management를 통해 API에 대한 인증, 스로틀링, 모니터링을 추가할 수 있습니다.

1. **API Management 인스턴스 생성**
2. **Functions 앱을 백엔드로 등록**
3. **API 정책 설정** (CORS, 인증 등)

## Chapter 9에서 배우는 핵심 내용

### 아이디어 도출 기법
- **마인드 맵**: 블로그 구독의 불편함에서 시작한 아이디어 확장
- **스캠퍼 기법**: 기존 RSS 리더 서비스의 개선점 도출
- **스마트 기법**: 구체적이고 측정 가능한 목표 설정

### 기술적 학습 포인트
1. **XML/RSS 파싱**: 웹에서 제공되는 구조화된 데이터 처리
2. **서버리스 아키텍처**: Azure Functions의 HTTP 트리거와 타이머 트리거 활용
3. **NoSQL 데이터베이스**: Cosmos DB의 MongoDB API 사용
4. **비동기 처리**: 주기적인 데이터 수집 및 처리
5. **웹 API 설계**: RESTful API 원칙에 따른 엔드포인트 설계

### 확장 아이디어
- **카테고리 필터링**: 블로그별 카테고리 분류 및 필터링
- **키워드 알림**: 특정 키워드가 포함된 글에 대한 알림 기능
- **소셜 공유**: 관심 있는 글을 소셜 미디어에 공유
- **개인화**: 사용자별 맞춤 피드 제공
- **모바일 앱**: React Native나 Flutter를 사용한 모바일 클라이언트

## 문제 해결

### 일반적인 문제들

1. **RSS 피드를 찾을 수 없음**
   - 블로그 URL에 `/rss`, `/feed`, `/atom.xml` 추가 시도
   - 웹사이트의 `<link>` 태그에서 피드 URL 확인

2. **Azure Functions가 시작되지 않음**
   ```bash
   # Core Tools 재설치
   npm uninstall -g azure-functions-core-tools
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

3. **Cosmos DB 연결 오류**
   - 연결 문자열 형식 확인
   - 방화벽 설정에서 현재 IP 허용
   - MongoDB API가 활성화되어 있는지 확인

4. **CORS 오류 (웹 인터페이스)**
   - Azure Functions에서 CORS 설정 확인
   - 로컬 개발 시에는 `func start --cors "*"` 사용

5. **타이머 트리거가 작동하지 않음**
   - `host.json`에서 타이머 설정 확인
   - Azure에서는 Always On 설정 필요 (유료 플랜)

### 디버깅 팁

1. **로그 확인**
   ```bash
   func start --verbose
   ```

2. **Azure에서 로그 스트리밍**
   ```bash
   func azure functionapp logstream your-rssfeed-app
   ```

3. **로컬에서 특정 함수 테스트**
   ```bash
   func start --functions fetch_articles
   ```

## 추가 리소스

- [Azure Functions Python 개발자 가이드](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [feedparser 라이브러리 문서](https://feedparser.readthedocs.io/)
- [Azure Cosmos DB MongoDB API](https://docs.microsoft.com/azure/cosmos-db/mongodb/)
- [RSS 2.0 스펙](https://www.rssboard.org/rss-specification)

---

**도서 정보**
- 제목: 해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지
- 저자: 노아론 (github.com/roharon)
- 출판사: 로드북

**구매 링크**
- [교보문고](https://product.kyobobook.co.kr/detail/S000217089414)
- [예스24](https://www.yes24.com/product/goods/149385474)
- [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)
