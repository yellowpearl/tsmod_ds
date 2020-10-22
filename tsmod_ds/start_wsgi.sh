#sudo ln -sf /etc/nginx/nginx.conf  ./
#sudo cp ./config.conf ./nginx.conf
sudo /etc/init.d/nginx restart
#sudo gunicorn3 -c ./hello.py hello:wsgi_application
gunicorn --bind 0.0.0.0:8000 ask.wsgi:application
#gunicorn --bind 0.0.0.0:8000 ask.ask.wsgi:application

