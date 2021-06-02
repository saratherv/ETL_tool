from typing import Optional
from db_querries import connect_to_db, get_bill_of_landing_data, get_container_data
import uvicorn
from fastapi import FastAPI


app = FastAPI()



@app.get("/search_bill_of_landing/{bol_id}")
def read_item(search_id: str):
    db = connect_to_db()
    data = get_bill_of_landing_data(db, search_id)
    return {"data": data}

@app.get("/search_container/{container_id}")
def read_item(container_id: str):
    db = connect_to_db()
    data = get_container_data(db, container_id)
    return {"data": data}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')



