# payroll

## 环境搭建
首先安装并进入virtualenv环境
```c
pip install virtualenv
virtualenv ENV
source ENV/bin/activate.sh
```

## 安装
```c
pip install -r requirements.txt
pip install --editable .
```

## 运行
```c
export FLASK_APP=payroll
flask run
```
