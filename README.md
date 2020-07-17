## Task :
This python application processes the two data files [students.csv , teachers.parquet], which can be provided as an absolute path and also as S3 bucket files.
Then the application outputs a report in json, listing each student and the teacher which the student has and the class ID the student is scheduled for.

## System requirements:
- OpenSSL 1.1.1
- python 3.6

## Packages used:
- pandas (for processing csv and parquet files)
- os (to access files from local directory)
- json (to output a proper json formatted data)
- pyarrow (to access parquet files)
- smart_open (to access files from S3)

## Environmen set up and Run below commands:
- Git clone command :
```python
git clone https://github.com/Akshat1211/test_data_engineer.git
```
- Go to root directory :
```
cd test_data_engineer
```

- Create an environment :
```
python -m virtualenv env
```

- Activate environment :
```
source env/bin/activate
```

- If we want to get input from s3 then do changes in runtime.ini file
- set
- aws_id = your_aws_access_key
- aws_secret = your_aws_secret_key
- bucket_name = s3_bucket_name


```python
python main.py
python main.py [path1 (.parquet)] [path2 (.csv)]
python main.py s3 [access_key] [secret_access_key] [bucket_name] [object_key_1 (.parquet)] [object_key_2 (.csv)]
```

- Docker commands :
```dockerfile
docker build app . -t <username>/image_name:latest
docker run app
```