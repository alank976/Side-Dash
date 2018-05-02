import pandas as _pd
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta



def data_from_backend():
    df = _pd.DataFrame({
        'When' : [_datetime.now() - _timedelta(days=1), _datetime.now()],
        'Who' : ['Alan', 'Alan'],
        'What' : ['Tech debt 1', 'Support-Celine'],
        'How long(hours)' : [1, 0.5]
    }, columns=['When', 'Who', 'What', 'How long(hours)'])
    df = df.append(dict(), True)
    return df.sort_values('When')

def update(id, field, value):
    print('PUT id={}, field={}, value={}.'.format(id, field, value))