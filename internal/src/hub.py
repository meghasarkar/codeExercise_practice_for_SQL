import psycopg2

"""Parameterized the value for output table name 'supplier_score_metrics'. """
outTable = 'supplier_score_metrics'

"""Connect to database server to run create table statement. Change the password value """
connect2DB = psycopg2.connect(dbname='practiceDB', host='localhost', port='5432', user='postgres',
                              password='$$$$$$$')
cur2DB = connect2DB.cursor()

"""Create a New table for dumping the metrics table"""
createTableStatement = 'CREATE TABLE IF NOT EXISTS ' + outTable + '( calculated_at DATE DEFAULT CURRENT_TIMESTAMP,' \
                                                                  'supplier_id INT NOT NULL,' \
                                                                  'metrics VARCHAR, ' \
                                                                  'values VARCHAR );'
cur2DB.execute(createTableStatement)
connect2DB.commit()

"""The SELECT command for the query to find the Supplier ID (hub_id) who accepted order 
(event = 'order/execute/customer/status/payment') """
accepted_supplierID = "SELECT data -> 'hub_id' FROM \"MY_TABLE\" WHERE name = 'order/execute/customer/status/payment'" \
                      " group by data -> 'hub_id'"

cur2DB.execute(accepted_supplierID)
list_supplierID = cur2DB.fetchall()

for record in list_supplierID:
    """The rate of ratio calculation where acceptance_count gives total count of payment for a particular hub_id 
    and acceptance_rate looks for count by total order submitted"""
    acceptance_count = "SELECT count(data -> 'event') FROM \"MY_TABLE\" " \
                       "WHERE name = 'order/execute/customer/status/payment' and cast(data->>'hub_id' as integer) = " + \
                       record[0]
    cur2DB.execute(acceptance_count)
    ((acceptance_count_result,),) = cur2DB.fetchall()

    acceptance_rate = "SELECT round( " + str(acceptance_count_result) + " " + " * 100.0/(select count(data -> 'event') " \
                                                                              "FROM \"MY_TABLE\" where name = " \
                                                                              "'order/execute/customer/status" \
                                                                              "/processing'))"
    cur2DB.execute(acceptance_rate)
    ((acceptance_rate_result,),) = cur2DB.fetchall()
    percent_acceptance = str(acceptance_rate_result) + '%'

    """Query for listing the rate ratio by adding 2 terms in data review_value_speed and review_value_print_quality to 
    the average"""
    review_rate = "SELECT round(avg(cast(data->> 'review_value_speed'as integer)+(cast(data->> " \
                  "'review_value_print_quality'as integer)))/2) FROM \"MY_TABLE\" WHERE name = " \
                  "'node/review/created' and cast(data->>'hub_id' as integer) = " + record[0]
    cur2DB.execute(review_rate)
    ((review_rate_result,),) = cur2DB.fetchall()
    percent_review = str(review_rate_result)

    """The current date SELECT Query"""
    calculated_at = "SELECT CURRENT_DATE"

    """Query for committing the values into the TABLE test"""
    for metric in ('acceptance_ratio', 'average_rating'):
        if metric == 'acceptance_ratio':
            dump_output = "INSERT INTO " + outTable + " VALUES (( " + calculated_at + "), " + record[0] + ", '" + metric \
                          + "' , '" + percent_acceptance + "' )"
            cur2DB.execute(dump_output)
        else:
            dump_output = "INSERT INTO " + outTable + " VALUES (( " + calculated_at + "), " + record[0] + ", '" + metric\
                          + "' , '" + percent_review + "' )"
            cur2DB.execute(dump_output)
            connect2DB.commit()
