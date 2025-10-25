# DJANGO-101

## <START>
0.Prepare
python --version
pip --version
postgres --version
django-admin --version

0. Install Virtualenv
pip install virtualenv

1. สร้าง env
python -m venv myenv

2.Activate env
myenv\Scripts\activate.bat

3. Install Django
pip install Django
pip install psycopg2-binary

4. สร้าง db ในโปรแกรมช้าง
user : postgres
pass : password
> คลิกขวาที่ Databases > Create.. > Database.. > ตั้งชื่อให้ตรงกับที่โจทย์กำหนด

<Start Project>
1.Create Project
django-admin startproject myblogs

2.Create the "blogs" app
> python manage.py startapp blogs

3.Start server
> python manage.py runserver

4. ตั้งค่าใน myblogs/settings.py เพิ่ม app ลงใน INSTALLED_APPS
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "kmitl",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

python manage.py makemigrations ชื่อแอป
python manage.py migrate ชื่อแอป

