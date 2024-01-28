# Project: Data Pipelines with Apache Airflow

## Introduction


Sparkify, a music streaming company, has opted to enhance the automation and monitoring of their data warehouse ETL pipelines. After thorough consideration, they have determined that Apache Airflow is the optimal tool for achieving this objective.

The aim is to construct sophisticated data pipelines characterized by dynamism and comprised of reusable tasks. These pipelines should be easily monitored and capable of facilitating backfills seamlessly. To ensure data integrity, tests must be conducted against the datasets subsequent to the execution of ETL steps in order to detect any inconsistencies.

The source data is stored in S3 and requires processing within Sparkify's data warehouse hosted on Amazon Redshift. Specifically, the source datasets consist of JSON logs detailing user activity within the application, as well as JSON metadata pertaining to the songs listened to by users.

## Datasets

For this particular project, we have two datasets available. Below are the S3 links for each of them.

>**s3://udacity-dend/song_data/**<br>
>**s3://udacity-dend/log_data/**

## Data Modeling wih Star Schema
![](https://github.com/JustePersonal/Project-6-Data-Pipelines-with-Airflow/blob/main/images/star_schema.png)

## Instructions for executing scripts

```bash
$ pip install -r requirements.txt
```

**Airflow Configuration**

In `airflow.cfg` (`~/airflow`) update `dags_folder` and `plugins_folder` to the project subdirectories. Set `load_examples = False`.

**Environment Configuration**

**`dwh.cfg`** - specifications for configuring the Redshift cluster and setting up data import.

**`create_cluster.py`** - establish an IAM role, set up a Redshift cluster, and enable TCP connections. Pass `--delete` flag to initiate resource deletion.

**`create_tables.py`** - recreate and drop tables.

- Set variables in `dhw.cfg` file:
<br />  **[AWS]**
<br />  KEY: AWS_ACCESS_KEY_ID
<br />  SECRET: AWS_SECRET_ACCESS_KEY
<br /> **[CLUSTER]**
<br /> DB_PASSWORD

- Establish an IAM role, set up a Redshift cluster, and arrange TCP connectivity.

```bash
$ python create_cluster.py
```

- Finish filling in `dwh.cfg` with the outputs obtained from `create_cluster.py`.
<br /> **[CLUSTER]**
<br /> HOST
<br /> **[IAM_ROLE]**
<br /> ARN

Drop and recreate tables:

```bash
$ python create_tables.py
```

### Start Airflow

```shell
$ airflow initdb
$ airflow scheduler
$ airflow webserver
```

### Airflow Web UI

Go to Admin > Connections apge and click `Create`.

On the create connection page, enter the following values:

* Conn Id: `aws_credentials`
* Conn Type: `Amazon Web Services`
* Login: `<AWS_ACCESS_KEY_ID>`
* Password: `<AWS_SECRET_ACCESS_KEY>`

Click `Save and Add Another`

* Conn Id: `redshift`
* Conn Type: `Postgres`
* Host: `<Redshift cluster endpoint from redshift.cfg>`
* Schema: `dev`
* Login: `awsuser`
* Password: `<Redshift db password from redshift.cfg>`
* Port: `5439`

## Customer Operators Built

### Stage Operator
The stage operator is designed to facilitate the loading of JSON formatted files from S3 into Amazon Redshift. This operator generates and executes a SQL COPY statement based on specified parameters, including the location of the file in S3 and the target table.

These parameters serve to differentiate between JSON files. Additionally, a crucial feature of the stage operator is its templated field, which enables the loading of timestamped files from S3 based on the execution time, thus facilitating backfills.

### Fact and Dimension Operators
The dimension and fact operators leverage the provided SQL helper class to execute data transformations. The majority of the logic resides within the SQL transformations, and the operator is expected to accept a SQL statement and a target database against which to execute the query. Furthermore, a target table can be defined to store the results of the transformation.

Dimension loads typically adhere to the truncate-insert pattern, where the target table is cleared before loading. Hence, a parameter can be included to toggle between insert modes during dimension loading. On the other hand, fact tables, due to their large size, generally support only append functionality.

### Data Quality Operator
The data quality operator is the final operator to be developed, responsible for conducting checks on the data itself. Its primary function is to receive one or more SQL-based test cases, along with the expected results, and execute these tests. For each test, a comparison is made between the actual and expected results. If there is a mismatch, the operator raises an exception, causing the task to retry and ultimately fail.

## Pipeline Graph
![](https://github.com/JustePersonal/Project-6-Data-Pipelines-with-Airflow/blob/main/images/final_project_dag.png)

#### Delete an IAM role and a Redshift cluster:
```bash
$ python create_cluster.py --delete
```
