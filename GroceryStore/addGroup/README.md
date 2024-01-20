```shell
zip addGroup.zip ./addGroup/lambda_function.py
awslocal lambda create-function --function-name addGroup --runtime python3.10 --role arn:aws:iam::000000000000:role/lambda-role --zip-file fileb://./addGroup.zip

awslocal lambda invoke --function-name addGroup output.txt

awslocal lambda create-function-url-config --function-name addGroup --auth-type NONE
```

```shell
awslocal lambda list-functions    

awslocal lambda delete-function --function-name addGroup
```

```shell

pip install --platform manylinux2014_aarch64 --target=package --implementation cp --python-version 3.12 --only-binary=:all: --upgrade

pip install -r requirements.txt --target ./package

zip -r addGroup.zip . -i lambda_function.py ./package


```
