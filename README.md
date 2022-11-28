# 医疗数据库系统使用指南

## 方法一：我要自己部署！

### 获取项目：

- 解压压缩包/从GitHub clone：

```
git clone https://github.com/minimao555/hospital-MySQL.git
```

### 配置环境：

- 进入project目录：

```
pip install -r requirements.txt
```

### 创建数据库：

- 版本：Mysql5.7.26

- 创建名为hospital的数据库，进入project目录，依次运行：

```
python manage.py migrate
python manage.py makemigrations
```

- 导入```hospital.sql```文件
- 创建用户：

```
python manage.py createsuperuser
```

### 运行：

```
python manage.py runserver
```

## 方法二：我不想自己部署！

- 创建数据库，直接导入```hospital-new.sql```文件
- 测试用用户：

|  username   |  password  |
| :---------: | :--------: |
|    admin    |   123456   |
| testDoctor  | Doctor123  |
| testPatient | Patient123 |

