# Chapter 11: 주식 매수 시점에 따른 현재 수익 조회하기

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Azure Functions](https://img.shields.io/badge/Azure-Functions-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Azure Storage](https://img.shields.io/badge/Azure-Storage-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Alpha Vantage](https://img.shields.io/badge/Alpha%20Vantage-API-FF6600?style=flat&logo=api&logoColor=white)

> **해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지** - Chapter 11 프로젝트

## 프로젝트 소개

"만약 그때 주식을 샀더라면 지금 얼마나 벌었을까?" 이런 궁금증을 해결해주는 프로젝트입니다. 

이 프로젝트는 **Chapter 11**에서 다루는 내용으로, 특정 시점부터 주식을 정기적으로 매수했을 때의 현재 수익률을 계산하고, 그 수익금으로 살 수 있는 상품을 재미있게 보여주는 웹 애플리케이션입니다.

### 주요 학습 목표

- 외부 금융 API 연동 방법 익히기
- Azure Functions를 활용한 서버리스 아키텍처 구현
- 시계열 데이터 처리 및 수익률 계산 로직 구현
- RESTful API 설계 및 OpenAPI 스펙 작성
- 정적 웹사이트 호스팅을 통한 프론트엔드 배포

## 주요 기능

### 1. 주식 수익률 계산
- 지정된 시작일부터 매월 정기적으로 주식을 매수했을 때의 현재 수익률 계산
- Alpha Vantage API를 통한 실시간 주식 데이터 조회
- 월별 주식 가격 데이터 수집 및 분석

### 2. 수익 시각화
- 계산된 수익금을 직관적으로 보여주는 웹 인터페이스
- 수익금으로 구매 가능한 상품 추천 (펜, 피자, 아이패드, 노트북)
- 상품별 구매 가능 수량 표시

### 3. API 기능
- **주식 수익 조회 API**: `/stocks/{company_symbol}/profit`
- **상품 추천 API**: `/products`

## 기술 스택

### Backend
- **Azure Functions**: 서버리스 컴퓨팅 플랫폼
- **Python 3.9+**: 메인 개발 언어
- **Alpha Vantage API**: 주식 데이터 조회
- **Requests**: HTTP 클라이언트 라이브러리

### Frontend
- **HTML5 + JavaScript**: 웹 인터페이스
- **Tailwind CSS**: 스타일링
- **jQuery**: DOM 조작 및 AJAX 통신

### Infrastructure
- **Azure Blob Storage**: 정적 웹사이트 호스팅
- **Azure Resource Manager**: 인프라 관리

## 프로젝트 구조

```
IfIHaveBoughtStocks/
├── function_app.py          # Azure Functions 메인 애플리케이션
├── host.json               # Azure Functions 호스트 설정
├── local.settings.json     # 로컬 개발 환경 설정
├── requirements.txt        # Python 의존성 패키지
├── openapi.yaml           # OpenAPI 3.0 스펙 문서
├── web/
│   └── index.html         # 웹 인터페이스
├── images/                # 상품 이미지 파일들
│   ├── pen.jpg
│   ├── pizza.jpg
│   ├── ipad.jpg
│   └── laptop.jpg
└── README.md              # 프로젝트 문서
```

## 시작하기

### 사전 요구사항

1. **Azure CLI**: Azure 리소스 관리를 위해 필요
2. **Azure Functions Core Tools**: 로컬 개발 및 배포
3. **Python 3.9+**: 애플리케이션 실행 환경
4. **Alpha Vantage API Key**: 주식 데이터 조회를 위한 API 키

### API 키 발급 받기

1. [Alpha Vantage](https://www.alphavantage.co/)에서 무료 API 키 발급
2. RapidAPI를 통해 Alpha Vantage API 구독 (선택사항, 더 높은 요청 한도)

### 로컬 개발 환경 설정

1. **프로젝트 클론 및 디렉토리 이동**
   ```bash
   git clone https://github.com/roharon/book-hackathon-project.git
   cd IfIHaveBoughtStocks
   ```

2. **Python 의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **환경변수 설정**
   
   `local.settings.json` 파일에 API 키 추가:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
       "API_KEY": "your-alpha-vantage-api-key"
     },
     "Host": {
       "LocalHttpPort": 7071,
       "CORS": "*"
     }
   }
   ```

4. **로컬에서 Azure Functions 실행**
   ```bash
   func start
   ```

5. **웹 애플리케이션 테스트**
   
   브라우저에서 `web/index.html` 파일을 열고 테스트

## Azure 배포 가이드

### 1. 환경변수 설정

#### Windows (PowerShell)
```powershell
$randomIdentifier = Get-Random -Maximum 10000000000
$location = "koreacentral"
$resourceGroup = "if-i-have-bought-stocks-$randomIdentifier"
$storage = "ifboughtstocks$randomIdentifier"
$functionApp = "if-i-have-bought-stocks-app-$randomIdentifier"
$skuStorage = "Standard_LRS"
$functionsVersion = "4"
```

#### Linux/macOS (Bash)
```bash
let "randomIdentifier=$RANDOM*$RANDOM%10000000000" 
location="koreacentral" 
resourceGroup="if-i-have-bought-stocks-$randomIdentifier" 
storage="ifboughtstocks$randomIdentifier" 
functionApp="if-i-have-bought-stocks-app-$randomIdentifier"
skuStorage="Standard_LRS" 
functionsVersion="4"
```

### 2. Azure 리소스 생성 및 배포

```bash
# Azure 로그인
az login

