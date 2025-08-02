# Chapter 10: 한 주간의 목표 세우기

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Azure Functions](https://img.shields.io/badge/Azure-Functions%20v4-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.27-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.3-4479A1?style=flat&logo=mysql&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 10 프로젝트

## 프로젝트 개요

Chapter 10에서는 개인의 목표 관리를 위한 API 서비스를 구축합니다. 이 프로젝트를 통해 Azure Functions 기반의 서버리스 아키텍처, 데이터베이스 모델링, 그리고 체계적인 API 설계 방법을 학습할 수 있습니다.

해커톤의 핵심인 "단기간에 의미있는 결과물 만들기"를 실현하기 위해, 복잡한 인증 시스템 대신 목표 설정과 평가라는 핵심 기능에 집중한 프로젝트입니다.

### 주요 기능

- **목표 설정**: 주별 목표를 설정하고 관리
- **목표 조회**: 이번 주/지난 주 목표 조회 및 필터링
- **목표 평가**: 완료된 목표에 대한 평가 작성
- **통계 기능**: 월별 목표 달성 현황 조회

### 학습 목표

Chapter 10을 통해 다음을 배울 수 있습니다:

1. **서버리스 아키텍처**: Azure Functions 기반의 효율적인 API 구축
2. **데이터 모델링**: 사용자-목표-평가 간의 관계 설계
3. **API 설계**: RESTful API 원칙에 따른 엔드포인트 구성
4. **상태 관리**: 목표의 생명주기와 상태 변화 관리

## 기술 스택

### Backend
- **Azure Functions v4**: 서버리스 컴퓨팅 플랫폼
- **Python 3.9+**: 주 개발 언어
- **SQLAlchemy 2.0.27**: ORM 라이브러리

### Database
- **MySQL 8.3**: 관계형 데이터베이스
- **Azure Database for MySQL**: 클라우드 데이터베이스 서비스

### API Documentation
- **OpenAPI 3.0**: API 스펙 문서화

## 데이터베이스 스키마

```sql
-- 사용자 테이블
CREATE TABLE users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id)
);

-- 목표 테이블
CREATE TABLE goals (
    id INT(11) NOT NULL AUTO_INCREMENT,
    user_id INT(11) NOT NULL,
    description VARCHAR(255) NOT NULL,
    resolved TINYINT(1) NOT NULL DEFAULT 0,
    year INT(11) NOT NULL,
    month INT(11) NOT NULL,
    week INT(11) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id)
);

-- 평가 테이블
CREATE TABLE assessments (
    id INT(11) NOT NULL AUTO_INCREMENT,
    user_id INT(11) NOT NULL,
    year INT(11) NOT NULL,
    month INT(11) NOT NULL,
    week INT(11) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id)
);
```

## 도메인 모델 구조

### Goal (목표)
- 사용자의 주별 목표를 관리
- 연도, 월, 주 단위로 구분
- 완료 여부 추적

### Assessment (평가)
- 목표에 대한 사용자 평가
- 주별로 하나의 평가만 작성 가능
- 완료된 목표 ID 목록 포함

### User (사용자)
- 기본 사용자 정보 관리
- 현재는 목업 사용자 ID 사용

## API 엔드포인트

### 목표 관리
- `POST /goals`: 새로운 목표 추가
- `GET /goals`: 목표 조회 (주별 필터링 지원)
- `GET /goals/stats`: 월별 목표 달성 통계

### 평가 관리
- `POST /assessments`: 목표 평가 작성
- `GET /assessment`: 특정 주의 평가 조회

자세한 API 스펙은 `openapi.yaml` 파일을 참조하세요.

## 개발 환경 설정

### 필수 요구사항

- Python 3.9 이상
- Azure Functions Core Tools
- Docker (MySQL 실행용)
- Azure CLI (배포용)

### Python 가상환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### Azure Functions Core Tools 설치

```bash
# npm을 통한 설치
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# 또는 Homebrew (Mac)
brew tap azure/functions
brew install azure-functions-core-tools@4
```

## 로컬 실행하기

### 1. MySQL 데이터베이스 실행

Docker를 사용하여 MySQL을 실행합니다:

```bash
# MySQL 컨테이너 실행
docker run -e MYSQL_ROOT_PASSWORD=password \
           -e MYSQL_DATABASE=setweeklygoals \
           -p 3306:3306 \
           -d mysql:8.3

# 데이터베이스 스키마 생성
mysql -h localhost -u root -ppassword setweeklygoals < schema.sql
```

### 2. 환경 변수 설정

`local.settings.json` 파일에서 데이터베이스 연결 설정:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "MYSQLCONNSTR_DB": "mysql://root:password@localhost:3306/setweeklygoals"
  }
}
```

### 3. Azure Functions 실행

```bash
# Functions 호스트 시작
func host start

