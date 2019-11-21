import click
from selenium import webdriver

def scrap_values(data, driver, path, variable):
    '''
    Scrap the Total Revenue of the Company from the data table loaded previously
    '''
    index = 1
    try:
        while index < 7:
            data[variable].append(driver.find_element_by_xpath(path.format(index)).text)
            index = index + 1
        data[variable].pop(0)
    except:
        print('Sorry, failure while retrieving {}.'.format(variable))
    return data

def scrap_company_name(data, driver):
    '''
    Scrap the Company name from the data table loaded previously
    '''
    try:
        data["company_name"] = driver.find_element_by_xpath(\
                               '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1').text
    except:
        print('Sorry, failure while retrieving Company name.')
    return data

def init_data():
    '''
    Initialize a new dictionnary and set empty variables inside
    '''
    data = {
        "company_name": None,
        "total_revenue": [],
        "net_income": [],
        "dates": []
    }
    return data

def scrap_data(driver):
    '''
    Scrap all needed values for future computes and store them into a dictionnary
    '''
    data = init_data()
    data = scrap_company_name(data, driver)
    data = scrap_values(data, driver,\
                       '//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/\
                       div[1]/div[2]/div[1]/div[1]/div[{}]', 'total_revenue')
    data = scrap_values(data, driver,\
                       '//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/\
                       div[1]/div[2]/div[11]/div[1]/div[{}]', 'net_income')
    data = scrap_values(data, driver,\
                        '//*[@id="Col1-1-Financials-Proxy"]/section/div[4]/div[1]/\
                        div[1]/div[1]/div/div[{}]', 'dates')
    return data

def is_result_available(driver):
    '''
    Check if the loaded page has available data
    '''
    try:
        path = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span'
        error = driver.find_element_by_xpath(path)
        if error and 'N/A' in error.text:
            return True
    except:
        return False

def is_result_empty(driver):
    '''
    Check if the loaded page has find the data
    '''
    path = '//*[@id="lookup-page"]/section/div/h2/span'
    try:
        error = driver.find_element_by_xpath(path)
        if error and 'Symbols similar to' in error.text:
            return True
    except:
        return False

def load_data(ticker):
    """
    Launch a new Chrome driver instance, go to the Yahoo Finance website, then configure the search
    """
    try:
        driver = webdriver.Chrome(executable_path=".//chromedriver")
        driver.get("https://finance.yahoo.com/quote/" + ticker + "/financials?p=" + ticker)
        if is_result_empty(driver) or is_result_available(driver):
            driver.quit()
            return None
    except:
        print("Error while loading data.")
        return None
    return driver

def handle_input(message):
    '''
    Retrieve the ticker value from the command line
    '''
    ticker = input(message)
    if not ticker.isalpha():
        handle_input('Wrong ticker, please insert a valid ticker :\n')
    return ticker

@click.group()
def cli():
    '''
    Scrapper combined with a graph builder
    '''

@cli.command('graph')
def corporate_profit_revenues():
    '''
    Display the total revenue and net income of a Company
    '''
    while True:
        ticker = handle_input('Please, choose a Company and insert the corresponding ticker :\n')
        driver = load_data(ticker)
        if driver:
            scrap_data(driver)
            driver.quit()
            break

if __name__ == '__main__':
    cli()
