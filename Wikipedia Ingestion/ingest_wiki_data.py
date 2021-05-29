import mysql.connector
import gzip
import shutil
import requests
import config
import os
import glob
import logging

logging.basicConfig(filename='ingestion.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

url_base = 'https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-'

files = glob.glob('./scripts/*')
for f in files:
    os.remove(f)

logging.info("old scripts deleted.")

cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD,
                              host=config.MYSQL_HOST,
                              database=config.MYSQL_DB)
cursor = cnx.cursor(dictionary=True)

logging.info("Connection has been established successfully with AWS RDS MySql.")

for table in config.tables_list:
    url = url_base + table + '.sql.gz'
    r = requests.get(url, stream=True)
    gz_save_path = './scripts/' + table + '.sql.gz'
    with open(gz_save_path, "wb") as f:
        r = requests.get(url)
        f.write(r.content)

    script_file = './scripts/' + table + '.sql'
    with gzip.open(gz_save_path, 'rb') as f_in:
        with open(script_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    logging.info("script file has been created.")

    drop_query = "DROP TABLE IF EXISTS " + table + ";"
    cursor.execute(drop_query)
    logging.info("%s table has been dropped.", table)

    with open(script_file, 'r', encoding="utf8") as sql_file:
        result_iterator = cursor.execute(sql_file.read(), multi=True)
        for res in result_iterator:
            print("Running query: ", res)  # Will print out a short representation of the query
            print(f"Affected {res.rowcount} rows")

        cnx.commit()

    logging.info("Data insertion completed successfully for: %s", table)

# creating top10 categories with outdated pages table
with open('top10_outdated.sql', 'r', encoding="utf8") as sql_file:
    result_iterator = cursor.execute(sql_file.read(), multi=True)
    for res in result_iterator:
        print("Running query: ", res)  # Will print out a short representation of the query
        print(f"Affected {res.rowcount} rows")

logging.info("Data has been loaded for top 10 categories with outdated pages.")
cnx.commit()
