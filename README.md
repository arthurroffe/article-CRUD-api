# article-CRUD-api
使用django-rest-framework建置的api 可以對文章進行CRUD

# 使用說明
打開cmd，並在資料夾所在位置
```
$ article-CRUD-api> docker-compose build
```
build的時候會下載需要的資源，會比較久，請讓他慢慢跑，跑完之後會看到
```
docker-compose build
[+] Building 39.6s (13/13) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                       0.0s 
 => => transferring dockerfile: 32B                                                                                                                                                        0.0s 
 => [internal] load .dockerignore                                                                                                                                                          0.0s 
 => => transferring context: 35B                                                                                                                                                           0.0s 
 => [internal] load metadata for docker.io/library/python:3.7                                                                                                                              0.8s 
 => [internal] load build context                                                                                                                                                          0.0s 
 => => transferring context: 1.94kB                                                                                                                                                        0.0s 
 => [1/8] FROM docker.io/library/python:3.7@sha256:1ae0dfb6419b454be461cbe0474c90134e9cdac0fe2c791fa189d64723ade049                                                                        0.0s 
 => CACHED [2/8] WORKDIR /app                                                                                                                                                              0.0s 
 => [3/8] COPY . .                                                                                                                                                                         0.0s 
 => [4/8] RUN python -m pip install --upgrade pip                                                                                                                                          5.7s 
 => [5/8] RUN apt-get update                                                                                                                                                               4.1s 
 => [6/8] RUN apt-get install -y postgresql-client                                                                                                                                         3.2s 
 => [7/8] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                              23.8s 
 => [8/8] RUN adduser --disabled-password --no-create-home django-user                                                                                                                     0.7s 
 => => exporting layers                                                                                                                                                                    1.1s 

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
```
就可以下下一個指令了
```
$ article-CRUD-api> docker-compose up
```
我在裡面有寫一個command，當資料庫user為空的時候會主動建立一個新的superuser  
帳號:admin@admin.com  
密碼:admin  
檔案在 app/core/management/commands/initadmin.py  
需要修改帳號密碼可以更改這裡   
up起來就可以用 127.0.0.1:8000進去網站了  
127.0.0.1:8000/api/docs/ 可以進入swagger  
![image](https://github.com/arthurroffe/article-CRUD-api/assets/61173724/a0136417-a966-4510-b05f-9046c99873a7)  
可以在裡面測試API 也是API文件  
因為資料內都是空的，請要在
![image](https://github.com/arthurroffe/article-CRUD-api/assets/61173724/7671fbbd-f49b-4fba-ba78-17382c95b0d1)
新增資料，然後就可以開始測試帳號

# 登入介紹
使用JWT 使用 simplejwt  
先到
mothod:POST
path: /token/
request
```
{
  "email": "admin@admin.com",
  "password": "admin"
}
```
response
```
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzMzY5ODYyLCJpYXQiOjE2OTMzNjk1NjIsImp0aSI6IjE3NzhiMmE0ZDQ4ZDQ3ODQ5Y2JhYjdjZjU1NWIxMzk5IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20ifQ.xfUOHk1Z9eZ4C4sLi1e27xKD1awOz6t5igcVZdKWrfw",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MzQ1NTk2MiwiaWF0IjoxNjkzMzY5NTYyLCJqdGkiOiJkYzNlZjljMTgxNjc0ZDQ3OTc3YWUyZGEzMTlmNzQ4MiIsInVzZXJfaWQiOjEsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIn0.pP7ignpu4o-JIuzsI4aZbdR4kSOkNLCFZoibp0ok48o"
}
```
# API介紹
基本上資料庫我把它分為  
1.文章 Article  
2.熱門文章 popular article
文章會記錄
- 標題
- 圖片連結
- 文章連結
- 誰上傳的
- 甚麼時候上傳
- 甚麼時候修改

熱門文章會記錄  
- 加入日期
- 文章id
熱門文章則是直接做一對一的連結，去抓取資料，就不用多重存放了  
連結的部分因為考慮通常前半部的連結是一樣的，只有後半部的會有差，所以把前半部的連結放在了docker-compose的環境變數裡面
如果之後使用s3等會比較方便

#### 獲取熱門文章的list
method:GET  
path:/popular_articles/
response
```
{
  "message": "ok",
  "returnData": [
    {
      "id": 2,
      "article_id": 1,
      "title": "123",
      "date": "2023-08-30",
      "article_link": "https://en.wikipedia.org/wiki/7",
      "image_link": "https://imgur.com/1"
    },
    {
      "id": 3,
      "article_id": 2,
      "title": "456",
      "date": "2023-08-30",
      "article_link": "https://en.wikipedia.org/wiki/8",
      "image_link": "https://imgur.com/2"
    },
    {
      "id": 4,
      "article_id": 3,
      "title": "789",
      "date": "2023-08-30",
      "article_link": "https://en.wikipedia.org/wiki/9",
      "image_link": "https://imgur.com/3"
    }
  ]
}
```

#### 新增熱門文章
method:POST  
path:/popular_articles/  
request
```
{
  "article_id": [
    1,2,3
  ]
}
```
response
```
{
  "message": "ok",
  "returnData": [
    1,
    2,
    3
  ]
}
```

#### 修改文章
method:PATCH PUT
path:/articles/{id}  
request
```
{
  "title": "string",
  "image": "string",
  "link": "string"
}
```

#### 刪除熱門文章
method:DELETE
path:/popular_articles/{id}  