# 또는 환경 변수 직접 설정
MYSQLCONNSTR_DB=mysql://root:password@localhost:3306/setweeklygoals func host start
```

성공적으로 실행되면 다음과 같은 메시지가 출력됩니다:

```
Functions:
        add_goal: [POST] http://localhost:7071/api/goals
        get_goals: [GET] http://localhost:7071/api/goals
        get_goals_stats: [GET] http://localhost:7071/api/goals/stats
        add_assessment: [POST] http://localhost:7071/api/assessments
        get_assessment: [GET] http://localhost:7071/api/assessment
```

## API 사용 예제

### 목표 추가

```bash
curl -X POST http://localhost:7071/api/goals \
  -H "Content-Type: application/json" \
  -d '{"description": "책 한 권 읽기"}'
```

### 목표 조회

```bash
# 이번 주 목표 조회
curl http://localhost:7071/api/goals

# 지난 주 목표 조회
curl http://localhost:7071/api/goals?weekly_offset=1
```

### 목표 평가 작성

```bash
curl -X POST http://localhost:7071/api/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "content": "목표를 설정한 덕에 보람찬 한 주를 보낼 수 있었다",
    "year": 2024,
    "month": 1,
    "week": 1,
    "resolvedGoalIds": [1, 2]
  }'
```

## Azure 배포

### 1. Azure 리소스 생성 (Linux/Mac)

```bash
# Azure CLI 로그인
az login

# 배포 스크립트 실행
let "randomIdentifier=$RANDOM*$RANDOM%10000000000"
location="koreacentral"
resourceGroup="set-weekly-goals-$randomIdentifier"
storage="setweeklygoals$randomIdentifier"
functionApp="set-weekly-goals-app-$randomIdentifier"
dbName="weekly_goals"
dbAdminUser=setweeklygoals
dbAdminPassword=setweeklygoals1!
skuStorage="Standard_LRS"
skuMySQL="Standard_B1s"
functionsVersion="4"

# 리소스 그룹 생성
echo "리소스 그룹 $resourceGroup 을 $location 리전에 생성합니다"
az group create --name "$resourceGroup" --location "$location"

# 스토리지 계정 생성
echo "리소스 그룹 $resourceGroup 에 스토리지 계정을 생성합니다."
az storage account create --name $storage --location "$location" --resource-group $resourceGroup --sku $skuStorage

# 함수 앱 생성
echo "$functionApp 서버리스 함수 앱을 생성합니다"
az functionapp create --name $functionApp --resource-group $resourceGroup --storage-account $storage --consumption-plan-location $location --functions-version $functionsVersion --runtime python --os-type Linux

# MySQL 서버 생성
echo "MySQL 서버 $storage 를 생성합니다."
az mysql flexible-server create --public-access 0.0.0.0 --resource-group $resourceGroup --name $storage --admin-user $dbAdminUser --admin-password $dbAdminPassword --location "$location" --sku-name $skuMySQL

