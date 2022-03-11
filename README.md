
# Code Exercise for Hubs
The test exercise for technical evaluation
Data Engineer - Hubs





## Prerequisites
### Python 3.6.* or later.

See installation instructions at: https://www.python.org/downloads/

Check you have python3 installed:

```bash
python3 --version
```

### Preferably an IDE such as Pycharm Community Edition

https://www.jetbrains.com/pycharm/download/

### Postgres SQL 

Install postgres on local or EC2 machine for loading and execution of data and logic file.

```bash
postgres -V postgres (PostgreSQL) 9.3.10
```

### Set CRON job for daily execution of the program

-Check if you already have a crontab created.
```bash
crontab -l 
```
-Create a new Crontab
```bash
crontab -e
```
-In vi editor, add the below line for executing script at 2.30AM daily
```bash
30 2 * * * /usr/bin/python /internal/src/hub.py
```


## Installing Python requirements

This will install some of the packages you might find useful:

```bash
pip3 install -r ./external/requirements.txt
```

## Loading the data to Postgres

1. Open pgAdmin 4 and connect to local or remote database(as per your requirements)
2. Load the hubs_event.sql file from the import file available in the application.
3. Execute the query file and check for the loaded data by executing simple query of 
```bash
select * from "MY_TABLE";
```

## Execution of program from Pycharm
1. Start Pycharm application.
2. CLick on Open project and load the folder from *./hubs*
3. After the project is loaded, traverse to the main py file named hubs.py from *.\hubs\internal\src*
4. Run the application and wait for the response code to be 0 (No error)
5. Check for the output file from pgAdmin by quering
```bash
select * from "supplier_score_metrics";
```


## Author 

[@meghasarkar](https://www.linkedin.com/in/megha-sarkar-1c9/)



## Note:

Each function and flow of the program is explained in the *hubs.py* file itself for better illustration of content.


