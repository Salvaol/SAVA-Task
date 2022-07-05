# SAVA - ETL

Python script to Extract, Transform and Load pssession files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Next items need to be installed and properly configured to ensure the tests work without any problem:
* Python 3.8
* pytest module

```
pip install pytest
```

## Running the tests

```
pytest tests
```

### Executing the ETL

```
Python <path to main>/main.py <container> <batch> <filename or wildcard> <Title of the curve>
```
Example:

```
C:\Users\Salva\PycharmProjects\SAVA-Task\venv\Scripts\python.exe C:/Users/Salva/PycharmProjects/SAVA-Task/ETL/main.py data batch1 * "OCP E vs t"
```
### Possible Future Steps
 1. Create connections to a SQL Database, Sharepoints or Blob Storadge
 2. Create Ingestions for different kind of files (csv, excel, parquet)
 3. Create Transformations for those files
 4. Upload those results to a NoSQL Database,  sharepoint, Blob, etc...


### Break down into end to end tests

Each test covers one execution step and all tests must start with 'test_' preffix

## Built With

* [pytest](https://pytest.org/en/latest/) - The test framework used

## Authors

* **Salvador Ollero** - *Initial work*

