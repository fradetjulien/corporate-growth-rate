import click
from selenium import webdriver

def compute_profit_margin(data):
    '''
    Compute the profit margin for each year
    '''
    try:
        index = 0
        while index < len(data["net_income"]) and index < len(data["total_revenue"]):
            data["profit_margin"].append(round((data["net_income"][index]\
                                                / data["total_revenue"][index]), 4))
            index = index + 1
    except:
        print('Sorry, error while computing Profit Margin.')
    return data

def compute_growth_rate(data):
    '''
    Compute the year-on-year revenue growth
    '''
    try:
        past = 0
        present = 1
        while present < len(data["total_revenue"]):
            data["growth_rate"].append(round((data["total_revenue"][present] - data["total_revenue"][past])\
                                            / data["total_revenue"][past], 4))
            present = present + 1
            past = past + 1
        return data
    except:
        print("Sorry, error while computing the Growth rate.")

def refactor_data(data, variable):
    '''
    Convert values inside the Dictionnary in INT type
    '''
    new_list = []
    try:
        for item in data[variable]:
            item = int(item.replace(',', ''))
            new_list.append(item)
        if new_list:
            data[variable] = new_list
    except:
        print('Sorry, failure while converting values into INT.')
    return data

def compute_results(data):
    '''
    Determine the annual growth rate as well as the profit margin
    '''
    data = refactor_data(data, 'total_revenue')
    data = refactor_data(data, 'net_income')
    data = compute_growth_rate(data)
    data = compute_profit_margin(data)
    print(data)
    return data

def scrap_values(data, driver, path, variable):
    '''
    Scrap values of the Company from the data table previously loaded
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
    Scrap the Company name from the data table previously loaded
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
        "dates": [],
        "growth_rate": [],
        "profit_margin": []
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

def is_result(driver, path, error_message):
    '''
    Check if the loaded page has find the data
    '''
    try:
        error = driver.find_element_by_xpath(path)
        if error and error_message in error.text:
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
        if is_result(driver, '//*[@id="lookup-page"]/section/div/h2/span', 'Symbols similar to') \
           or is_result(driver, '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span', 'N/A'):
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
            data = scrap_data(driver)
            data = compute_results(data)
            driver.quit()
            break

if __name__ == '__main__':
    cli()
