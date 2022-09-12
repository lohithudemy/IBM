from fastapi import FastAPI

import redis
import logging



app = FastAPI()

logging.basicConfig(filename='myapp.log', format='%(asctime)s %(levelname)s -- %(message)s', level=logging.DEBUG)

_rclient = redis.StrictRedis('redis', 6379, db=0, charset='utf-8', decode_responses=True)


@app.get('/')
async def read_root():
    logging.info('endpoint call /')
    logging.debug('endpoint call / func: read_root message: HI')
    return {'message': 'Hi'}


@app.get('/count')
def read_count():
    db_size = _rclient.dbsize()
    logging.info('endpoint call /count')
    logging.debug(f'endpoint call /count func: read_count {db_size} items in redis')
    return {'Item count': f'{db_size}'}


@app.get('/ping')
def check_ping():
    rds = _rclient.ping()
    logging.debug(f'ping is {rds}!!!')
    return {'ping': f'{rds}'}


@app.get('/items/{item_id}')
def read_item(item_id: int):
    logging.info('endpoint call GET /items')
    logging.debug(f'endpoint call GET /items func: read_item Item ID {item_id}')
    return {'item_id': item_id, 'item_name': _rclient.get(item_id)}


@app.put('/items/{item_id}')
def update_item(item_id: int, item_name: str):
    logging.info('endpoint call PUT /items')
    logging.debug(f'endpoint call PUT /items func: update_item Item ID {item_id}')
    _rclient.set(item_id, item_name)
    logging.debug(f'Item ID {item_id} updated with value: {item_name}')
    return {'message': 'success', 'item_id': item_id, 'item_name': item_name}
