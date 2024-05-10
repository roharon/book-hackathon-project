
```shell
pip install -r requirements.txt
```

![img.png](img.png)
```shell
# 우분투
sudo apt install default-libmysqlclient-dev pkg-config -y

# 맥
brew install pkg-config
```


```shell
docker run -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=weekly_goals -p 3306:3306 -d mysql:8.3
```
