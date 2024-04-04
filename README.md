
# shortCuts - A tiny minimalistic link shortner

shortCuts is  a tiny link shortner that helps you shortner you long URL on the go.The vision of this project is to learn about Rest APIs and impliment learnings. shortCuts has been made on top of FastAPI [web framework]. 


## Important

The applications is divided into submodules, these submodules have indipendent functions.

- **Danych** contains code for database 
- **Fief** initially contained firebase file, now contains utility functions
- **Orarin** contains scheduler code
- **Routes** has all Routes
- **Test** contains testlib and test 

shortCuts uses Postgres DB for storing relational date and MongoDB for analytics, previously realtime DB was used to store analytics data, due to extra latency migration was done.

Create a json file as **"cred.json"** at previous working directory with following schema to store connection strings. This file is refrencenced by get_cred.py submodule to get connection strings.

```json
{
  "postgres_uri": <postgres  uri>,
  "mongo_uri": <mongodb uri>
}
```
Test directory contains test functions that test overall behavior of API.

## 🔗 Links
[![Website](https://img.shields.io/badge/Website-000?style=for-the-badge)](https://shrk.xyz/)

[![API Docs](https://img.shields.io/badge/API%20Docs-23aa12?style=for-the-badge)](https://shrk.xyz/Documentation)


## Run Locally

Clone the project

```bash
git clone https://github.com/shivanshguleria/shortCuts.git
```

Go to the project directory

```bash
cd shortCuts
```

Create Python virtual environment

```bash
python3 -m venv venv
```
Install required packages

```bash
pip install -r requirements.txt
```

Run application

```bash
uvicorn app.main:app [--reload --host --port]
```



## API Reference
This Documentaion is same as on [docs page](https://shrk.xyz/Documentation), for full docs visit docs.
#### Get a token

```http
  GET /api/token
```

#### Shorten a link


```http
  POST /api/link
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `link`      | `string` | **Required**. Long Url          |
   `token`     |  `string` | Include token for extra options see [docs](https://shrk.xyz/Documentation)


#### Redirect to long URL

```http
  GET /${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Short code generated from above request |

