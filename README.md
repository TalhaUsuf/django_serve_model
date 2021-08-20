# Commands

Write inside the `django_backend_api/app/` folder:

- To start the celery workers:
> `watchmedo auto-restart -d './'  -p '*.py' -- celery -A app worker --max-tasks-per-child 12 --concurrency=10 --loglevel=INFO
`
- To start the API
> `python manage.py runserver`

# Customize

| purpose | file-path |
|:---------| :------------|
| Acts like json schema. It **validates the input request and fields**, define the datatype of each field here.  | `app/keras_updated/models.py` | 
| Contains the **model loading and prediction functions**. Task defined here is carried out by celery worker. Model must be loaded as instructed in the file. |`app/keras_updated/tasks.py` | 

# URLs

 - [http://127.0.0.1:8000/api/predict/](http://127.0.0.1:8000/api/predict/) 
    - POST method, send a json request to this URL as shown in [sample[1]](#samples) , API will send a response as shown in [sample[2]](#samples)

 - [http://127.0.0.1:8000/api/predict/?task_id=<task_id>](http://127.0.0.1:8000/api/predict/?task_id=<task_id>) 
    - GET method, send a query request to this URL as shown in [sample[3]](#samples) , API will send a response as shown in [sample[4]](#samples)

 - [http://127.0.0.1:8000/api/db_get_id/<db_obj_id>](http://127.0.0.1:8000/api/db_get_id/) 
    - GET method, send a primary_key to this URL as shown in [sample[5]](#samples), API will send a response like [sample[6]](#samples) 

 - [http://127.0.0.1:8000/api/db_get_id/](http://127.0.0.1:8000/api/db_get_id/)
    -  GET method, send a request to this URL, PI will send a list of all the data records stored in the DB. 

# API architecture

|flow diagram|
|:--------:|
|![API flow chart](./api_FLOWCHART.png)}|



# Samples

[1]
 > `{
"service":"-",
"state":"NEW",
"proto":"tcp",
"attack_cat":"Normal",
"ID_NO":12,
"dur":100,
"spkts":10,
"dpkts":10,
"sbytes":100,
"dbytes":100,
"rate":100,
"sttl":100,
"dttl":100,
"sload":12,
"dload":12,
"sloss":12,
"dloss":12,
"sinpkt":15,
"dinpkt":15,
"sjit":15,
"djit":15,
"swin":15,
"stcpb":48,
"dtcpb":48,
"dwin":48,
"tcprtt":98,
"synack":98,
"ackdat":98,
"smean":98,
"dmean":98,
"trans_depth":8,
"response_body_len":54,
"ct_srv_src":56,
"ct_state_ttl":55,
"ct_dst_ltm":55,
"ct_src_dport_ltm":87.215,
"ct_dst_sport_ltm":87.215,
"ct_dst_src_ltm":87.215,
"is_ftp_login":87.215,
"ct_ftp_cmd":87.215,
"ct_flw_http_mthd":0.225,
"ct_src_ltm":0.225,
"ct_srv_dst":0.225,
"is_sm_ips_ports":1.25
}`

[2] 
> `{
    "db_obj_id": 12577,
    "task_id": "b4fac631-eb66-42e2-b283-62f984e904d6",
    "status": "Assigned to worker"
}`

[3]
> `http://127.0.0.1:8000/api/predict/?task_id=b4fac631-eb66-42e2-b283-62f984e904d6`

[4]
> `{
    "db_obj_id": 12577,
    "task_id": "b4fac631-eb66-42e2-b283-62f984e904d6",
    "status": "Completed",
    "result": 0.0
}`

[5]
> `http://127.0.0.1:8000/api/db_get_id/12577`


[6]
> `{
    "id": 12577,
    "task_id": "b4fac631-eb66-42e2-b283-62f984e904d6",
    "probability": 0.0,
    "service": "-",
    "state": "NEW",
    "proto": "tcp",
    "attack_cat": "Normal",
    "ID_NO": 12.0,
    "dur": 100.0,
    "spkts": 10.0,
    "dpkts": 10.0,
    "sbytes": 100.0,
    "dbytes": 100.0,
    "rate": 100.0,
    "sttl": 100.0,
    "dttl": 100.0,
    "sload": 12.0,
    "dload": 12.0,
    "sloss": 12.0,
    "dloss": 12.0,
    "sinpkt": 15.0,
    "dinpkt": 15.0,
    "sjit": 15.0,
    "djit": 15.0,
    "swin": 15.0,
    "stcpb": 48.0,
    "dtcpb": 48.0,
    "dwin": 48.0,
    "tcprtt": 98.0,
    "synack": 98.0,
    "ackdat": 98.0,
    "smean": 98.0,
    "dmean": 98.0,
    "trans_depth": 8.0,
    "response_body_len": 54.0,
    "ct_srv_src": 56.0,
    "ct_state_ttl": 55.0,
    "ct_dst_ltm": 55.0,
    "ct_src_dport_ltm": 87.215,
    "ct_dst_sport_ltm": 87.215,
    "ct_dst_src_ltm": 87.215,
    "is_ftp_login": 87.215,
    "ct_ftp_cmd": 87.215,
    "ct_flw_http_mthd": 0.225,
    "ct_src_ltm": 0.225,
    "ct_srv_dst": 0.225,
    "is_sm_ips_ports": 1.25
}`
