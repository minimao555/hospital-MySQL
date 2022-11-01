# Demo 使用说明

## 初始化数据库

### 清空应用数据

```python
python manage.py flush
```

### 迁移数据模型

在修改数据模型后，需要进行数据模型迁移，以同步到数据库

```python
python manage.py makemigrations
python manage.py migrate
```



## 启动服务

```python
python manage.py runserver [port]
```

