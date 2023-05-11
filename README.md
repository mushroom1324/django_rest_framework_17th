# 5주차 미션: AWS : EC2, RDS & Docker & Github Action

- 대충 이미지 = 컨테이너에 넣을것들 정의한것이라고 이해했다
  - 이름이 이미지인 이유는 마치 `requirements.txt`처럼 필요한것들 모아서 찍어둔거라 그런 것 같다
- 대충 컨테이너 = 미니컴퓨터라고 이해했다
  - 미니컴퓨터 하나엔 데이터베이스, 하나엔 웹앱 이런식으로 켜두고 상호작용 하는 것 같다.

## Dockerfile
- `Dockerfile`은 `python`, `mysqlclient`, `mariadb-dev` 등 설치할 것들을 정의한다.

## docker-compose.yml
- `docker-compose.yml`에 base configuration을 넣는게 컨벤션이다.
- 여러개의 configuration files 사용 가능하다. *`docker-compose.override.yml` 처럼
  - 여러개의 configuration file들을 사용할 때, 파일들의 주소는 base Compose file(`-f`로 특정되는 Compose file)을 기준으로 두어야 한다.
- `docker-compose.yml`은 각각의 컨테이너들을 정의했다. 들어가는 정보들:
  - 컨테이너 이름
  - env: 환경변수
  - 포트번호
  - 의존성: 얘는 얘에 의존하니까 먼저 실행하지 마라
  - 커맨드: 쉘스크립트 실행할거 적어두는 것 같음
  - 이미지: 베이스 이미지를 지정할 수 있음 (템플릿 같이 제공하는 것들도 있고 커스텀 할수도 있고)
  - 등

## docker-compose.prod.yml
- production 환경에서 사용할 configuration을 정의한다.
- `docker-compose.prod.yml`은 `docker-compose.yml`을 상속받는다.

```yml
version: '3'
services:

  web:
    container_name: web
    build:
      context: ./
      dockerfile: Dockerfile.prod
    command: gunicorn django_rest_framework_17th.wsgi:application --bind 0.0.0.0:8000
    environment:
      DJANGO_SETTINGS_MODULE: django_rest_framework_17th.settings.prod
    env_file:
      - ./.env.prod
    volumes:
      - static:/home/app/web/static
      - media:/home/app/web/media
    expose:
      - 8000
    entrypoint:
      - sh
      - config/docker/entrypoint.prod.sh

  nginx:
    container_name: nginx
    build: ./config/nginx
    volumes:
      - static:/home/app/web/static
      - media:/home/app/web/media
    ports:
      - 80:80
    depends_on:
      - web

volumes:
  static:
  media:
```
##### web
- `dockerfile` : Dockerfile.prod로 적었다. 솔직히 그냥 눈치껏 적었다
- `env_file` : 이것도 눈치껏..
- `expose` : 그냥 `nginx.conf` 열어보니까 upstream server 포트 8000이길래 8000이라 적었다. (이것도 컨벤션이라..)

##### nginx
- `build` : config 안에 nginx가 있다.. 이 path를 주겠다.
- `ports` : 80이다. 포트번호야 뭐 아무거나 해도 되겠다만, 80이 컨벤션인 것 같다.
  - 여기선 `config/nginx/nginx.conf` 를 열어보면 `server -> listen 80;` 이라고 되어있다.

##### docker-compose.prod.yml은 DB가 없다?
<img width="729" alt="image" src="https://user-images.githubusercontent.com/76674422/237023670-3fe88be1-f544-4758-a9b0-7f90efb1cf56.png">

- 솔직히 웬만한 인터넷 자료보다 스터디 자료가 설명을 진짜 잘해놨다. (감사합니다)
  - 장고는 웹앱, nginx는 서버라고 한다. (난 지금까지 서버 개발 한다고 말해왔는데 엄밀히 말하면 아니네)
> nginx <-> gunicorn or uwsgi <-> wsgi <-> django

## docker-compose up
> sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d

- `docker-compose` 등 Compose files에 정의된 컨테이너들을 띄우는 명령어다.
- `-f` : forcing
- `--build` : 이미지를 새로 빌드한다.
- `-d` : 백그라운드에서 실행한다. (안하면 터미널 창에서 로그가 계속 찍힌다)

