# Chapter 4: 일주일 치 구내식당 식단표, 하루 단위로 확인하기

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-FF9900?style=flat&logo=amazon-dynamodb&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-Bot-4A154B?style=flat&logo=slack&logoColor=white)
![OCR](https://img.shields.io/badge/CLOVA-OCR-03C75A?style=flat&logo=naver&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 4 프로젝트

일주일 치 구내식당 식단표를 OCR로 인식하여 메신저 봇을 통해 하루 단위로 확인할 수 있는 서비스입니다.

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [설치 및 배포](#-설치-및-배포)
- [API 문서](#-api-문서)
- [학습 포인트](#-학습-포인트)
- [문제 해결](#-문제-해결)

## 📋 프로젝트 개요

### Chapter 4에서 배우는 내용

- **아이디어 도출 기법**: 마인드 맵, 스캠퍼(SCAMPER), 스마트(SMART) 기법 실습
- **OCR API 활용**: 네이버 CLOVA OCR을 이용한 식단표 이미지 텍스트 추출
- **서버리스 아키텍처**: AWS Lambda와 DynamoDB를 활용한 경량 서비스 구축
- **메신저 봇 연동**: Slack Bot과의 API 연동을 통한 사용자 인터페이스 제공
- **웹 스크래핑**: BeautifulSoup을 이용한 식단표 이미지 URL 추출

## 🎯 기능

매주 업데이트되는 구내식당 식단표 이미지를 자동으로 수집하고, OCR 기술로 텍스트를 추출하여 메신저를 통해 당일 메뉴를 간편하게 조회할 수 있는 봇 서비스입니다.

### 주요 기능
- 📷 구내식당 웹사이트에서 식단표 이미지 자동 수집
- 🔍 CLOVA OCR API를 통한 이미지 텍스트 인식
- 📅 날짜별 점심/저녁 메뉴 데이터 자동 파싱 및 저장
- 🤖 Slack 메신저를 통한 실시간 메뉴 조회
- ☁️ 서버리스 아키텍처로 관리 부담 최소화

## 🏗️ 아키텍처

```
  🌐 웹사이트  →  ⚡ OCR Lambda  →  🗄️ DynamoDB
    (식단표)      (이미지 처리)        (저장)
                                     ↑
                                     │ 조회
                                     │
  🤖 Slack Bot ← ⚡ 조회 Lambda ───────┘
    (사용자)       (메뉴 응답)
```

## 🛠️ 기술 스택

- **클라우드**: AWS Lambda, DynamoDB
- **언어**: Python 3.9+
- **OCR**: 네이버 CLOVA OCR API
- **웹 스크래핑**: BeautifulSoup4, requests
- **메신저**: Slack Bot API
- **데이터 처리**: boto3 (AWS SDK)

## 📁 프로젝트 구조

```
CafeteriaMenuBot/
├── README.md
├── requirements.txt
├── lambda_layer.zip                    # 공통 의존성 레이어
├── saveCafeteriaMenu/
│   └── lambda_function.py              # 식단표 수집 및 저장
├── getCafeteriaLunchMenu/
│   └── lambda_function.py              # 점심 메뉴 조회
└── getCafeteriaAllOfMenu/
    └── lambda_function.py              # 전체 메뉴 조회
```

### Lambda 함수별 역할

#### 1. saveCafeteriaMenu
- **역할**: 구내식당 웹사이트에서 식단표 이미지를 수집하고 OCR 처리
- **주요 기능**:
  - 웹사이트에서 식단표 이미지 URL 추출
  - CLOVA OCR API로 이미지 텍스트 인식
  - 날짜별/시간대별 메뉴 파싱 및 DynamoDB 저장
- **실행 주기**: 주 1회 (스케줄링)

#### 2. getCafeteriaLunchMenu
- **역할**: 당일 점심 메뉴만 조회하여 Slack으로 응답
- **주요 기능**:
  - DynamoDB에서 당일 점심 메뉴 조회
  - Slack Block Kit 형식으로 응답 포맷팅

#### 3. getCafeteriaAllOfMenu
- **역할**: 당일 전체 메뉴(점심+저녁) 조회하여 Slack으로 응답
- **주요 기능**:
  - DynamoDB에서 당일 전체 메뉴 조회
  - 점심/저녁 메뉴를 구분하여 응답

## 🚀 설치 및 배포

### 사전 요구사항

1. **AWS 계정** 및 AWS CLI 설정
2. **네이버 클라우드 플랫폼** 계정 (CLOVA OCR 사용)
3. **Slack 워크스페이스** 및 Bot 토큰

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone https://github.com/roharon/book-hackathon-project.git
cd CafeteriaMenuBot

# Python 의존성 설치
pip install -r requirements.txt
```

### 2. AWS 리소스 생성

#### DynamoDB 테이블 생성
```bash
aws dynamodb create-table \
    --table-name cafeteria_menu \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

#### Lambda 레이어 업로드
```bash
aws lambda publish-layer-version \
    --layer-name cafeteria-menu-dependencies \
    --zip-file fileb://lambda_layer.zip \
    --compatible-runtimes python3.9
```

### 3. Lambda 함수 배포

각 함수별로 배포 패키지를 생성하고 업로드합니다.

#### saveCafeteriaMenu 함수
```bash
cd saveCafeteriaMenu
zip -r ../saveCafeteriaMenu.zip .
cd ..

aws lambda create-function \
    --function-name saveCafeteriaMenu \
    --zip-file fileb://saveCafeteriaMenu.zip \
    --handler lambda_function.lambda_handler \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
    --layers arn:aws:lambda:REGION:ACCOUNT:layer:cafeteria-menu-dependencies:1 \
    --environment Variables='{
        "CLOVA_OCR_URL":"YOUR_CLOVA_OCR_ENDPOINT",
        "CLOVA_OCR_SECRET":"YOUR_CLOVA_OCR_SECRET"
    }'
```

#### 메뉴 조회 함수들
```bash
# getCafeteriaLunchMenu
cd getCafeteriaLunchMenu
zip -r ../getCafeteriaLunchMenu.zip .
cd ..

aws lambda create-function \
    --function-name getCafeteriaLunchMenu \
    --zip-file fileb://getCafeteriaLunchMenu.zip \
    --handler lambda_function.lambda_handler \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
    --layers arn:aws:lambda:REGION:ACCOUNT:layer:cafeteria-menu-dependencies:1

# getCafeteriaAllOfMenu (동일한 방식으로 배포)
```

### 4. API Gateway 설정

Slack Bot과 연동하기 위한 REST API 엔드포인트를 생성합니다.

```bash
# API Gateway 생성
aws apigateway create-rest-api --name cafeteria-menu-api

# 리소스 및 메서드 생성
# /lunch-menu (POST) -> getCafeteriaLunchMenu
# /all-menu (POST) -> getCafeteriaAllOfMenu
```

## 🔧 환경 변수 설정

### CLOVA OCR API 설정

1. 네이버 클라우드 플랫폼에서 CLOVA OCR 서비스 신청
2. API Gateway 도메인과 Secret Key 발급
3. Lambda 함수에 환경 변수 설정:
   - `CLOVA_OCR_URL`: OCR API 엔드포인트
   - `CLOVA_OCR_SECRET`: OCR API 시크릿 키

### Slack Bot 설정

1. Slack App 생성 및 Bot Token 발급
2. Slash Command 설정:
   - `/점심메뉴`: 점심 메뉴 조회 명령
   - `/전체메뉴`: 전체 메뉴 조회 명령
3. Request URL을 API Gateway 엔드포인트로 설정

## 📝 API 문서

### 점심 메뉴 조회
```
POST /lunch-menu
Content-Type: application/x-www-form-urlencoded

Response:
{
  "response_type": "in_channel",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*점심 메뉴*"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "메뉴 내용..."
      }
    }
  ]
}
```

### 전체 메뉴 조회
```
POST /all-menu
Content-Type: application/x-www-form-urlencoded

Response: 점심 + 저녁 메뉴 블록 조합
```

## 🎓 학습 포인트

### 1. OCR 기술 활용
- 이미지에서 텍스트를 추출하는 OCR의 원리와 활용법
- 네이버 CLOVA OCR API의 테이블 인식 기능 활용
- OCR 결과 데이터의 정제 및 파싱 기법

### 2. 서버리스 아키텍처
- AWS Lambda의 이벤트 기반 처리 모델
- DynamoDB NoSQL 데이터베이스 설계
- Lambda Layer를 통한 의존성 관리

### 3. 웹 스크래핑
- BeautifulSoup을 이용한 HTML 파싱
- 동적 웹사이트에서 데이터 추출하기
- 웹 스크래핑 시 고려사항 (로봇 배제 표준, 요청 빈도 등)

### 4. 메신저 봇 개발
- Slack Bot API와 Block Kit 활용
- Slash Command 구현 및 응답 포맷팅
- 사용자 친화적인 메시지 디자인

### 5. 데이터 처리 및 파싱
- 정규표현식을 이용한 텍스트 패턴 매칭
- 날짜/시간 데이터 처리
- 반복적인 데이터 구조 파싱

## 🔍 문제 해결 가이드

### OCR 인식률이 낮은 경우
- 이미지 품질 확인 (해상도, 명도, 대비)
- OCR API 파라미터 조정 (`enableTableDetection` 등)
- 전처리 과정 추가 (이미지 크기 조정, 노이즈 제거)

### Lambda 함수 시간 초과
- 타임아웃 설정 증가 (최대 15분)
- 메모리 할당량 증가
- 처리 로직 최적화 (병렬 처리, 캐싱)

### DynamoDB 액세스 오류
- IAM 역할 권한 확인
- 테이블명 및 키 스키마 확인
- VPC 설정 시 엔드포인트 확인

### Slack Bot 응답 지연
- Lambda 콜드 스타트 최소화
- 응답 시간 3초 이내 유지
- 필요시 비동기 처리 구현

## 📚 관련 자료

- [AWS Lambda 개발자 가이드](https://docs.aws.amazon.com/lambda/)
- [DynamoDB 개발자 가이드](https://docs.aws.amazon.com/dynamodb/)
- [네이버 CLOVA OCR API 문서](https://www.ncloud.com/product/aiService/ocr)
- [Slack API 문서](https://api.slack.com/)

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

이 프로젝트를 통해 OCR 기술과 서버리스 아키텍처를 활용한 실용적인 서비스 개발 경험을 쌓아보세요!
