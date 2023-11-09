# irr_calculator
## Introduction
Python solution that calculates irr for a set of entities.

## Execution
On this section you will find how to run the code locally.

### Python environment
To execute the solution with your machine you will need an environment with python 3.10.0 and the libraries listed in 
requirements.txt. In case you do not have such environment, you can create it as follows with conda:
 
```
conda create -n [] python=3.10.0 pip
pip install -r cloud_function/requirements.txt
```

### Testing

To execute the Python tests use next command on the CLI:

```commandline
python -m pytest -vv
```

It is needed a _.env_ file with the next settings:

```
PROJECT=
SOURCE_TABLE=
DESTINATION_TABLE=
DATASET=
```

You will also need to provide a Service Account credentials or to use a user account with the right permissions to 
interact with BigQuery.