> gunicorn django_rest_framework_17th.wsgi:application --bind 0.0.0.0:8000
- 어쨌든 docker가 실행하는건 이거니까 먼저 실행해본다.
<img width="1029" alt="Screen Shot 2023-05-09 at 4 38 23 PM" src="https://user-images.githubusercontent.com/76674422/237027479-269842fb-3a06-40e8-87b7-c5a10b08e47b.png">

- 서버 실행이 되는 모습

<img width="1064" alt="image" src="https://user-images.githubusercontent.com/76674422/237027630-4a67779b-770e-4804-8eb8-786b9cdd99c1.png">

- `ALLOWED_HOSTS`에 `0.0.0.0`을 추가하랜다.
- `settings.py`에 추가하면 해결된다.

## 로컬에서 docker를 통해 서버와 db 실행
> docker-compose -f docker-compose.yml up --build

``` terminal
 => ERROR [8/8] COPY ../../Downloads/django_rest_framework_17th-master /app/                                                                                           0.0s
------
 > [8/8] COPY ../../Downloads/django_rest_framework_17th-master /app/:
------
failed to solve: failed to compute cache key: failed to calculate checksum of ref moby::tkce1vr8cnd2w31hes61pytzc: "/Downloads/django_rest_framework_17th-master": not found
```
- 에러가 발생했다: 캐쉬 키를 계산할 수 없다고 한다.
- `Dockerfile`에 있는 주소가 임의의 주소로 설정되어 있다.
- `COPY . /app/` 로 수정 후 실행하니 해결되었다.

``` terminal
web  |   File "<frozen importlib._bootstrap>", line 973, in _find_and_load_unlocked
web  | ModuleNotFoundError: No module named 'django_docker'
web exited with code 1
```

- 에러가 발생했다: 모듈이름이 `django_docker`라는데, 우리 모듈 이름은 `django_rest_framework_17th`이다.
- `docker-compose.yml`의 `DJANGO_SETTINGS_MODULE` 을 수정했다.

``` terminal
web  | ModuleNotFoundError: No module named 'rest_framework_simplejwt'
```
- requirements.txt에 `rest_framework_simplejwt`가 없다.
- freeze 하는걸 깜박했다.

> pip freeze > requirements.txt

##### 이 외에 에러떄문에 추가한것들..

- Package libffi was not found in the pkg-config search path 
  - Dockerfile에 `RUN apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev libffi-dev` 추가

- cryptography가 잘 안깔렸다고 징징댄다..
- 애플실리콘 맥이라 문제를 일으킨다고 한다.
> $ brew install openssl@1.1 rust

- 그리고 cffi를 지웠다가 다시 깔았다.
- cryptography도 다시 깔았다.
``` terminal
$ pip uninstall cffi
$ LDFLAGS=-L$(brew --prefix libffi)/lib CFLAGS=-I$(brew --prefix libffi)/include pip install cffi --no-binary :all:
$ LDFLAGS="-L$(brew --prefix openssl@1.1)/lib" CFLAGS="-I$(brew --prefix openssl@1.1)/include" pip install cryptography
```
- 안써도 되는 것 같아서 다시 지웠다.
- pymysql안쓰고 mysqlclient로 바꿨다.
  - mysql.config파일이 실종되어서 mysqlclient 패키지를 깔 수 없는 오류가 자꾸 생겼다..
  - mysql@5.7을 깔고 pip3 install mysqlclient를 해서 해결하긴 했다
  - 그 사이 수많은 방법을 시도해서 뭐가 정확한 방법인진 모르겠다.
- 그 외 많진 않고 오류 뭐 한 2억개정도? 고쳤다.

<img width="1005" alt="image" src="https://github.com/CEOS-Developers/django_rest_framework_17th/assets/76674422/b9233872-fbf7-40d0-abfa-2affcdc8cf4e">

- 도커에서 돌아가는 모습

<img width="1011" alt="image" src="https://github.com/CEOS-Developers/django_rest_framework_17th/assets/76674422/5151d326-bac0-4021-a7a1-ba6fb6fdee37">

- 지난 과제에서 구현한 회원가입 및 로그인이 잘 작동한다.

## 실 환경 배포
