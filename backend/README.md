## README.md

Scripts to execute to run to apply migrations

```
python3 manage.py makemigrations users
python3 manage.py migrate
```

Script to execute to create the Certificate file and Key pem files

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

```
SUPER USER for admin panel login credentials are

Username: admin
Password: admin
```