# 리소스 그룹 생성
az group create --name "$resourceGroup" --location "$location"

# 스토리지 계정 생성
az storage account create \
  --name $storage \
  --location "$location" \
  --resource-group $resourceGroup \
  --sku $skuStorage

# Function App 생성
az functionapp create \
  --name $functionApp \
  --resource-group $resourceGroup \
  --storage-account $storage \
  --consumption-plan-location $location \
  --functions-version $functionsVersion \
  --runtime python \
  --os-type Linux

# API 키 환경변수 설정 (YOUR_API_KEY를 실제 키로 교체)
az webapp config appsettings set \
  --resource-group $resourceGroup \
  --name $functionApp \
  --settings API_KEY=YOUR_API_KEY

# CORS 설정
az functionapp cors add \
  --name $functionApp \
  --resource-group $resourceGroup \
  --allowed-origins '*'

# Function App 배포
func azure functionapp publish $functionApp
```

### 3. 정적 웹사이트 배포

1. **웹 인터페이스 설정 수정**
   
   `web/index.html` 파일에서 API_HOST 상수를 배포된 Function App URL로 변경:
   ```javascript
   const API_HOST = 'https://if-i-have-bought-stocks-app-XXXXXXXXXX.azurewebsites.net';
   ```

2. **Blob Storage 웹사이트 호스팅 설정**
   ```bash
   # 웹 컨테이너 생성
   az storage container create --name '$web' --account-name $storage
   
   # HTML 파일 업로드
   az storage blob upload \
     --account-name $storage \
     --container-name '$web' \
     --type block \
     --file ./web/index.html
   
   # 정적 웹사이트 호스팅 활성화
   az storage blob service-properties update \
     --account-name $storage \
     --static-website \
     --index-document index.html
   
   # 웹사이트 URL 확인
   az storage account show --name $storage --query "primaryEndpoints.web" --output tsv
   ```

## API 문서

### 주식 수익 조회 API

**엔드포인트**: `GET /stocks/{company_symbol}/profit`

**Parameters**:
- `company_symbol` (path): 주식 종목 코드 (예: MSFT, AAPL)
- `start_date` (query): 매수 시작일 (YYYY-MM-DD 형식)

**Example Request**:
```
GET /stocks/MSFT/profit?start_date=2020-01-01
```

**Example Response**:
```json
{
  "profit": 1250.50
}
```

### 상품 추천 API

**엔드포인트**: `GET /products`

**Parameters**:
- `price` (query): 수익금 (달러 기준)

**Example Request**:
```
GET /products?price=1250.50
```

**Example Response**:
```json
{
  "name": "아이패드 에어",
  "count": 2,
  "image_url": "https://raw.githubusercontent.com/roharon/book-hackathon-project/master/IfIHaveBoughtStocks/images/ipad.jpg"
}
```

## 주요 코드 설명

### 수익률 계산 로직

```python
def get_portfolio(start_date, time_series):
    """주식 포트폴리오의 현재 수익을 계산합니다."""
    last_date = datetime.now().strftime('%Y-%m')
    data = buy_stocks_monthly(start_date, time_series)
    
    return {
        "profit": (float(time_series[last_date]["1. open"]) * data[1]) - data[0],
    }

def buy_stocks_monthly(start_date, time_series):
    """시작일부터 매월 주식을 매수하는 시뮬레이션을 수행합니다."""
    current_date = start_date
    total_price = 0  # 총 투자금액
    count = 0        # 보유 주식 수
    
    while current_date <= datetime.now():
        date_str = current_date.strftime('%Y-%m')
        
        if date_str in time_series.keys():
            count += 1
            total_price += float(time_series[date_str]["1. open"])
        
        current_date = current_date + relativedelta(months=+1)
    
    return [total_price, count]
