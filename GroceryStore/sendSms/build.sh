mkdir ./.build
pip install --platform manylinux2014_aarch64 --target=./.build --implementation cp --python-version 3.12 --only-binary=:all: --upgrade -r requirements.txt

cp ./lambda_function.py ./.build
cd ./.build

wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
zip -r ../sendSms.zip .
rm -rf ../.build
