# baccc-scoreboard
This is a very cool scoreboard
It keeps track of things.

Basic setup:
```
cd /path/to/baccc-scoreboard
sudo -H pip3 install -r requirements.txt
sudo gunicorn main:app -b 0.0.0.0:80
```
If you have a certificate, you can replace the last line with
```
sudo gunicorn --certfile=./cert.pem --keyfile=./priv.pem main:app --bind 0.0.0.0:443
```
where cert.pem and priv.pem are your certificate and private key.
You can avoid running gunicorn in superuser by not binding to common ports (80 and 443) and use port forwarding to forward ports like 2020, etc. instead.