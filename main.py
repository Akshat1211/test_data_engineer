import sys
import json
from configparser import ConfigParser

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from smart_open import smart_open


def preprocessing(students, teachers):
    """
    Processing data and converting to json report
    :param students: pd.DataFrame
    :param teachers: pd.DataFrame
    :return data: json
    """
    data = []

    for _, row in teachers.iterrows():
        teacher = {'teacher_id': row['id'],
                   'teacher_name': row['fname'] + ' ' + row['lname'],
                   'class_id': row['cid']}

        obj_list = []

        for __, _row in students[students['cid'] == row['cid']].iterrows():
            student = {'student_id': _row['id'],
                       'student_name': _row['fname'] + ' ' + _row['lname']}
            obj_list.append(student)

        teacher['students'] = obj_list
        data.append(teacher)

    with open('data.json', 'w') as student_data:
        json.dump(data, student_data, indent=4)

    return data


if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read('runtime.ini')
    connect_to_s3 = cfg.getboolean('main_config', 'connect_to_s3')

    if not connect_to_s3:

        path_to_students = cfg.get('local_credentials', 'path_to_students')
        path_to_teachers = cfg.get('local_credentials', 'path_to_teachers')
        students = pd.read_csv(path_to_students, delimiter='_')
        teachers = pd.read_parquet(path_to_teachers)

        output = preprocessing(students, teachers)
        print(output)
    else:

        aws_id = cfg.get('remote_credentials', 'aws_id')
        aws_secret = cfg.get('remote_credentials', 'aws_secret')
        bucket_name = cfg.get('remote_credentials', 'bucket_name')

        path_to_teachers = cfg.get('remote_credentials', 'path_to_teachers')
        path_to_students = cfg.get('remote_credentials', 'path_to_students')

        s3_bucket_path = f"s3://{aws_id}:{aws_secret}@{bucket_name}/{path_to_teachers}"
        teachers = pd.read_parquet(smart_open(
            s3_bucket_path), engine='pyarrow')

        s3_bucket_path = f"s3://{aws_id}:{aws_secret}@{bucket_name}/{path_to_students}"
        students = pd.read_csv(smart_open(
            s3_bucket_path), delimiter='_')

        output = preprocessing(students, teachers)
        print(output)
