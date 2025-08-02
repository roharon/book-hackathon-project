# Chapter 7: 구글 드라이브의 공유 문서함 초대 자동화하기

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![API Gateway](https://img.shields.io/badge/AWS-API%20Gateway-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![Google Drive](https://img.shields.io/badge/Google-Drive%20API-4285F4?style=flat&logo=google-drive&logoColor=white)
![EventBridge](https://img.shields.io/badge/AWS-EventBridge-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![SES](https://img.shields.io/badge/AWS-SES-FF9900?style=flat&logo=amazon-aws&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 7 프로젝트

팀원들과 문서를 공유할 때마다 일일이 초대하는 번거로움을 해결하는 자동화 시스템입니다. 웹 인터페이스를 통해 간단하게 이메일 주소와 인증 코드를 입력하면 자동으로 구글 드라이브 공유 폴더에 초대되며, 정기적으로 활동 리포트를 받아볼 수 있습니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [아키텍처](#아키텍처)
- [사전 준비](#사전-준비)
- [설치 및 배포](#설치-및-배포)
- [사용 방법](#사용-방법)
- [API 명세](#api-명세)
- [학습 포인트](#학습-포인트)
- [문제 해결](#문제-해결)

## 📋 프로젝트 개요

### Chapter 7에서 배우는 내용

이 프로젝트는 해커톤에서 자주 발생하는 **반복적인 업무를 자동화**하는 방법을 학습합니다:

- **아이디어 도출**: 마인드 맵, 스캠퍼, 스마트 기법을 활용한 문제 정의
- **외부 API 연동**: Google Drive API와 Google Drive Activity API 활용
- **서버리스 아키텍처**: AWS Lambda를 활용한 이벤트 기반 처리
- **자동화 스케줄링**: EventBridge를 활용한 정기 작업 실행
- **이메일 알림**: SES를 활용한 리포트 발송
- **사용자 스토리 기반 개발**: 실제 사용자 요구사항에 맞는 기능 구현

### 해결하고자 하는 문제

- 팀 프로젝트 시 매번 수동으로 구글 드라이브 폴더 공유
- 누가 언제 폴더에 접근했는지 추적의 어려움
- 관리자의 반복적인 초대 작업으로 인한 시간 낭비

## 🎯 기능

### 1. 웹 기반 자동 초대
- 간단한 웹 인터페이스를 통한 이메일 주소 입력
- 인증 코드를 통한 보안 강화
- 실시간 이메일 형식 검증

### 2. 구글 드라이브 자동 공유
- Google Drive API를 통한 자동 권한 부여
- 'commenter' 권한으로 안전한 접근 제어
- 초대 완료 시 자동 이메일 알림

### 3. 활동 리포트 자동 발송
- 주간 단위 공유 폴더 활동 리포트
- EventBridge를 통한 정기적 실행
- SES를 통한 HTML 형식 이메일 발송

## 🛠️ 기술 스택

### Backend
- **AWS Lambda**: 서버리스 함수 실행 환경
- **Python 3.9**: 주요 개발 언어
- **requests**: HTTP 클라이언트 라이브러리
- **boto3**: AWS SDK for Python

### Cloud Services
- **API Gateway**: REST API 엔드포인트 제공
- **EventBridge**: 스케줄 기반 이벤트 트리거
- **SES (Simple Email Service)**: 이메일 발송 서비스
- **Lambda Layers**: 공통 라이브러리 관리

### External APIs
- **Google Drive API v3**: 파일 권한 관리
- **Google Drive Activity API v2**: 활동 로그 조회
- **Google OAuth 2.0**: 인증 토큰 관리

### Frontend
- **HTML5 + JavaScript**: 웹 인터페이스
- **Bulma CSS**: 반응형 UI 프레임워크
- **Font Awesome**: 아이콘 라이브러리

## 아키텍처

```
[웹 브라우저] → [API Gateway] → [Lambda: 공유 처리]
                                      ↓
                              [Google Drive API]

[EventBridge] → [Lambda: 리포트 생성] → [SES] → [관리자 이메일]
    ↓               ↓
[스케줄 설정]  [Google Drive Activity API]
```

### 주요 구성 요소

1. **shareGoogleDriveFolder**: 웹에서 요청받은 이메일을 구글 드라이브 폴더에 자동 초대
2. **reportGoogleDriveFolderHistory**: 정기적으로 폴더 활동 내역을 조회하여 리포트 발송
3. **API Gateway**: RESTful API 엔드포인트 제공
4. **EventBridge**: 주간 리포트 발송을 위한 스케줄 트리거

## 사전 준비

### 1. AWS 계정 설정
- AWS 계정 및 CLI 설정
- 다음 AWS 서비스 사용 권한 필요:
  - Lambda
  - API Gateway
  - EventBridge
  - SES
  - IAM

### 2. Google Cloud Platform 설정

#### Google Drive API 활성화
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. API 및 서비스 > 라이브러리에서 다음 API 활성화:
   - Google Drive API
   - Google Drive Activity API

#### OAuth 2.0 인증 정보 생성
1. API 및 서비스 > 사용자 인증 정보
2. '사용자 인증 정보 만들기' > 'OAuth 클라이언트 ID'
3. 애플리케이션 유형: 웹 애플리케이션
4. 승인된 리디렉션 URI 설정
5. 클라이언트 ID와 클라이언트 보안 비밀번호 저장

#### 리프레시 토큰 획득
```bash
# OAuth 동의 화면을 통해 리프레시 토큰 획득
# 상세한 과정은 Google OAuth 2.0 문서 참조
```

### 3. 환경 변수 준비
다음 정보들을 Lambda 환경 변수로 설정해야 합니다:

```
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
REFRESH_TOKEN=your_refresh_token
FILE_ID=your_google_drive_folder_id
VERIFY_CODE=your_custom_verification_code
REGION=ap-northeast-2
ADMIN_EMAIL=your_admin_email@example.com
```

## 📖 설치 및 배포

### 1. 프로젝트 클론
```bash
git clone https://github.com/roharon/book-hackathon-project.git
cd GoogleDriveInvitation
```

### 2. Lambda Layer 생성
```bash
# Python 의존성 패키지 설치
pip install -U -r requirements.txt -t ./python

# Lambda Layer 패키징
zip -9 -r lambda_layer.zip ./python
```

### 3. Lambda 함수 배포

#### shareGoogleDriveFolder 함수
1. AWS Lambda 콘솔에서 새 함수 생성
2. 런타임: Python 3.9
3. 코드: `shareGoogleDriveFolder/lambda_handler.py` 업로드
4. 환경 변수 설정
5. Lambda Layer 연결

#### reportGoogleDriveFolderHistory 함수
1. 새 Lambda 함수 생성
2. 코드: `reportGoogleDriveFolderHistory/lambda_handler.py` 업로드
3. 동일한 환경 변수 설정
4. SES 권한 추가

### 4. API Gateway 설정
1. REST API 생성
2. `/share` POST 메서드 생성
3. Lambda 프록시 통합 설정
4. CORS 활성화
5. API 배포

### 5. EventBridge 규칙 설정
```bash
# 매주 월요일 오전 9시 실행 (UTC 기준 0시)
aws events put-rule \
  --name google-drive-weekly-report \
  --schedule-expression "cron(0 0 ? * MON *)"

# Lambda 함수를 타겟으로 설정
aws events put-targets \
  --rule google-drive-weekly-report \
  --targets "Id"="1","Arn"="arn:aws:lambda:region:account:function:reportGoogleDriveFolderHistory"
```

### 6. 웹 인터페이스 배포
1. `index.html`의 API_ENDPOINT를 실제 API Gateway URL로 수정
2. 웹 서버 또는 S3 정적 웹사이트로 배포

## 사용 방법

### 웹 인터페이스를 통한 초대

1. 웹 브라우저에서 배포된 웹사이트 접속
2. 초대할 이메일 주소 입력
3. 관리자로부터 받은 인증 코드 입력
4. '확인' 버튼 클릭
5. 성공 시 해당 이메일로 구글 드라이브 초대 메일 발송

### API 직접 호출

```bash
curl -X POST https://your-api-gateway-url/share \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "verify_code": "123456"
  }'
```

### 리포트 확인

- 매주 월요일 오전 9시(UTC 0시)에 관리자 이메일로 리포트 자동 발송
- 리포트 내용: 공유 폴더의 최근 활동 내역

## 📚 API 명세

API 상세 명세는 `openapi.yaml` 파일을 참조하세요.

### POST /share
구글 드라이브 폴더에 이메일 주소를 자동으로 초대합니다.

**Request Body:**
```json
{
  "email": "user@example.com",
  "verify_code": "123456"
}
```

**Responses:**
- `201`: 초대 성공
- `400`: 이메일 형식 오류 또는 인증 코드 불일치

## 💡 학습 포인트

### 1. 이벤트 기반 아키텍처
- **서버리스 컴퓨팅**: Lambda를 활용한 비용 효율적인 백엔드 구성
- **이벤트 스케줄링**: EventBridge를 통한 정기 작업 자동화
- **마이크로서비스**: 기능별로 분리된 Lambda 함수 설계

### 2. 외부 API 연동
- **OAuth 2.0 인증**: Google API 인증 및 토큰 관리
- **REST API 호출**: requests 라이브러리를 활용한 HTTP 통신
- **에러 핸들링**: API 호출 실패 시 적절한 예외 처리

### 3. 보안 고려사항
- **인증 코드**: 무분별한 접근 방지를 위한 검증 메커니즘
- **환경 변수**: 민감한 정보의 안전한 관리
- **권한 제어**: 최소 권한 원칙 적용 (commenter 권한)

### 4. 사용자 경험 개선
- **실시간 검증**: JavaScript를 통한 이메일 형식 실시간 확인
- **시각적 피드백**: Bulma CSS를 활용한 사용자 친화적 UI
- **자동 알림**: 초대 완료 시 자동 이메일 알림

### 5. 운영 자동화
- **모니터링**: 정기 리포트를 통한 사용 현황 추적
- **로깅**: CloudWatch를 통한 Lambda 함수 실행 로그 관리
- **알림**: SES를 통한 이메일 기반 알림 시스템

## 🔧 문제 해결

### Google API 관련 오류

**문제**: `token을 가져올 수 없습니다` 오류
**해결방법**: 
- Google Cloud Console에서 OAuth 2.0 클라이언트 ID 확인
- 리프레시 토큰이 유효한지 확인
- API가 활성화되었는지 확인

**문제**: `공유 폴더 초대에 실패하였습니다` 오류
**해결방법**:
- FILE_ID 환경 변수가 올바른 Google Drive 폴더 ID인지 확인
- 해당 폴더에 대한 소유자 권한이 있는지 확인

### AWS 서비스 관련 오류

**문제**: Lambda 함수가 실행되지 않음
**해결방법**:
- IAM 역할에 필요한 권한이 있는지 확인
- 환경 변수가 모두 설정되었는지 확인
- CloudWatch 로그에서 오류 메시지 확인

**문제**: SES 이메일 발송 실패
**해결방법**:
- SES에서 발신자 이메일 주소가 검증되었는지 확인
- SES가 샌드박스 모드가 아닌지 확인 (프로덕션 환경)
- IAM 역할에 SES 권한이 있는지 확인

### 일반적인 오류

**문제**: CORS 오류가 발생함
**해결방법**:
- API Gateway에서 CORS가 활성화되었는지 확인
- OPTIONS 메서드가 설정되었는지 확인

**문제**: 웹 인터페이스에서 API 호출 실패
**해결방법**:
- `index.html`의 API_ENDPOINT가 올바른 API Gateway URL인지 확인
- 네트워크 탭에서 실제 요청/응답 확인

## 추가 학습 자료

- [Google Drive API 문서](https://developers.google.com/drive/api)
- [AWS Lambda 개발자 가이드](https://docs.aws.amazon.com/lambda/)
- [EventBridge 사용자 가이드](https://docs.aws.amazon.com/eventbridge/)
- [Chapter 7 상세 내용](../): 해커톤 서적 7장 참조

---

**Chapter 7에서 중요하게 다루는 개념:**
- 반복 업무의 자동화를 통한 팀 생산성 향상
- 서버리스 아키텍처를 활용한 비용 효율적인 솔루션 구현
- 외부 API와의 안전한 연동 방법
- 이벤트 기반 시스템 설계 및 구현
