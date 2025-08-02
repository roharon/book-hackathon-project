# Chapter 5: 주말에 갈 캠핑장 찾기

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![API Gateway](https://img.shields.io/badge/AWS-API%20Gateway-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-6BA539?style=flat&logo=openapi-initiative&logoColor=white)
![Weather API](https://img.shields.io/badge/Weather-API-0052CC?style=flat&logo=api&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 5 프로젝트

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [설치 및 배포](#-설치-및-배포)
- [API 사용법](#-api-사용법)
- [학습 포인트](#-학습-포인트)
- [문제 해결](#-문제-해결)

## 📋 프로젝트 개요

**『해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지』** Chapter 5에서 다루는 캠핑장 검색 및 추천 서비스입니다.

이 프로젝트는 사용자가 원하는 날씨 조건과 일정에 맞는 캠핑장을 찾아주고, 위치 기반으로 주변 캠핑장을 추천하는 서비스를 구현합니다. AWS Lambda와 API Gateway를 활용한 서버리스 아키텍처로 구성되어 있으며, 한국관광공사 API와 기상청 API를 연동하여 실시간 데이터를 제공합니다.

## 🎯 기능

- **캠핑장 검색**: 날씨 조건과 일정에 따른 캠핑장 검색
- **캠핑장 추천**: 사용자 위치 기반 주변 캠핑장 추천
- **날씨 연계**: 실시간 강수 확률을 고려한 스마트 필터링
- **OpenAPI 3.0**: 표준화된 API 스펙 문서 제공

## 🛠️ 기술 스택

- **서버리스 아키텍처**: AWS Lambda, API Gateway
- **외부 API 연동**: 한국관광공사 API, 기상청 API
- **API 문서화**: OpenAPI 3.0
- **프로그래밍 언어**: Python 3.11
- **HTTP 클라이언트**: requests

## 아키텍처

```
사용자 요청
     ↓
API Gateway
     ↓
Lambda Functions (campsiteSearch / campsiteSuggest)
     ↓
External APIs (한국관광공사 API + 기상청 API)
     ↓
데이터 가공 및 필터링
     ↓
JSON 응답 반환
```

## 디렉토리 구조

```
Campsite/
├── campsiteSearch/           # 캠핑장 검색 Lambda 함수
│   └── lambda_function.py
├── campsiteSuggest/          # 캠핑장 추천 Lambda 함수
│   └── lambda_function.py
├── lib/                      # 공통 라이브러리
│   ├── fetch_campsite.py     # 캠핑장 정보 조회
│   ├── fetch_precipitation.py # 강수 확률 조회
│   ├── fetch_suggest_campsite.py # 위치 기반 캠핑장 조회
│   └── search_campsite.py    # 캠핑장 검색 로직
├── python/                   # Python 의존성 패키지
├── lambda_layer.zip          # Lambda 레이어 (의존성 패키지)
├── openapi.yaml             # OpenAPI 3.0 스펙 문서
└── requirements.txt         # Python 의존성 목록
```

## 사용하는 외부 API

### 1. 한국관광공사 API
- **기본 목록 조회**: `http://apis.data.go.kr/B551011/GoCamping/basedList`
- **위치 기반 목록 조회**: `http://apis.data.go.kr/B551011/GoCamping/locationBasedList`

### 2. 기상청 API
- **중기육상예보**: `http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst`
- **지원 예보구역**:
  - 11B00000: 서울, 인천, 경기도
  - 11D10000: 강원도영서
  - 11D20000: 강원도영동
  - 11C20000: 대전, 세종, 충청남도
  - 등등...

## 📖 설치 및 배포

### 1. 환경 변수 설정

AWS Lambda 환경 변수에 다음을 설정해야 합니다:

```bash
service_key=YOUR_OPEN_API_SERVICE_KEY
```

### 2. Lambda 레이어 생성

Python 의존성 패키지들이 포함된 Lambda 레이어를 생성합니다:

```bash
# requirements.txt를 기반으로 의존성 설치
pip install -r requirements.txt -t python/

# Lambda 레이어 zip 파일 생성
zip -r lambda_layer.zip python/
```

### 3. Lambda 함수 배포

1. `campsiteSearch` Lambda 함수 생성
2. `campsiteSuggest` Lambda 함수 생성
3. 생성된 Lambda 레이어를 각 함수에 연결
4. `lib/` 디렉토리를 각 함수에 포함하여 배포

### 4. API Gateway 설정

OpenAPI 3.0 스펙(`openapi.yaml`)을 기반으로 API Gateway를 구성합니다:

- `/campsites/search` → `campsiteSearch` Lambda 함수
- `/campsites/suggests` → `campsiteSuggest` Lambda 함수

## 📚 API 사용법

### 1. 캠핑장 검색

**Endpoint**: `GET /campsites/search`

**Parameters**:
- `weather_type` (string, required): 날씨 유형 ("CLEAR" | "DOWNFALL")
- `begins_at` (string, required): 시작일 (ISO 8601 형식)
- `ends_at` (string, required): 종료일 (ISO 8601 형식)

**Example**:
```bash
GET /campsites/search?weather_type=CLEAR&begins_at=2030-01-01T00:00:00+0900&ends_at=2030-01-02T00:00:00+0900
```

### 2. 캠핑장 추천

**Endpoint**: `GET /campsites/suggests`

**Parameters**:
- `weather_type` (string, required): 날씨 유형 ("CLEAR" | "DOWNFALL")
- `begins_at` (string, required): 시작일 (ISO 8601 형식)
- `ends_at` (string, required): 종료일 (ISO 8601 형식)
- `longitude` (number, required): 경도
- `latitude` (number, required): 위도

**Example**:
```bash
GET /campsites/suggests?weather_type=CLEAR&begins_at=2030-01-01T00:00:00+0900&ends_at=2030-01-02T00:00:00+0900&longitude=127.6403183&latitude=37.2199766
```

### 3. 응답 형식

```json
[
  {
    "name": "OO 캠핑장",
    "allar": 1030,
    "line_intro": "주말에 가기 좋은 근교 캠핑장입니다",
    "image_url": "https://example.com/image.png",
    "created_time": "2023-01-01T00:00:00",
    "updated_time": "2023-01-01T00:00:00",
    "address": "강원도 강릉시",
    "latitude": 37.2199766,
    "longitude": 127.6403183
  }
]
```

## 핵심 구현 로직

### 1. 날씨 기반 필터링

```python
def _filter_campsites(campsites, weather_type):
    seoul_weather_score = fetch_precipitation(current_time, "11B00000")
    gangwon_weather_score = fetch_precipitation(current_time, "11D10000")
    
    # 강수 확률 75% 기준으로 필터링
    if weather_type == 'CLEAR' and weather_score < 75:
        # 맑은 날씨 선호 시 강수 확률 낮은 지역 캠핑장 포함
    elif weather_type == 'DOWNFALL' and weather_score >= 75:
        # 비 오는 날씨 상관없을 시 강수 확률 높은 지역도 포함
```

### 2. 위치 기반 추천

- 사용자 위치로부터 반경 30km 내 캠핑장 검색
- 위도, 경도 좌표를 기반으로 한국관광공사 API 호출
- 거리 순으로 정렬된 결과 반환

### 3. API 호출 최적화

- 강수 확률은 지역별로 한 번만 조회하여 재사용
- 캐싱을 통한 불필요한 API 호출 방지
- 병렬 처리를 통한 응답 시간 단축

## 💡 학습 포인트

### Chapter 5에서 배우는 내용

### 1. 아이디어 도출 기법
- **마인드 맵**: 캠핑 관련 아이디어 확장
- **스캠퍼**: 기존 서비스 개선 아이디어 도출
- **스마트**: 구체적이고 측정 가능한 목표 설정

### 2. 외부 API 활용
- OpenAPI 찾기 및 선택 기준
- API 문서 읽는 방법
- API 키 관리 및 보안

### 3. 서버리스 아키텍처
- AWS Lambda를 활용한 함수형 프로그래밍
- API Gateway와 Lambda 연동
- Lambda 레이어를 통한 의존성 관리

### 4. OpenAPI 3.0 설계
- RESTful API 설계 원칙
- OpenAPI 3.0 스펙 작성법
- API 문서화의 중요성

### 5. API 호출 최적화
- 불필요한 API 호출 최소화
- 데이터 캐싱 전략
- 응답 시간 개선 방법

## 🔧 문제 해결

### 1. API 키 오류
```
Error: 서비스 키가 유효하지 않습니다
```
**해결방법**: 
- 한국관광공사 및 기상청에서 발급받은 API 키가 정확한지 확인
- Lambda 환경 변수 `service_key` 설정 확인

### 2. CORS 오류
```
Error: Access to fetch has been blocked by CORS policy
```
**해결방법**: 
- API Gateway에서 CORS 설정 활성화
- 적절한 Access-Control-Allow-Origin 헤더 추가

### 3. Lambda 타임아웃
```
Error: Task timed out after 30.00 seconds
```
**해결방법**: 
- Lambda 함수 타임아웃 설정 증가
- API 호출 최적화를 통한 실행 시간 단축

### 4. 의존성 패키지 오류
```
Error: No module named 'requests'
```
**해결방법**: 
- Lambda 레이어가 올바르게 연결되었는지 확인
- requirements.txt 의존성이 Lambda 레이어에 포함되었는지 확인

## 🚀 확장 아이디어

1. **사용자 선호도 저장**: 사용자별 선호 캠핑장 유형 학습
2. **실시간 예약 현황**: 캠핑장 실시간 예약 가능 여부 확인
3. **리뷰 시스템**: 사용자 리뷰 및 평점 기능
4. **경로 안내**: 캠핑장까지의 최적 경로 제공
5. **주변 시설 정보**: 마트, 병원 등 주변 편의시설 정보

## 학습 포인트

- 외부 API를 활용한 데이터 연동 방법
- 서버리스 아키텍처의 장점과 한계
- OpenAPI 3.0를 통한 API 설계 및 문서화
- 날씨 데이터를 활용한 비즈니스 로직 구현
- AWS Lambda와 API Gateway 실전 활용

---

**도서 정보**
- 제목: 해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지
- 저자: 노아론 (github.com/roharon)
- 출판사: 로드북
- 구매 링크: [교보문고](https://product.kyobobook.co.kr/detail/S000217089414) | [예스24](https://www.yes24.com/product/goods/149385474) | [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)
