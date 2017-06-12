# 工资管理系统

## 环境搭建
首先安装virtualenv环境
```c
pip install virtualenv
virtualenv ENV
```
进入virtualenv环境
Linux环境下
```c
source ENV/bin/activate.sh
```
Windows环境下
```c
.\ENV\Scripts\activate
```

## 安装
```c
pip install -r requirements.txt
pip install --editable .
```

## 运行
先添加环境变量
Linux环境下
```c
export FLASK_APP=payroll
```
Windows环境下
```c
$env:FLASK_APP = 'payroll'
```
初始化数据库
```c
flask initdb
```
运行程序
```c
flask run
```
