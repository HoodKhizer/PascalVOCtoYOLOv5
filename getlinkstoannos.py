import psycopg2
import os


cvat_url = '172.16.128.67'
cvat_port = '8080'

conn = psycopg2.connect(
    host=cvat_url,
    port="5432",
    database="cvat",
    user="root",
)
cur = conn.cursor()

images_names = ['0010100015220906211112.jpg']

for name in images_names:
    query = f"select concat('http://{cvat_url}:{cvat_port}/tasks/', engine_task.id, '/jobs/', engine_segment.id, '?frame=', engine_image.frame), engine_image.frame, engine_task.id, engine_segment.id from engine_image inner join engine_task on engine_image.data_id = engine_task.data_id inner join engine_segment on engine_task.id =engine_segment.task_id where path='{name}' and engine_segment.start_frame <= engine_image.frame and engine_image.frame <= engine_segment.stop_frame;"
    cur.execute(query)

    for row in cur.fetchall():
        print(row[0])

cur.close()
conn.close()