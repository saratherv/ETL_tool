import time
import random
import json
from sqlalchemy import create_engine
import prefect

logger = prefect.context.get("logger")



db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'



# Connecto to the database
def connect_to_db():
    logger.info("Connecting to postgres db")
    db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    db = create_engine(db_string)
    return db


### Insert data 
def add_new_row_bol(data, db):
    
    bol_id = data["bill_of_landing_id"]
    meta = json.dumps(data["bol_meta_data"])
    containers = json.dumps(data["containers"])
    try:
        query = f"""
                INSERT INTO bill_of_lading_bookmarks(bill_of_landing_id, bol_meta_data, containers)
                VALUES('{bol_id}', '{meta}', '{containers}');
        """
        db.execute(query)
    except Exception as e:
        logger.error(repr(e))
        logger.error(json.dumps(data))


### Insert data
def add_new_row_containers(data, db):
    container_id = data["container_id"]
    meta_data = json.dumps(data["meta_data"])
    meta_data = json.dumps(data["tracking_data"])
    try:
        query = f"""
                INSERT INTO container_no_bookmarks(container_id, meta_data, tracking_data)
                VALUES('{container_id}', '{meta_data}', '{meta_data}');
                """
        db.execute(query)
    except Exception as e:
        logger.error(repr(e))
        logger.error(json.dumps(data))







