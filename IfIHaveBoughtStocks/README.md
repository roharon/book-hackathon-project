## 11. 이때 주식을 매수했더라면 현재 수익은 얼마인지 조회하기

### 1. 사용하는 운영체제에 맞게 환경변수 설정하기

#### 윈도우 환경변수

```shell
$randomIdentifier = Get-Random -Maximum 10000000000
$location = "koreacentral"
$resourceGroup = "if-i-have-bought-stocks-$randomIdentifier"
$storage = "ifboughtstocks$randomIdentifier"
$functionApp = "if-i-have-bought-stocks-app-$randomIdentifier"
$skuStorage = "Standard_LRS"
$skuMySQL = "Standard_B1s"
$functionsVersion = "4"
```

#### 리눅스 / 맥 운영체제의 환경변수

```shell
let "randomIdentifier=$RANDOM*$RANDOM%10000000000" 
location="koreacentral" 
resourceGroup="if-i-have-bought-stocks-$randomIdentifier" 
storage="ifboughtstocks$randomIdentifier" 
functionApp="if-i-have-bought-stocks-app-$randomIdentifier"
skuStorage="Standard_LRS" 
skuMySQL="Standard_B1s" 
functionsVersion="4"
```


### 2. 애저 함수 생성하기

```shell
az login

az group create --name "$resourceGroup" --location "$location" 
az storage account create --name $storage --location "$location" --resource-group $resourceGroup --sku $skuStorage
az functionapp create --name $functionApp --resource-group $resourceGroup --storage-account $storage --consumption-plan-location $location --functions-version $functionsVersion --runtime python --os-type Linux 

az webapp config appsettings set --resource-group $resourceGroup --name $functionApp --settings API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
az functionapp cors add --name $functionApp --resource-group $resourceGroup --allowed-origins '*'
func azure functionapp publish $functionApp
```

### 3-1. web/index.html API_HOST 상수 값 변경

[2. 애저 함수 생성하기] 에서 생성한 URL로 변경하기

```javascript
const API_HOST = 'https://if-i-have-bought-stocks-app-XXXXXXXXXX.azurewebsites.net';
```


### 3-2. 블롭 스토리지 생성 및 정적 웹 사이트 호스팅 활성화하기

```shell
az storage container create --name '$web' --account-name $storage
az storage blob upload --account-name $storage --container-name '$web' --type block --file ./web/index.html

az storage blob service-properties update --account-name $storage --static-website --index-document index.html

az storage account show --name $storage
```
