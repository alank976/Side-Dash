import pandas as _pd
import requests as _requests
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta

_BASE_URL = 'http://localhost:8080/api/v1/tasks'
_TASK_ID_URL = _BASE_URL + "/{id}"


def data_from_backend():
    try:
        tasks = _requests.get(_BASE_URL).json()
    except: 
        tasks = []
    return (
        _pd.DataFrame(tasks,
                      columns=['id', 'date', 'personName', 'taskName', 'hourSpent'])
        .sort_values('date')
        .append(dict(), True)
    )


def update(id, field, value):
    # TODO: let backend implements PATCH
    print('PATCH id={}, field={}, value={}.'.format(id, field, value))
    task = get_task(id) if id else dict()
    task[field] = value
    r = _requests.post(_BASE_URL, json=task)
    print('Updated={}'.format(r.content))


def delete(id):
    # print('Delete '+id)
    _requests.delete(_TASK_ID_URL.format(id=id))


def get_task(id):
    return _requests.get(_TASK_ID_URL.format(id=id)).json()
