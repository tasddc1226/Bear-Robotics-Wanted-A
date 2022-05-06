## 👩‍💻 Team
- **[양수영](https://github.com/tasddc1226)**
- **[권은경](https://github.com/fore0919)**
- **[윤상민](https://github.com/redtea89)**

`프로젝트 진행 기간 2022.05.02 09:00 ~ 2022.05.06 18:00`

[`Team-A-notion`](https://pretty-marlin-13a.notion.site/Team-A-03cf51c7174847ce88a6302e6939ea2a)


## 🛠 기술 스택
<img src="https://img.shields.io/badge/python-3776AB?style=plastic&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/django-092E20?style=plastic&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/mysql-C70D2C?style=plastic&logo=mysql&logoColor=white">


## 🍝 서비스 개요
- 레스토랑 프렌차이즈의 **비즈니스 KPI(핵심 성과 지표)** 데이터를 얻기 위한 플랫폼 서비스.

## 🤟 Swagger API
- Link : https://app.swaggerhub.com/apis/redtea89/BearAteam1/1.0.0

## 📏  규칙
- **RDB** : 관계형 데이터베이스
- **Point Of Sale** : 판매 시점 관리
- **KPI** : Key Performance Indicator, 핵심 성과 지표

## 📌 사용자 요구사항 정의
- **주어진 데이터셋을 요구사항대로 서빙하기위한 관계형 데이터베이스를 설계**
    - [x] 주어진 데이터 csv를 RDB에 적재
    - [x] 필요시 추가적인 모델 정의 
    
- **POS 데이터를 가공하여 KPI 데이터를 제공하는 REST API 구현**
    1. 레스토랑별 매출 KPI Filtering
    
        - [x] `(필수)` 시간대별 집계(년, 월, 주, 일, 시간)
        - [x] `(필수)` 검색시 StartTime ~ EndTime 범위 설정
        - [x] 가격 범위
        - [x] 인원 규모
        - [x] 레스토랑 그룹 
    2. 각 레스토랑 매출의 결제수단별 KPI 
        - [x] `(필수)` 시간대별 집계(년, 월, 주, 일, 시간)
        - [x] `(필수)` 검색시 StartTime ~ EndTime 범위 설정
        - [x] 가격 범위
        - [x] 인원 규모
        - [x] 레스토랑 그룹 
    3. 각 레스토랑 이용 인원별 KPI 
        - [x] `(필수)` 시간대별 집계(년, 월, 주, 일, 시간)
        - [x] `(필수)` 검색시 StartTime ~ EndTime 범위 설정
        - [x] 가격 범위
        - [x] 인원 규모
        - [x] 레스토랑 그룹 
- **레스토랑 정보 CRUD | 요구사항 구현을 위한 추가 기능**
    - `[POST]` 레스토랑 등록
        - [x] 레스토랑 이름, 그룹, 도시, 주소 등록
    - `[PUT]` 레스토랑 정보 수정
        - [x] 레스토랑 이름, 그룹, 도시, 주소 수정
    - `[DELETE]` 레스토랑 삭제
        - [x] 레스토랑 정보 삭제 시 관련 정보 삭제
    - `[GET]` 레스토랑 조회 
        - [x] 레스토랑 목록/상세정보 조회
        - [x] 레스토랑 id, 레스토랑 이름, 그룹, 도시, 주소 조회

## Bonus Point
  - [x] Unit Test codes 
  - [x] Swagger UI : http://127.0.0.1:8000/swagger/
  - [ ] 레스토랑 이름을 제외한 정보를 조회, 집계된 KPI 데이터를 얻는 REST API
  - [ ] POS 데이터에 레스토랑 메뉴 추가, 집계된 KPI 데이터를 얻는 REST API

## DB Modeling
![bear (1)](https://user-images.githubusercontent.com/91520365/167058056-8254ae2a-50be-434d-b5ab-23a55e1a15f2.png)

## Path Variable
|Method|Request|URL|
|:-:|:--|:--|
|POST|POS 데이터 생성 |http://127.0.0.1:8000/api/v1/restaurant/pos|
|GET|POS 데이터 목록 조회 |http://127.0.0.1:8000/api/v1/restaurant/pos|
|GET|POS 데이터 정보 상세 조회|http://127.0.0.1:8000/api/v1/restaurant/pos/{id}|
|POST|레스토랑 데이터 생성 |http://127.0.0.1:8000/api/v1/restaurant/restaurants|
|GET|레스토랑 목록 조회 |http://127.0.0.1:8000/api/v1/restaurant/restaurants|
|GET|레스토랑 정보 상세 조회 |http://127.0.0.1:8000/api/v1/restaurant/restaurants/{id}|
|PUT|레스토랑 정보 수정 |http://127.0.0.1:8000/api/v1/restaurant/restaurants/{id}|
|DELETE|레스토랑 정보 삭제 |http://127.0.0.1:8000/api/v1/restaurant/restaurants/{id}|

## Query Parameter
|Method|Request|URL|
|:-:|:--|:--|
|GET|레스토랑별 매출 KPI 조회|http://127.0.0.1:8000/api/v1/kpi/restaurant?|
|GET|레스토랑 매출의 결제 수단별 집계 KPI|http://127.0.0.1:8000/api/v1/kpi/payment?|
|GET|레스토랑 이용 인원 규모별 집계 KPI|http://127.0.0.1:8000/api/v1/kpi/partynumber?|
