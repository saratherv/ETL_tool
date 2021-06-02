from selenium import webdriver
import scrapy
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import prefect

logger = prefect.context.get("logger")


def configure_firefox_driver():
    # Add additional Options to the webdriver
    firefox_options = FirefoxOptions()
    # add the argument and make the browser Headless.
    firefox_options.add_argument("--headless")

    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # if driver is in PATH, no need to provide executable_path
    driver = webdriver.Firefox(options = firefox_options)
    logger.info('Loaded Firefox Driver')
    return driver 


def extractBOLData(table):
    table_body = table.xpath(".//tbody")
    body_rows = table_body.xpath(".//tr//td//span//text()")
    table_head = table.xpath(".//thead")
    head_rows = table_head.xpath(".//tr//th")
    data = {}
    for index in range(0, len(head_rows)):
        data[head_rows[index].xpath(".//text()").extract_first()] = body_rows[index].extract()
    return data


##### Refactor this to make it more generic currently doing as per records in table
def extractMetaTable(table):
    table_body = table.xpath(".//tbody")
    table_rows = table_body.xpath(".//tr")
    data = {}
    data[table_rows[0].xpath(".//th//text()")[0].extract()] = table_rows[1].xpath(".//td//span//text()")[0].extract().strip(' \t\n\r\xa0').replace("'", "inch")
    data[table_rows[0].xpath(".//th//text()")[1].extract()] = table_rows[1].xpath(".//td//span//text()")[1].extract().strip(' \t\n\r\xa0')
    data[table_rows[2].xpath(".//th//text()")[0].extract()] = table_rows[3].xpath(".//td//span//text()")[0].extract().strip(' \t\n\r\xa0')
    data[table_rows[2].xpath(".//th//text()")[1].extract()] = table_rows[3].xpath(".//td//span//text()")[1].extract().strip(' \t\n\r\xa0')
    return data


def extractDataTable(table):
    table_head = table.xpath(".//thead")
    head_rows = table_head.xpath(".//tr//th")
    header_list = [  ]
    #### Note - This could have been done in o(1) complexity instead of using for loop but to make it scalable I have written for loop here
    for row in head_rows:
        text = row.xpath(".//text()").extract_first()
        header_list.append(text)
    
    table_body = table.xpath(".//tbody")
    body_rows = table_body.xpath(".//tr")
    data_list = []
    for row in body_rows:
        tdata = row.xpath(".//td")
        data_dict = {}
        for index, data in enumerate(tdata):
            text = data.xpath(".//span//text()").extract_first().strip(' \t\n\r\xa0')
            # print("text", text)
            data_dict[header_list[index]] = text
        data_list.append(data_dict)
    return data_list


def fetchData(containers, bill_of_landing):
    containers_tracking_data = []
    for container in containers:
        driver = configure_firefox_driver()
        logger.info("fetching content for conatiner id  " +  container)
        try:
            driver.get("https://www.msc.com/track-a-shipment?agencyPath=arg")
            inp = driver.find_element_by_id("ctl00_ctl00_plcMain_plcMain_TrackSearch_txtBolSearch_TextField")
            inp.send_keys(container)
            driver.find_element_by_id("ctl00_ctl00_plcMain_plcMain_TrackSearch_hlkSearch").click()
            response = scrapy.Selector(text=driver.page_source.encode('utf-8'))
            
            table1 = response.xpath('//*[@id="ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_pnlBOLContent"]//table[1]')
            data = extractMetaTable(table1)
            table2 = response.xpath('//*[@id="ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_pnlBOLContent"]//table[2]')
            table_data = extractDataTable(table2)
            containers_tracking_data.append({"container_id" : container, "meta_data" : data, "tracking_data" : table_data})
        except Exception as e:
            logger.warning(repr(e))
            logger.warning("Error extracting data for container...............", container)
        finally:
            logger.info("Closing driver successfully")
            driver.quit()
    
    bill_of_landing_dict = []
    for bol_id in bill_of_landing:
        driver = configure_firefox_driver()
        logger.info("fetching content for bill of landing id " + bol_id)
        try:
            driver.get("https://www.msc.com/track-a-shipment?agencyPath=arg")
            inp = driver.find_element_by_id("ctl00_ctl00_plcMain_plcMain_TrackSearch_txtBolSearch_TextField")
            inp.send_keys(bol_id)
            driver.find_element_by_id("ctl00_ctl00_plcMain_plcMain_TrackSearch_hlkSearch").click()
            response = scrapy.Selector(text=driver.page_source.encode('utf-8'))
            
            bol_data_table = response.xpath('//*[@class="resultTable singleRowTable"]')
            bill_of_landing_data = extractBOLData(bol_data_table)
            tables = response.xpath('//*[@class="containerAccordion"]//table')
            bol_container_tracking_data = []
            for index in range(0, len(tables), 2):
                table1 = tables[index]
                data = extractMetaTable(table1)
                table2 = tables[index + 1]
                table_data = extractDataTable(table2)
                bol_container_tracking_data.append({"meta_data" : data, "tracking_data" : table_data})
            bill_of_landing_dict.append({ "bill_of_landing_id" : bol_id, "bol_meta_data" :  bill_of_landing_data, "containers" : bol_container_tracking_data })
        except Exception as e:
            logger.warning(repr(e))
            logger.warning("Error extracting data for bill of landing id...............", bol_id)
        finally:
            logger.info("Closing driver successfully")
            driver.quit() 
    
    return {"bill_of_landing_data" : bill_of_landing_dict, "containers_data" : containers_tracking_data}
        
    
