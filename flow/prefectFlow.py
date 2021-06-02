from datetime import timedelta, datetime
from prefect import task
from prefect import Flow
from prefect.schedules import IntervalSchedule
from scrape import fetchData
from db_querries import connect_to_db, add_new_row_bol, add_new_row_containers
import prefect

logger = prefect.context.get("logger")


@task(max_retries=3, retry_delay=timedelta(minutes=1))
def extract():
    logger.info("Starting extract flow")
    containers = ["SEGU9765052", "MSCU4847068", "OTPU6030554"]
    bill_of_landing = ["MEDUC6599558", "MEDUAQ786421", "WWLLWYTN0101088", "MEDUPS216950"]
    data = fetchData(containers, bill_of_landing)
    logger.info("Data extraction done successfully")
    return data


@task
def transform(scraped_data):
    # filter list to houston realtors
    ### note: Leaving tranform flow empty so that if required can trannform json to other formats 
    ### If we plan to change db schema
    logger.info("Traform data here ")
    return scraped_data


@task(max_retries=3, retry_delay=timedelta(minutes=1))
def load(scraped_data):
    # store data into database
    logger.info("starting database operations in load flow")
    db = connect_to_db()
    for data in scraped_data["bill_of_landing_data"]:
        add_new_row_bol(data, db)
    for data in scraped_data["containers_data"]:
        add_new_row_containers(data, db)
    logger.info("database querries executed successfully")


if __name__ == "__main__":
    logger.info("..........................starting prefect flow..........................")
    schedule = IntervalSchedule(
            start_date=datetime.utcnow() + timedelta(seconds=1),
            interval=timedelta(minutes=5))
    with Flow("SCRAPE-Data", schedule=schedule) as flow:
        scraped_data = extract()
        transformed_data = transform(scraped_data)
        load_to_database = load(transformed_data)

    flow.run()