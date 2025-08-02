# Chapter 8: 1인 가구의 장 함께 보기

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![AWS SAM](https://img.shields.io/badge/AWS-SAM-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![API Gateway](https://img.shields.io/badge/AWS-API%20Gateway-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![DocumentDB](https://img.shields.io/badge/AWS-DocumentDB-FF9900?style=flat&logo=amazon-documentdb&logoColor=white)
![SNS](https://img.shields.io/badge/AWS-SNS-FF9900?style=flat&logo=amazon-aws&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 8 프로젝트

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [설치 및 배포](#-설치-및-배포)
- [API 문서](#-api-문서)
- [학습 포인트](#-학습-포인트)
- [문제 해결](#-문제-해결)

## 📋 프로젝트 개요

이 프로젝트는 《해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지》의 Chapter 8에서 다루는 **1인 가구의 장 함께 보기** 서비스입니다. 

혼자 사는 1인 가구들이 장을 볼 때 필요한 물건들을 함께 구매할 수 있도록 그룹을 만들고 참여할 수 있는 플랫폼을 제공합니다. 사용자들은 특정 장소(마트)와 시간에 맞춰 그룹을 만들거나 참여할 수 있으며, SMS 알림을 통해 실시간으로 소통할 수 있습니다.

## 🎯 기능

### 핵심 기능
- **그룹 생성 및 관리**: 장보기 그룹을 생성하고 관리
- **그룹 참여**: 기존 그룹에 참여하여 함께 장보기
- **참여 조건 설정**: 선호하는 장소(마트) 등의 조건 설정
- **SMS 알림**: 그룹 활동에 대한 실시간 SMS 알림
- **사용자 인증**: API 요청에 대한 인증 및 권한 관리

### API 엔드포인트
- `POST /groups` - 새로운 그룹 생성
- `GET /groups` - 그룹 목록 조회
- `GET /groups/{id}` - 특정 그룹 조회
- `DELETE /groups/{id}` - 그룹 삭제
- `POST /groups/{id}/participate` - 그룹 참여
- `GET /participation_conditions/me` - 내 참여 조건 조회
- `PUT /participation_conditions/me` - 내 참여 조건 수정

## 🛠️ 기술 스택

### 서버리스 아키텍처
이 프로젝트는 AWS의 서버리스 기술을 활용하여 구축되었습니다:

- **AWS SAM (Serverless Application Model)**: 서버리스 애플리케이션 개발 및 배포
- **AWS Lambda**: 각 API 기능별 마이크로서비스 구현
- **Amazon API Gateway**: REST API 엔드포인트 제공
- **Amazon DocumentDB (MongoDB 호환)**: 그룹 및 사용자 데이터 저장
- **Amazon SNS**: SMS 알림 발송
- **Python 3.10**: Lambda 함수 런타임

### 마이크로서비스 구조
각 기능별로 독립적인 Lambda 함수로 구현:

```
GroceryStore/
├── addGroup/           # 그룹 생성
├── authorizer/         # API 인증
├── deleteGroup/        # 그룹 삭제
├── getGroup/          # 그룹 조회
├── getGroupList/      # 그룹 목록 조회
├── getMyParticipationConditions/    # 참여 조건 조회
├── modifyMyParticipationConditions/ # 참여 조건 수정
├── participateGroup/   # 그룹 참여
└── sendSms/           # SMS 발송
```

## 사전 요구사항

### 필수 도구
- **AWS CLI**: AWS 리소스 관리를 위한 명령줄 도구
- **SAM CLI**: 서버리스 애플리케이션 개발 및 배포 도구
- **Python 3.10+**: Lambda 함수 개발을 위한 Python 환경
- **Docker**: SAM 로컬 테스트를 위한 컨테이너 환경

### AWS 서비스 설정
- **AWS 계정**: 유효한 AWS 계정
- **DocumentDB 클러스터**: MongoDB 호환 데이터베이스
- **SNS 서비스**: SMS 발송을 위한 권한 설정
- **IAM 역할**: Lambda 실행을 위한 적절한 권한

## 📖 설치 및 배포

### 1. 프로젝트 클론
```bash
git clone https://github.com/roharon/book-hackathon-project.git
cd GroceryStore
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
각 Lambda 함수에서 사용할 환경 변수를 설정합니다:
```bash
export DOCUMENT_DB_CONNECTION_STRING="your-documentdb-connection-string"
```

### 4. SAM을 이용한 배포

#### 로컬 테스트
```bash
# API Gateway 로컬 실행
sam local start-api

# 특정 함수 로컬 테스트
sam local invoke AddGroup -e addGroup/events/event.json
```

#### AWS 배포
```bash
# 빌드
sam build

# 배포 (최초)
sam deploy --guided

# 업데이트 배포
sam deploy
```

### 5. 개별 Lambda 함수 배포 (선택사항)
각 함수 디렉토리에서 개별 배포도 가능합니다:
```bash
cd addGroup
sh ./build.sh
aws lambda update-function-code --function-name addGroup --zip-file fileb://addGroup.zip
```

## API 사용 가이드

### 인증
모든 API 요청은 `authorizer` Lambda 함수를 통해 인증됩니다. 요청 헤더에 적절한 인증 토큰을 포함해야 합니다.

### 그룹 생성 예시
```bash
curl -X POST https://your-api-gateway-url/groups \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "name": "홍대 이마트 장보기",
    "participation_conditions": [
      {
        "place": "이마트 홍대점"
      }
    ]
  }'
```

### 그룹 참여 예시
```bash
curl -X POST https://your-api-gateway-url/groups/{group-id}/participate \
  -H "Authorization: Bearer your-token"
```

## Lambda 함수별 상세 설명

### addGroup
- **기능**: 새로운 장보기 그룹 생성
- **입력**: 그룹명, 참여 조건
- **출력**: 생성된 그룹 정보
- **데이터 검증**: 그룹명 문자열 검증, 참여 조건 배열 검증

### authorizer
- **기능**: API 요청 인증 및 권한 검증
- **입력**: 인증 토큰
- **출력**: 인증 결과 및 사용자 정보
- **역할**: 모든 API 요청의 게이트키퍼 역할

### participateGroup
- **기능**: 기존 그룹에 참여
- **입력**: 그룹 ID
- **출력**: 참여 결과
- **로직**: 중복 참여 방지, 그룹 존재 여부 확인

### sendSms
- **기능**: SMS 알림 발송
- **입력**: 전화번호, 발신자, 메시지 내용
- **출력**: 발송 결과
- **서비스**: Amazon SNS 활용

### getGroup / getGroupList
- **기능**: 그룹 정보 조회
- **필터**: 지역, 시간, 참여 조건별 필터링 가능
- **정렬**: 생성일시, 참여자 수 등으로 정렬

### getMyParticipationConditions / modifyMyParticipationConditions
- **기능**: 사용자별 참여 조건 관리
- **설정 항목**: 선호 장소, 시간대, 기타 조건
- **개인화**: 사용자별 맞춤 설정

## 데이터 모델

### 그룹 (Groups Collection)
```json
{
  "_id": "ObjectId",
  "group_name": "string",
  "participation_conditions": [
    {
      "place": "string"
    }
  ],
  "owner_email": "string",
  "members": ["email1", "email2"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 참여 조건 (Participation Conditions)
```json
{
  "place": "이마트 홍대점",
  "preferred_time": "오후 7시",
  "max_budget": 50000
}
```

## Chapter 8 학습 포인트

### 1. 서버리스 아키텍처의 장점
- **비용 효율성**: 사용한 만큼만 비용 지불
- **자동 확장**: 트래픽에 따른 자동 스케일링
- **운영 부담 감소**: 서버 관리 불필요

### 2. 마이크로서비스 패턴
- **기능별 분리**: 각 Lambda 함수가 단일 책임 원칙 따름
- **독립적 배포**: 각 함수를 독립적으로 업데이트 가능
- **장애 격리**: 한 기능의 오류가 전체 시스템에 영향 주지 않음

### 3. AWS SAM 활용
- **Infrastructure as Code**: 코드로 인프라 관리
- **로컬 개발 환경**: 클라우드 환경을 로컬에서 시뮬레이션
- **배포 자동화**: 일관된 배포 프로세스

### 4. API 설계 원칙
- **RESTful 설계**: HTTP 메서드와 리소스 중심 설계
- **OpenAPI 스펙**: API 문서화 및 계약 정의
- **인증/인가**: 보안을 고려한 API 설계

### 5. Lambda 함수 간 데이터 전달
- **이벤트 기반**: API Gateway에서 Lambda로 이벤트 전달
- **JSON 직렬화**: 구조화된 데이터 교환
- **상태 관리**: DocumentDB를 통한 영속적 데이터 저장

## 문제 해결 가이드

### 1. 배포 관련 문제

#### SAM 배포 실패
```bash
# 템플릿 검증
sam validate

# 상세 로그로 배포
sam deploy --debug
```

#### Lambda 함수 업데이트 실패
```bash
# 함수 존재 여부 확인
aws lambda get-function --function-name addGroup

# 수동 업데이트
aws lambda update-function-code --function-name addGroup --zip-file fileb://addGroup.zip
```

### 2. 데이터베이스 연결 문제

#### DocumentDB 연결 오류
- 보안 그룹 설정 확인
- VPC 설정 및 서브넷 확인
- 연결 문자열 형식 검증

#### MongoDB 연결 문자열 예시
```
mongodb://username:password@cluster-endpoint:27017/database?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false
```

### 3. SMS 발송 문제

#### SNS 권한 설정
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "*"
    }
  ]
}
```

#### 발송 실패 디버깅
```python
# CloudWatch 로그 확인
# SMS 발송 한도 확인
# 전화번호 형식 검증 (+82 형식)
```

### 4. API 인증 문제

#### Authorizer 함수 디버깅
- 토큰 형식 검증
- IAM 정책 확인
- Lambda 함수 로그 확인

### 5. 로컬 테스트 문제

#### Docker 관련 오류
```bash
# Docker 실행 상태 확인
docker info

# SAM 로컬 환경 초기화
sam local start-api --debug
```

## 성능 최적화

### 1. Lambda 함수 최적화
- **메모리 할당**: 적절한 메모리 크기 설정 (256MB 기본)
- **타임아웃**: 적절한 타임아웃 설정 (10초 기본)
- **환경 변수**: 설정 값의 환경 변수 활용

### 2. 데이터베이스 최적화
- **인덱스 설정**: 자주 조회하는 필드에 인덱스 생성
- **쿼리 최적화**: 필요한 필드만 조회
- **연결 풀링**: 연결 재사용으로 성능 향상

### 3. API Gateway 최적화
- **캐싱**: 자주 조회하는 데이터의 캐싱 설정
- **압축**: 응답 데이터 압축 활성화
- **모니터링**: CloudWatch를 통한 성능 모니터링

## 확장 방안

### 1. 기능 확장
- **위치 기반 서비스**: GPS를 활용한 주변 그룹 추천
- **채팅 기능**: 실시간 그룹 채팅
- **정산 기능**: 공동 구매 비용 정산
- **리뷰 시스템**: 그룹 활동 후 평가

### 2. 기술적 확장
- **실시간 알림**: WebSocket을 통한 실시간 업데이트
- **이미지 업로드**: S3를 활용한 장보기 리스트 이미지 공유
- **푸시 알림**: 모바일 앱 푸시 알림 연동
- **데이터 분석**: 사용자 행동 분석 및 추천 시스템

## 관련 챕터

이 프로젝트는 책의 다음 내용들과 연관됩니다:

- **Chapter 1**: 해커톤 팀 빌딩 및 역할 분담
- **Chapter 2-3**: 아이디어 도출 기법 (마인드 맵, 스캠퍼, 스마트)
- **Appendix A**: 개발환경 구성
- **Appendix B**: STAR 기법을 활용한 프로젝트 발표

## 도서 정보

**제목**: 해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지  
**부제**: 10개의 해커톤 프로젝트로 배우는 소프트웨어 개발  
**저자**: 노아론 (github.com/roharon)  
**출판사**: 로드북  
**출간일**: 2025년 7월 28일

### 구매 링크
- [교보문고](https://product.kyobobook.co.kr/detail/S000217089414)
- [예스24](https://www.yes24.com/product/goods/149385474)
- [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)

## 라이선스

이 프로젝트는 Apache-2.0 라이선스 하에 배포됩니다.

## 기여하기

프로젝트 개선을 위한 기여를 환영합니다:

1. 이슈 등록: 버그 리포트나 기능 제안
2. Pull Request: 코드 개선이나 문서 업데이트
3. 피드백: 사용 경험 공유

---

**해커톤에서 성공하는 팁**: 이 프로젝트처럼 핵심 기능에 집중하고, 서버리스 아키텍처를 활용하면 빠른 시간 안에 완성도 높은 서비스를 만들 수 있습니다. 로그인/회원가입 같은 부차적인 기능보다는 그룹 생성과 참여라는 핵심 가치에 집중한 것이 포인트입니다.
