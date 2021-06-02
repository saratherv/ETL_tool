import json
from sqlalchemy import create_engine


db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'



# Connecto to the database
def connect_to_db():
    db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    db = create_engine(db_string)
    return db


# Get data from bill of landing table

def get_bill_of_landing_data(db, bol_id):
    query = f"""
        SELECT * FROM bill_of_lading_bookmarks WHERE bill_of_landing_id = '{bol_id}';
    """
    result_set = db.execute(query)
    for (r) in result_set:
        return r


def get_container_data(db, container_id):
    query = f"""
        SELECT * FROM container_no_bookmarks WHERE container_id = '{container_id}';
    """
    result_set = db.execute(query)
    for (r) in result_set:
        return r
