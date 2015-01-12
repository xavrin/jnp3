jnp3
====
Należy zainstalować postgresql i utworzyć bazę danych jak w settingsach,
ew. zmienić podejście na bardziej elastyczne, tj. każdy ma prywatny plik z
ustawieniami - jak będzie wygodniej.
Tworzymy virtualenva, np. tak:
````bash
virtualenv -p /usr/bin/python2.7 env
````
No i go używamy.
Instalujemy wymagania:
````bash
pip install -r requirements.txt
````
Poza tym należy odpalić migracje:
````bash
./manage.py makemigrations
./manage.py migrate
````
Następnie, a także po każdych zmianach w shardowanych modelach należy odpalić
````bash
./manage.py partition tweets
````
Instalujemy memcacheda, na Archu robi się to tak:
````bash
sudo pacman -S memcached
````
Przed używaniem cache'a należy go włączyć, np. tak (w tle):
````bash
memcached &
````
Przed używaniem celery należy włączyć workera:
````bash
celery -A twitter worker -l info
````
