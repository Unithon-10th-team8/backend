# backend

<br><br>

## 가상 환경

pyenv 를 설치합니다.

```
curl https://pyenv.run | bash
```

python 을 설치합니다.

```
pyenv install 3.11.0
```

가상환경을 생성합니다.

```
pyenv virtualenv 3.11.0 가상환경이름
```

가상환경에 진입합니다.

```
pyenv local 가상환경이름
```

<br><br>

## 종속성 관리

poetry 를 설치합니다.

```
curl -sSL https://install.python-poetry.org | python3 -
```

의존성 패키지를 설치합니다.

```
poetry install
```

의존성 패키지 추가 명령어

```
poetry add 패키지이름
```

의존성 패키지 제거 명령어

```
poetry remove 패키지이름
```

<br><br>

## pre-commit

pre-commit hook 설치

```
pre-commit install
```

<br><br>

## 서버 실행

스크립트 권한을 추가합니다.

```
chmod +x scripts/* 
```

서버 실행 명령어

```
scripts/run-server.sh
```

서버 실행 명령어(변경사항 반영)

```
scripts/run-server.sh --reload
```

DB 컨테이너 띄우기

```
scripts/up.sh
```

<br><br>

## 폴더 구조

- alembic: Alembic 마이그레이션 관련 폴더.

- app: 실제 어플리케이션 코드가 들어있는 폴더.

- base: 기본적인 설정이나 공통 로직이 들어가는 폴더.

- repositories: 데이터 접근 로직이 들어갈 폴더.

- services: 비즈니스 로직이 들어갈 폴더.

- views: 뷰(콘트롤러) 로직이 들어갈 폴더.

- deps.py: 의존성 주입 관련 파일.

- exception_handlers.py와 exceptions.py: 에러 처리 관련 파일.

- main.py: FastAPI 어플리케이션의 시작점 파일.

- orm.py: ORM 관련 정의 파일.

- schemas.py: 데이터 스키마(dto) 정의 파일.

- utils.py: 유틸리티 함수가 담긴 파일.

- scripts: 스크립트 파일들이 있는 폴더. 서버를 실행하거나 다른 작업을 자동화하는 스크립트가 담겨 있음.

- secrets: 보안 관련 정보들을 저장하는 폴더.

- tests: 테스트 코드들이 담긴 폴더.

- docker-compose.yaml: Docker Compose 설정 파일.

- manage.py: 커맨드 라인에서 사용할 수 있는 관리 스크립트 파일.

- poetry.lock과 pyproject.toml: Poetry 의존성 정보를 담고 있는 파일.


