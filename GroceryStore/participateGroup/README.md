```shell
sh ./build.sh

aws lambda create-function --function-name participateGroup --handler lambda_function.lambda_handler --runtime python3.12 --package-type Zip --zip-file fileb://participateGroup.zip --role arn:aws:iam::541915504278:role/service-role/addGroup-role-cx5lxt6w \
--environment "Variables={DOCUMENT_DB_CONNECTION_STRING=mongodb://}"

aws lambda update-function-code --function-name participateGroup --zip-file fileb://participateGroup.zip
```
