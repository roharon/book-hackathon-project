# Chapter 6: 달리기 측정 앱 간의 기록 연동하기

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![Amazon S3](https://img.shields.io/badge/AWS-S3-FF9900?style=flat&logo=amazon-s3&logoColor=white)
![Nike Run Club](https://img.shields.io/badge/Nike-Run%20Club-000000?style=flat&logo=nike&logoColor=white)
![Strava](https://img.shields.io/badge/Strava-FC4C02?style=flat&logo=strava&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 6 프로젝트

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [설치 및 배포](#-설치-및-배포)
- [사용법](#-사용법)
- [학습 포인트](#-학습-포인트)
- [문제 해결](#-문제-해결)

## 📋 프로젝트 개요

이 프로젝트는 『해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지』 **Chapter 6**에서 다루는 프로젝트입니다.

Nike Run Club과 Strava 간의 러닝 기록을 자동으로 동기화하는 서비스로, 서로 다른 플랫폼에 분산된 운동 데이터를 하나로 통합할 수 있습니다.

RunnerSyncer는 Nike Run Club에서 Strava로 러닝 기록을 자동 연동하는 서비스입니다. Nike Run Club의 활동 데이터를 GPX 형식으로 변환하여 Strava에 업로드하는 과정을 AWS 서버리스 아키텍처로 구현했습니다.

## 🎯 기능

- **OAuth 2.0 인증**: Strava API 연동을 위한 안전한 인증
- **활동 데이터 추출**: Nike Run Club API에서 러닝 기록 조회
- **GPX 변환**: Nike 데이터를 Strava 호환 GPX 형식으로 변환
- **자동 업로드**: S3 이벤트 트리거를 통한 자동 Strava 업로드
- **실시간 처리**: 이벤트 기반 비동기 처리 시스템

## 🛠️ 기술 스택
- **Backend**: AWS Lambda (Python 3.9)
- **Storage**: Amazon S3
- **API**: Nike Run Club API, Strava API
- **Authentication**: OAuth 2.0
- **Libraries**: stravalib, boto3, requests

### 아키텍처 구성
```
Nike Run Club API → Lambda (fetchActivity) → S3 (GPX 저장) → S3 Event → Lambda (uploadActivity) → Strava API
                                                    ↑
                          Lambda (authorizeStrava) ← User Authorization
```

### AWS Lambda 함수들
1. **authorizeStrava**: Strava OAuth 인증 처리
2. **fetchActivity**: Nike Run Club에서 활동 데이터 조회 및 GPX 변환
3. **uploadActivity**: S3 이벤트 트리거로 Strava에 활동 업로드

## 📖 설치 및 배포

### 사전 요구사항

### 필수 계정 및 API 키
- **Strava 개발자 계정**
  - [Strava API](https://developers.strava.com/) 가입
  - Client ID 및 Client Secret 발급
- **Nike Developer 계정**
  - Nike Developer API 접근 권한
- **AWS 계정**
  - Lambda, S3, IAM 권한

### 환경 변수 설정
```bash
STRAVA_CLIENT_ID=your_strava_client_id
STRAVA_CLIENT_SECRET=your_strava_client_secret
S3_BUCKET_NAME=your_s3_bucket_name
```

### 1. 프로젝트 클론
```bash
git clone https://github.com/your-repo/book-hackathon-project.git
cd book-hackathon-project/RunnerSyncer
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. Lambda 레이어 준비
```bash
# lambda_layer.zip에 필요한 패키지들이 포함되어 있습니다
unzip lambda_layer.zip
```

### 4. AWS Lambda 함수 배포

#### authorizeStrava 함수
```bash
cd authorizeStrava
zip -r authorize-function.zip .
aws lambda create-function \
  --function-name authorizeStrava \
  --runtime python3.9 \
  --role arn:aws:iam::your-account:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://authorize-function.zip
```

#### fetchActivity 함수
```bash
cd fetchActivity
zip -r fetch-function.zip .
aws lambda create-function \
  --function-name fetchActivity \
  --runtime python3.9 \
  --role arn:aws:iam::your-account:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://fetch-function.zip
```

#### uploadActivity 함수
```bash
cd uploadActivity
zip -r upload-function.zip .
aws lambda create-function \
  --function-name uploadActivity \
  --runtime python3.9 \
  --role arn:aws:iam::your-account:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://upload-function.zip
```

### 5. S3 버킷 생성 및 이벤트 설정
```bash
# S3 버킷 생성
aws s3 mb s3://your-runner-syncer-bucket

# S3 이벤트 알림 설정 (GPX 파일 업로드 시 uploadActivity Lambda 트리거)
aws s3api put-bucket-notification-configuration \
  --bucket your-runner-syncer-bucket \
  --notification-configuration file://s3-event-config.json
```

## 📚 사용법

### 1. Strava 인증
1. 웹 브라우저에서 `index.html` 열기
2. "Sync to Strava" 버튼 클릭
3. Strava OAuth 인증 완료
4. 발급된 액세스 토큰 저장

### 2. Nike Run Club 토큰 설정
```javascript
// Nike 액세스 토큰을 입력 필드에 입력
document.getElementById("nike-access-token").value = "your_nike_token";
```

### 3. 동기화 실행
API 엔드포인트로 POST 요청:
```bash
curl -X POST https://your-api-gateway-url/sync \
  -H "Content-Type: application/json" \
  -d '{
    "strava_access_token": "your_strava_token",
    "nike_access_token": "your_nike_token"
  }'
```

### 워크플로우
1. Nike Run Club에서 러닝 활동 데이터 조회
2. GPX 형식으로 데이터 변환
3. S3에 GPX 파일 업로드 (메타데이터에 Strava 토큰 포함)
4. S3 이벤트가 uploadActivity Lambda 자동 트리거
5. Strava API로 활동 업로드 완료

## 📚 API 문서

### 인증 엔드포인트
```
GET /authorize?code={authorization_code}
```
- Strava OAuth 인증 코드를 액세스 토큰으로 교환

### 동기화 엔드포인트
```
POST /sync
Content-Type: application/json

{
  "strava_access_token": "string",
  "nike_access_token": "string"
}
```

자세한 API 스펙은 `openapi.yaml` 파일을 참조하세요.

## 🔧 핵심 구현 요소

### 1. 이벤트 기반 아키텍처
- S3 객체 생성 이벤트를 트리거로 사용
- 비동기 처리로 확장성 확보
- 각 Lambda 함수의 단일 책임 원칙 적용

### 2. GPX 데이터 변환
Nike Run Club API의 메트릭 데이터를 GPX 형식으로 변환:
```python
def to_gpx(data):
    # 위도, 경도, 고도, 시간 데이터 추출
    # GPX XML 형식으로 변환
    return GPX_TEMPLATE.format(start_time, name, track_points)
```

### 3. 메타데이터 활용
S3 객체의 메타데이터에 Strava 액세스 토큰 저장하여 Lambda 간 데이터 전달:
```python
s3_client.upload_fileobj(
    io.BytesIO(gpx_data),
    bucket, key,
    ExtraArgs={"Metadata": {"strava-access-token": token}}
)
```

## 💡 학습 포인트

### Chapter 6에서 학습할 수 있는 내용

### 아이디어 발상 기법
- **마인드 맵**: 러닝 앱 생태계 분석
- **스캠퍼 기법**: 기존 서비스 개선 아이디어 도출
- **스마트 기법**: 구체적이고 달성 가능한 목표 설정

### 기술적 학습 포인트
- **이벤트 기반 아키텍처**: S3 이벤트를 활용한 서버리스 워크플로우
- **OAuth 2.0 인증**: 제3자 API 안전한 연동 방법
- **데이터 변환**: 서로 다른 API 형식 간 데이터 매핑
- **AWS Lambda**: 서버리스 컴퓨팅 활용법
- **비동기 처리**: 이벤트 트리거 기반 처리 흐름

### 확장 가능성
- 멀티 사용자 지원 구조로 발전
- 연동 상태 모니터링 시스템 추가
- 다양한 러닝 앱 플랫폼 지원 확대

## 🔍 문제 해결

### 자주 발생하는 문제

#### 1. Strava OAuth 인증 실패
```
Error: Invalid client credentials
```
**해결방법**: 
- Strava 개발자 설정에서 redirect URI 확인
- Client ID와 Secret 재확인

#### 2. Nike API 접근 거부
```
Error: 401 Unauthorized
```
**해결방법**:
- Nike 액세스 토큰 유효성 확인
- API 요청 헤더 형식 점검

#### 3. S3 이벤트 트리거 작동 안함
**해결방법**:
- Lambda 함수 권한 설정 확인
- S3 버킷 이벤트 알림 설정 재확인
- CloudWatch 로그에서 오류 메시지 확인

#### 4. GPX 변환 오류
```
Error: Missing latitude/longitude data
```
**해결방법**:
- Nike 활동 데이터에 GPS 정보 포함 여부 확인
- 메트릭 데이터 구조 변경 대응

### 디버깅 팁
```bash
# CloudWatch 로그 확인
aws logs filter-log-events \
  --log-group-name /aws/lambda/uploadActivity \
  --start-time 1640995200000

# S3 객체 메타데이터 확인
aws s3api head-object \
  --bucket your-bucket \
  --key gpx/activity_id.gpx
```

## 📖 관련 자료

- **Chapter 6 전체 내용**: 책에서 상세한 구현 과정과 설계 원리 학습
- **Strava API 문서**: https://developers.strava.com/docs/
- **AWS Lambda 개발자 가이드**: https://docs.aws.amazon.com/lambda/
- **OAuth 2.0 스펙**: https://oauth.net/2/

## 🤝 기여하기

이 프로젝트는 해커톤 학습을 위한 예제 프로젝트입니다. 
개선 사항이나 버그 발견 시 이슈를 등록해 주세요.

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었으며, 『해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지』 도서의 예제 코드입니다.

---

**저자**: 노아론 (github.com/roharon)  
**출판사**: 로드북  
**도서 구매**: [교보문고](https://product.kyobobook.co.kr/detail/S000217089414) | [예스24](https://www.yes24.com/product/goods/149385474) | [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)