```

### 상품 추천 로직

```python
def get_product_by_price(price):
    """수익금에 따라 구매 가능한 상품을 추천합니다."""
    products = [
        {"name": "펜", "price": 2, "image_url": "..."},
        {"name": "피자", "price": 30, "image_url": "..."},
        {"name": "아이패드 에어", "price": 599, "image_url": "..."},
        {"name": "노트북", "price": 1999, "image_url": "..."}
    ]
    
    # 가격 내림차순 정렬
    products.sort(key=lambda x: x["price"], reverse=True)
    
    # 구매 가능한 가장 비싼 상품 찾기
    for product in products:
        if price >= product["price"]:
            return {
                "name": product["name"],
                "count": int(price / product["price"]),
                "image_url": product["image_url"]
            }
```

## 사용 방법

1. **웹사이트 접속**: 배포된 정적 웹사이트 URL로 접속
2. **주식 종목 코드 입력**: 예) MSFT, AAPL, GOOGL
3. **매수 시작일 선택**: 언제부터 주식을 사기 시작했는지 날짜 선택
4. **매수하기 버튼 클릭**: 수익률 계산 및 구매 가능 상품 확인

### 지원 주식 종목 (예시)

- **MSFT**: Microsoft Corporation
- **AAPL**: Apple Inc.
- **GOOGL**: Alphabet Inc.
- **AMZN**: Amazon.com Inc.
- **TSLA**: Tesla Inc.

## 학습 포인트

### 1. 외부 API 연동
- Alpha Vantage API를 통한 실시간 금융 데이터 조회
- API 응답 데이터 파싱 및 가공
- API 호출 최적화 및 에러 처리

### 2. 서버리스 아키텍처
- Azure Functions를 활용한 HTTP 트리거 함수 구현
- 서버리스 환경에서의 환경변수 관리
- 비용 효율적인 클라우드 서비스 활용

### 3. 시계열 데이터 처리
- 월별 주식 가격 데이터 수집
- 정기 매수 시뮬레이션 알고리즘 구현
- 수익률 계산 로직

### 4. RESTful API 설계
- OpenAPI 3.0 스펙을 통한 API 문서화
- RESTful한 엔드포인트 설계 원칙
- 적절한 HTTP 상태 코드 사용

## 확장 아이디어

### 단기 확장
- 다양한 투자 전략 시뮬레이션 (일시불 vs 적립식)
- 여러 주식 종목 동시 비교 기능
- 수익률 차트 시각화

### 중장기 확장
- 사용자 계정 및 포트폴리오 관리
- 주식 알림 기능 (목표 수익률 달성 시)
- 실제 투자 연동 기능
- 암호화폐, 펀드 등 다른 금융상품 지원

## 문제 해결 가이드

### 자주 발생하는 문제

1. **API 키 관련 오류**
   ```
   Error: Unauthorized (401)
   ```
   - Alpha Vantage API 키가 올바르게 설정되었는지 확인
   - API 키의 사용 한도를 초과하지 않았는지 확인

2. **CORS 에러**
   ```
   Error: CORS policy
   ```
   - Azure Function App의 CORS 설정 확인
   - 로컬 개발 시 `local.settings.json`의 CORS 설정 확인

3. **주식 데이터 없음**
   ```
   Error: KeyError in time_series
   ```
   - 입력한 주식 종목 코드가 올바른지 확인
   - 주말이나 공휴일에는 최신 데이터가 없을 수 있음

### 디버깅 팁

- Azure Portal에서 Function App 로그 확인
- 로컬 개발 시 `func start --verbose` 옵션 사용
- API 응답을 직접 확인하여 데이터 구조 파악

## 관련 Chapter

이 프로젝트는 **"해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지"** 도서의 **Chapter 11**에서 다루는 내용입니다.

### Chapter 11에서 다루는 주요 내용
- 아이디어 도출 기법 (마인드 맵, 스캠퍼, 스마트)
- 주식 가격 데이터 조회 API 선택 과정
- Azure Functions 기반 서버리스 아키텍처 설계
- OpenAPI 3.0을 활용한 API 스펙 설계
- 사용자 스토리 기반 기능 정의

### 도서 정보
- **제목**: 해커톤: 아이디어 도출, 팀 구축, 구현, 입상 전략까지
- **부제**: 10개의 해커톤 프로젝트로 배우는 소프트웨어 개발
- **저자**: 노아론 (github.com/roharon)
- **출판사**: 로드북
- **출간일**: 2025년 7월 28일

**구매 링크**:
- [교보문고](https://product.kyobobook.co.kr/detail/S000217089414)
- [예스24](https://www.yes24.com/product/goods/149385474)
- [알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=368098929&start=slayer)

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
