# 工资管理系统

## 环境搭建
首先安装virtualenv环境
```
pip install virtualenv
virtualenv ENV
```
进入virtualenv环境
Linux环境下
```
source ENV/bin/activate.sh
```
Windows环境下
```
.\ENV\Scripts\activate
```

## 安装
```
pip install -r requirements.txt
pip install --editable .
```

## 添加配置
修改config.py文件，例如
```
class Config(object):
    SECRET_KEY = 'This Is Some Secret Key'
    DEBUG = False
    TESTING = False
    # change next line to make DATABASE available
    SQLALCHEMY_DATABASE_URI = 'postgresql://name@host/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
```

## 运行
先添加环境变量
Linux环境下
```
export FLASK_APP=payroll
```
Windows环境下
```
$env:FLASK_APP = 'payroll'
```
初始化数据库
```
flask initdb
```
运行程序
```
flask run
```
