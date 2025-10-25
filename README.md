# DJANGO-101 — Getting Started Guide

เอกสารนี้อธิบายขั้นตอนการสร้างโปรเจกต์ Django พร้อมเชื่อมต่อฐานข้อมูล PostgreSQL
เหมาะสำหรับผู้เริ่มต้นที่ต้องการตั้งค่า Environment และรันเซิร์ฟเวอร์ให้พร้อมใช้งาน

## 0. ตรวจสอบเวอร์ชันของเครื่องมือ

ก่อนเริ่ม ให้ตรวจสอบว่าเครื่องของคุณติดตั้งเครื่องมือครบแล้ว
```python
python --version
pip --version
postgres --version
django-admin --version
```

## 1. ติดตั้ง Virtual Environment

Virtualenv ใช้สำหรับสร้างสภาพแวดล้อมแยกเฉพาะของแต่ละโปรเจกต์
```python
pip install virtualenv
```

## 2. สร้าง Virtual Environment
```python
python -m venv myenv
```

## 3. เปิดใช้งาน Virtual Environment

Windows
```python
myenv\Scripts\activate.bat
```
เมื่อเปิดสำเร็จ จะเห็นชื่อ (myenv) อยู่หน้าบรรทัดคำสั่ง

## 4. ติดตั้ง Django และ PostgreSQL Driver
```python
pip install Django
pip install psycopg2-binary
```

## 5. สร้างฐานข้อมูล PostgreSQL

- เปิดโปรแกรม pgAdmin (รูปช้าง) แล้วทำตามขั้นตอน:
- เข้าระบบด้วย
```
user : postgres
password : password
```
- คลิกขวาที่ Databases → Create → Database...
- ตั้งชื่อฐานข้อมูลให้ตรงกับที่โจทย์หรือโปรเจกต์กำหนด เช่น kmitl

## 6. สร้างโปรเจกต์ Django
```
django-admin startproject myblogs
```

โครงสร้างที่ได้:

myblogs/
 ├─ myblogs/
 │   ├─ settings.py
 │   ├─ urls.py
 │   └─ ...
 └─ manage.py

## 7. สร้างแอป (App) ชื่อ blogs
```
python manage.py startapp blogs
```

* เพิ่มชื่อแอปในไฟล์ myblogs/settings.py

INSTALLED_APPS = [
    ...
    'blogs',
]

## 8. ตั้งค่าฐานข้อมูล PostgreSQL

เปิดไฟล์ myblogs/settings.py แล้วแก้ส่วน DATABASES ให้เชื่อมกับฐานข้อมูลที่สร้างไว้

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "kmitl",          # ชื่อ Database
        "USER": "postgres",       # Username
        "PASSWORD": "password",   # Password
        "HOST": "localhost",      # หรือ IP ของ DB Server
        "PORT": "5432",           # พอร์ตค่าเริ่มต้นของ Postgres
    }
}
```

## 9. สร้างตารางในฐานข้อมูล
```
python manage.py makemigrations blogs
python manage.py migrate blogs
```

หรือใช้แบบย่อ:

```
python manage.py makemigrations
python manage.py migrate
```
## 10. รันเซิร์ฟเวอร์ทดสอบ
```
python manage.py runserver
```

เปิดเบราว์เซอร์และไปที่
http://127.0.0.1:8000

หากเห็นข้อความ “The install worked successfully!” แสดงว่า Django พร้อมใช้งานแล้ว

## 11. คำสั่งที่ควรรู้เพิ่มเติม
- ดูรายการ migrations ทั้งหมด
```
python manage.py showmigrations
```

- สร้าง superuser (สำหรับเข้าหน้า admin)
```
python manage.py createsuperuser
```

- ดู SQL ที่ Django จะรัน
```
python manage.py sqlmigrate blogs 0001
```

## 12. โครงสร้างโปรเจกต์ตัวอย่าง
```
myblogs/
├─ myblogs/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ blogs/
│  ├─ migrations/
│  ├─ models.py
│  ├─ views.py
│  └─ admin.py
└─ manage.py
```
