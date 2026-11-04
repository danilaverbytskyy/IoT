import pandas as pd
import psycopg2
from io import StringIO

# названия столбцов
cols = [
    'date',        # yyyy-mm-dd
    'time',        # hh:mm:ss.xxx
    'epoch',       # int
    'mote_id',      # int (1-55)
    'temperature', # float (°C)
    'humidity',    # float (0-100 %)
    'light',       # float (Lux)
    'voltage',     # float (V)
]

df = pd.read_csv(
    '../data/data.txt',
    sep=r'\s+',
    header=None,
    names=cols,
    engine='c',
)

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='mixed')

df = df.drop(columns=['date', 'time']).set_index('datetime').sort_index()

df = df[
    (df['temperature'].between(-60, 60)) &
    (df['humidity'].between(0, 100)) &
    (df['light'] >= 0) &
    (df['voltage'].between(1.5, 3.5)) &
    (df['mote_id'].between(1, 55))
]

df = df.drop_duplicates(subset=['epoch', 'mote_id'])
df['mote_id'] = df['mote_id'].astype('int16')

df_to_db = df.reset_index()

conn = psycopg2.connect(
    dbname='iot_db',
    user='postgres',
    password='postgrespassword',
    host='localhost',
    port=5433,
)
cur = conn.cursor()

buffer = StringIO()
df_to_db.to_csv(buffer, index=False, header=False)
buffer.seek(0)

cur.copy_from(
    buffer,
    'sensors_data',
    sep=',',
    columns=['datetime', 'epoch', 'mote_id', 'temperature', 'humidity', 'light', 'voltage'],
)

conn.commit()
cur.close()
conn.close()
