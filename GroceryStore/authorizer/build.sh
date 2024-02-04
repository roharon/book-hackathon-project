mkdir ./.build
pip install --platform manylinux2014_aarch64 --target=./.build --implementation cp --python-version 3.12 --only-binary=:all: --upgrade -r requirements.txt

cp ./lambda_function.py ./.build
cd ./.build

zip -r ../authorizer.zip .
rm -rf ../.build
