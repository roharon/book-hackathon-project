```shell
sh ./build.sh

aws lambda create-function --function-name getGroup --handler lambda_function.lambda_handler --runtime python3.12 --package-type Zip --zip-file fileb://getGroup.zip --role arn:aws:iam::541915504278:role/service-role/addGroup-role-cx5lxt6w \
--environment "Variables={DOCUMENT_DB_CONNECTION_STRING=mongodb://roharon:password@grocery-store.cluster-cjyarlzmcey0.ap-northeast-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false}"

aws lambda update-function-code --function-name getGroup --zip-file fileb://getGroup.zip
```
