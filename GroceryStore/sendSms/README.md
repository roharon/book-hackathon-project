```shell
sh ./build.sh

aws lambda create-function --function-name sendSms --handler lambda_function.lambda_handler --runtime python3.12 --package-type Zip --zip-file fileb://sendSms.zip --role arn:aws:iam::541915504278:role/service-role/addGroup-role-cx5lxt6w
aws lambda update-function-code --function-name sendSms --zip-file fileb://sendSms.zip
```
