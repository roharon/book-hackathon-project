# 해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Functions-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-교육용-green?style=flat)
![Book](https://img.shields.io/badge/출간-2025.07.28-blue?style=flat&logo=book&logoColor=white)

**10개의 해커톤 프로젝트로 배우는 소프트웨어 개발**

![책 커버 이미지](./book_image.png)

## 📖 도서 정보

- **저자**: 노아론 ([@roharon](https://github.com/roharon))
- **출판사**: 로드북
- **출간일**: 2025년 7월 28일
- **구매 링크**:
  - [교보문고](https://product.kyobobook.co.kr/detail/S000217089414)
  - [예스24](https://www.yes24.com/product/goods/149385474)
  - [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)

## 🎯 책 소개

해커톤은 짧은 시간 안에 팀을 이뤄 결과물을 만드는 것입니다. 이 책은 수많은 해커톤에 참여하고 국제 규모의 해커톤에서 입상한 저자가 **10개의 프로젝트 예제**를 통해 아이디어 발상, 기획, 구현, 발표까지 실제 해커톤의 과정을 알려줍니다.

### 이런 분들에게 추천합니다

- 🔧 혼자 사이드 프로젝트를 하다 늘 완성하지 못했던 개발자
- 🎓 포트폴리오가 부족해 고민 중인 컴공 전공 대학생  
- 💡 아이디어는 많은데 실제로 구현을 못 해본 스타트업 지망생
- 👥 '프론트만' '백엔드만' 하다 협업 감각을 잃은 주니어 개발자
- 🎨 신입 디자이너로서 개발자와 함께 일하는 법을 배우고 싶은 사람

### 주요 특징

- ✅ **10개의 해커톤 프로젝트**를 아이디어 구상부터 구현까지 구체적인 과정을 전부 수록
- ☁️ **클라우드의 서버리스 아키텍처**를 적극 활용
- 🎯 **본질적인 가치를 전달할 수 있는 최소 기능 제품(MVP)** 만들기에 집중

## 📁 프로젝트 목록

이 저장소에는 책에서 다루는 10개의 해커톤 프로젝트가 포함되어 있습니다.

| Chapter | 프로젝트명 | 설명 | 기술 스택 |
|---------|------------|------|-----------|
| 2 | [SnsMarket](./SnsMarket/) | 거래하기 안전한 SNS 마켓 | Python, Flask, SQLite |
| 3 | [UniversityCafeteriaMenu](./UniversityCafeteriaMenu/) | 주변 대학의 학생식당 메뉴 모아보기 | Python, FastAPI, PostgreSQL, Docker |
| 4 | [CafeteriaMenuBot](./CafeteriaMenuBot/) | 일주일 치 구내식당 식단표, 하루 단위로 확인하기 | Python, AWS Lambda, OCR API |
| 5 | [Campsite](./Campsite/) | 주말에 갈 캠핑장 찾기 | Python, AWS Lambda, OpenAPI |
| 6 | [RunnerSyncer](./RunnerSyncer/) | 달리기 측정 앱 간의 기록 연동하기 | Python, AWS Lambda, S3 |
| 7 | [GoogleDriveInvitation](./GoogleDriveInvitation/) | 구글 드라이브의 공유 문서함 초대 자동화하기 | Python, AWS Lambda, Google Drive API |
| 8 | [GroceryStore](./GroceryStore/) | 1인 가구의 장 함께 보기 | Python, AWS Lambda, SAM, MongoDB |
| 9 | [RssFeed](./RssFeed/) | 즐겨보는 블로그 글 모아보기 | Python, Azure Functions, MongoDB |
| 10 | [SetWeeklyGoals](./SetWeeklyGoals/) | 한 주간의 목표 세우기 | Python, Azure Functions, MySQL |
| 11 | [IfIHaveBoughtStocks](./IfIHaveBoughtStocks/) | 주식 매수 시점에 따른 현재 수익 조회하기 | Python, Azure Functions, Azure Storage |

## 🚀 저장소 사용법

### 1. 저장소 클론

```bash
git clone https://github.com/roharon/book-hackathon-project.git
cd book-hackathon-project
```

### 2. 개별 프로젝트 실행

각 프로젝트는 독립적으로 실행할 수 있습니다. 원하는 챕터의 디렉토리로 이동하여 해당 프로젝트의 README.md를 참고하세요.

```bash
# 예시: Chapter 2 SNS 마켓 프로젝트
cd SnsMarket
# SnsMarket/README.md 파일 참고하여 실행
```

### 3. 프로젝트별 실행 방법 요약

#### 로컬 개발 환경이 필요한 프로젝트
- **SnsMarket**: Python + pipenv 환경
- **UniversityCafeteriaMenu**: Python + Docker (PostgreSQL)
- **SetWeeklyGoals**: Python + Docker (MySQL)

#### 클라우드 환경이 필요한 프로젝트
- **CafeteriaMenuBot, Campsite, RunnerSyncer, GoogleDriveInvitation, GroceryStore**: AWS Lambda
- **RssFeed, IfIHaveBoughtStocks**: Azure Functions

## 🛠 필요한 개발환경

### 기본 요구사항

- **Python 3.8 이상**
- **Git**
- **Visual Studio Code** (권장)
- **Docker** (일부 프로젝트)

### 클라우드 계정

실습 중 무료 사용량 한도가 초과되면 일부 금액이 소진될 수 있습니다.
이를 방지하기 위해 **실습을 마치면 클라우드 내 생성한 리소스를 제거하시기 바랍니다.**

책의 모든 프로젝트를 실행하려면 다음 클라우드 계정이 필요합니다:

- **AWS 계정** (CafeteriaMenuBot, Campsite, RunnerSyncer, GoogleDriveInvitation, GroceryStore)
- **Microsoft Azure 계정** (RssFeed, SetWeeklyGoals, IfIHaveBoughtStocks)
- **Google Cloud Platform 계정** (GoogleDriveInvitation - Google Drive API 사용)


### 개발 도구 설치

#### 1. Python 환경 관리

```bash
# pipenv 설치 (권장)
pip install pipenv

# 또는 pip 사용
pip install -r requirements.txt
```

#### 2. Docker 설치

일부 프로젝트(UniversityCafeteriaMenu, SetWeeklyGoals)는 데이터베이스를 위해 Docker가 필요합니다.

- [Docker Desktop 다운로드](https://www.docker.com/products/docker-desktop/)

#### 3. 클라우드 CLI 도구

```bash
# AWS CLI
pip install awscli

# Azure CLI  
# macOS: brew install azure-cli
# Windows: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

## 📚 학습 가이드

### 읽는 순서

1. **Chapter 1**: 해커톤 기본 개념과 팀 빌딩 이해
2. **Chapter 2-3**: 로컬 개발 환경에서 시작 (SnsMarket, UniversityCafeteriaMenu)
3. **Chapter 4-8**: AWS 서버리스 아키텍처를 활용해 만들기
4. **Chapter 9-11**: Azure Functions 아키텍처를 활용해 만들기

### 실습 팁

- 💡 **핵심 기능부터 구현**: 로그인이나 회원가입 같은 부가 기능보다는 프로젝트의 고유한 가치를 구현하는 핵심 기능에 집중하세요
- 🔄 **반복적 개발**: 완벽한 기능을 한 번에 만들려 하지 말고, 작동하는 최소 기능부터 만들어보세요
- 👥 **협업 시뮬레이션**: 혼자 실습하더라도 팀 협업을 가정하고 API 문서 작성, 코드 리뷰 등을 해보세요

## 🤝 질문 / 제보하기

이 저장소는 도서의 예제 코드를 제공합니다. 실습 중 버그 발견 사항이나 질문이 있다면 이슈를 등록해주세요.

## 📄 라이선스

이 프로젝트의 코드는 교육 목적으로 제공됩니다. 상업적 사용 시에는 저자에게 문의해주세요.

## 👨‍💻 저자 정보

**노아론 (Aron Roh)**
- GitHub: [@roharon](https://github.com/roharon)
- 다수의 해커톤 참여 및 수상 경험
- 소프트웨어 개발자

---

📖 **"해커톤은 빠르게, 재밌게, 함께 만드는 즐거운 여정입니다."**

혼자서 공부했다면, 이제는 팀과 협업하며 실제 서비스를 만들 수 있는 해커톤에 도전해보세요!