# 데이터베이스 생성
echo "MySQL 서버 $storage 에 데이터베이스 $dbName 을 생성합니다."
az mysql flexible-server db create --resource-group $resourceGroup --database-name $dbName --server-name $storage

# SSL 설정 비활성화
az mysql flexible-server parameter set --name require_secure_transport --value OFF --server-name $storage --resource-group $resourceGroup

# 연결 문자열 구성
mysqlHostName=$(az mysql flexible-server show --resource-group $resourceGroup --name $storage --query "fullyQualifiedDomainName" -o tsv)
mysqlConnectionString="mysql+pymysql://${dbAdminUser}:${dbAdminPassword}@${mysqlHostName}/${dbName}"
echo $mysqlConnectionString

# 함수 앱에 연결 문자열 설정
az webapp config connection-string set --resource-group $resourceGroup --name $functionApp -t mysql --settings "DB=$mysqlConnectionString"
```

### 2. 함수 배포

```bash
# Azure Function 배포
func azure functionapp publish $functionApp
```

### 3. 리소스 정리

```bash
# 모든 리소스 삭제
az group delete --name $resourceGroup --yes --no-wait
```

## 사용자 스토리

Chapter 10에서 다루는 주요 사용자 스토리:

1. **목표 설정자로서** 이번 주 달성하고 싶은 목표를 설정할 수 있다
2. **목표 추적자로서** 설정한 목표의 완료 여부를 업데이트할 수 있다
3. **자기성찰자로서** 지난 주 목표에 대한 평가를 작성할 수 있다
4. **진척도 확인자로서** 월별 목표 달성 통계를 확인할 수 있다

## 학습 포인트

### 1. 데이터 모델링
- 주차별 목표 관리를 위한 시간 기반 데이터 구조 설계
- 목표와 평가 간의 관계 모델링

### 2. API 설계
- RESTful 원칙에 따른 엔드포인트 구성
- 쿼리 매개변수를 활용한 필터링 구현

### 3. 상태 관리
- 목표의 생명주기 관리 (생성 → 진행 → 완료)
- 평가와 목표 간의 상태 동기화

### 4. 서버리스 아키텍처
- Azure Functions의 효율적 활용
- 데이터베이스 연결 풀 관리

## 확장 아이디어

### 기능 확장
- 푸시 알림 기능 (주별 목표 설정/평가 리마인더)
- 목표 카테고리 분류 시스템
- 소셜 기능 (친구와 목표 공유)
- 시각화 대시보드 (차트, 그래프)

### 기술적 확장
- 인증/인가 시스템 도입
- 캐싱 레이어 추가
- 배치 작업을 통한 통계 데이터 생성
- 마이크로서비스 아키텍처로 분리

## 문제 해결

### MySQL 연결 오류

**증상**: `OperationalError: (2003, "Can't connect to MySQL server")`

**해결책**:
1. MySQL 컨테이너가 실행 중인지 확인
2. 포트 3306이 사용 가능한지 확인
3. 연결 문자열의 호스트/포트/자격증명 검증

### Azure Functions 배포 실패

**증상**: `Error: subprocess-exited-with-error`

**해결책**:
```bash
# Ubuntu
sudo apt install default-libmysqlclient-dev pkg-config -y

# macOS
brew install pkg-config mysql
```

### 데이터베이스 스키마 오류

**증상**: `Table 'goals' doesn't exist`

**해결책**:
```bash
# 스키마 파일 재실행
mysql -h localhost -u root -ppassword setweeklygoals < schema.sql
```

## 참고 자료

- [Azure Functions Python 개발자 가이드](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [OpenAPI 3.0 스펙](https://swagger.io/specification/)
- [MySQL 8.3 문서](https://dev.mysql.com/doc/refman/8.3/en/)

## 기여하기

이 프로젝트는 "해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지" 도서의 Chapter 10 예제입니다. 개선사항이나 질문이 있으시면 Issue를 생성해 주세요.

## 라이센스

이 프로젝트는 교육 목적으로 제작되었습니다.
