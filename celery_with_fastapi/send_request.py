from fastapi import FastAPI, Query
from typing import Optional
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
import json
from tasks import give_features
from rich.console import Console
from pydantic import BaseModel

app = FastAPI()




class valid_request(BaseModel):
    Event : dict
    Version : str
    ClientId : str
    RequestId : str
    WebApiUrl : str
    LiveSequence : int
    Sources : list
    Analytics : list
    TargetVector : list

class valid_task(BaseModel):
    task_id : str
    status : str

class valid_feature(BaseModel):
    task_id : str
    status : str
    features : list

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#           sends json containing the required
#                        features
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@app.post('/model/predict', status_code=202, response_model=valid_task)
async def get_features(customer:valid_request):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    Console().status(f"request received .... ", spinner="bouncingBall")
    # Console().print(f"{customer}")
    #
    # print("prev ", type(customer))

    customer = dict(customer)

    # customer = json.loads(customer)
    print("after ", customer.keys())

    task_id = give_features.delay(customer["Sources"])
    return {'task_id': str(task_id), 'status': 'Processing'}


@app.get('/model/result/', status_code=200,response_model=valid_feature,
         responses={202: {'model': valid_task, 'description': 'Accepted: Not Ready'}})
async def get_features_result(task_id : Optional[str] = Query(None, max_length=100)):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        print(app.url_path_for('get_features'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': 'Success', 'features': result}