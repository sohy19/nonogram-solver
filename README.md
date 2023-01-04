# nonogram-solver
흔히 NP문제로 알려져 있는 노노그램을 개선된 유전 알고리즘을 통해 해결하고 결과를 출력하는 웹사이트입니다. 행, 열 값과 힌트를 입력하면 결과와 연산 횟수를 확인할 수 있습니다.

## 구현 내용 이미지
|메인페이지|힌트 입력창|
|:-:|:-:|
|<img width="390" alt="스크린샷 2022-06-13 오후 6 00 52" src="https://user-images.githubusercontent.com/88651937/173318737-948ca32b-37be-490e-b4f8-61f062e1d920.png">|<img width="390" alt="스크린샷 2022-06-13 오전 11 11 08" src="https://user-images.githubusercontent.com/88651937/173270191-7c89535a-4bcf-4ac7-ab87-a94f24890f46.png">|
|결과 예시 1|결과 예시 2|
|<img width="390" alt="스크린샷 2022-06-13 오전 11 11 51" src="https://user-images.githubusercontent.com/88651937/173270202-4b5d6f48-844c-40d7-a92b-090a45ef9194.png">|<img width="390" alt="스크린샷 2022-06-13 오전 11 21 11" src="https://user-images.githubusercontent.com/88651937/173270208-896ecf35-f48c-4224-b2fa-9bfebc24afa7.png">|

* * *

## 사용 방법 
### IDE는 VS Code를 기준으로 합니다.
  
#### 깃에서 초기 파일을 내려 받는 방법 (VS code에서 빈 폴더 생성 후)
```
$ git clone https://github.com/sohy19/nonogram-solver.git
```
#### 가상환경 생성하기 및 켜기
```
$ cd nonogram-solver
$ python -m venv myvenv
$ source myvenv/bin/activate      //Mac
$ source myvenv/scripts/activate  // Windows
```
#### 프로젝트에 필요한 패키지 다운로드
```
$ pip install -r requirements.txt
```
#### .env 파일 생성 
  - 프로젝트 루트 디렉토리 (`/nonogram-solver`)에 작성
```
$ touch .env
```
  - 필요 환경변수 (.env 파일 내에 입력)
  ```bash
  SECRET_KEY=
  ```
#### 잘 다운로드 받아졌는지 확인
```
$ cd NonogramSolver
$ python manage.py runserver
```
