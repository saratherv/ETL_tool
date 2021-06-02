# prefect_scrapy_fastAPI
- This project scrapes data from https://www.msc.com/track-a-shipment, using ETL tool and loads data to postgres DB.


### Built With
* [Scrapy](https://github.com/scrapy/scrapy)
* [Prefect Flow](https://www.prefect.io/cloud/)
* [FastAPI](https://fastapi.tiangolo.com/)


## Getting Started

This project build with dockers and can be installed using minmal commands.

### Prerequisites
* [docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/saratherv/prefect_scrapy_fastAPI.git
   ```
2. Change directory
    ```sh
    cd prefect_scrapy_fastAPI
    ```
3. Run command 
   ```sh
   sudo docker-compose up --build
   ```
   
## Usage

- Visit http://0.0.0.0:8080/docs to see swagger.

### Assumptions and Considerations
- Aim is just to save data to database not refreshing it, thats why each time task executes we save copies of same data.
- Container and Bill of landing information was loading dynamically due to which had to use selenium to run headless browser and scrape html.
- The REST-API is just returning one row for each id not the list.
