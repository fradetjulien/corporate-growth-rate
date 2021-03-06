import click
from selenium import webdriver
from matplotlib import pyplot as plt

def build_growth_rate_graph(data):
    '''
    Build the Company Growth Rate graphic
    '''
    try:
        if data["dates"] and data["growth_rate"]:
            plt.figure(1)
            plt.subplot(2, 1, 2)
            plt.plot(data["dates"][1:], data["growth_rate"])
            plt.grid(True)
            plt.ylabel("% of Growth Rate")
            plt.xlabel("Years")
            plt.title("{} Growth Rate".format(data["company_name"]))
            plt.tight_layout()
            plt.show()
    except Exception as error:
        print("Sorry, unable to create the Graphic for the Growth Rate.\n{}".format(error))

def build_profit_margin_graph(data):
    '''
    Build the Company Profit Margin graphic
    '''
    try:
        if data["dates"] and data["profit_margin"]:
            plt.figure(1)
            plt.subplot(2, 1, 1)
            plt.plot(data["dates"], data["profit_margin"])
            plt.grid(True)
            plt.ylabel("% of Profit Margin")
            plt.xlabel("Years")
            plt.title("{} Profit Margin".format(data["company_name"]))
        build_growth_rate_graph(data)
    except Exception as error:
        print("Sorry, unable to create the Graphic for the Profit Margin.\n{}".format(error))

def compute_profit_margin(data):
    '''
    Compute the profit margin for each year
    '''
    try:
        index = 0
        while index < len(data["net_income"]) and index < len(data["total_revenue"]):
            data["profit_margin"].append(round((data["net_income"][index]\
                                                / data["total_revenue"][index]), 4) * 100)
            index = index + 1
    except Exception as error:
        print('Sorry, error while computing Profit Margin.\n{}'.format(error))
    return data

def compute_growth_rate(data):
    '''
    Compute the year-on-year revenue growth
    '''
    try:
        past = 0
        present = 1
        while present < len(data["total_revenue"]):
            data["growth_rate"].append(round((data["total_revenue"][present] -\
                                            data["total_revenue"][past])\
                                            / data["total_revenue"][past], 4) * 100)
            present = present + 1
            past = past + 1
        return data
    except Exception as error:
        print("Sorry, error while computing the Growth rate.\n{}".format(error))

def refactor_dates(data):
    '''
    Convert date format from 'day/month/year' to 'year'
    '''
    try:
        years = []
        for item in data["dates"]:
            if item == 'TTM':
                years.append(item)
            else:
                years.append(int(item[-4:]))
        years.reverse()
        data["dates"] = years.copy()
        del years
    except Exception as error:
        print('Sorry, failure while converting date format from "day/month/year" to "year"\n{}'.format(error))
    return data

def refactor_data(data, variable):
    '''
    Convert values inside the Dictionnary in INT type
    '''
    try:
        true_numbers = []
        for item in data[variable]:
            item = int(item.replace(',', ''))
            true_numbers.append(item)
        if true_numbers:
            true_numbers.reverse()
            data[variable] = true_numbers.copy()
            del true_numbers
    except Exception as error:
        print('Sorry, failure while converting values into INT.\n{}'.format(error))
    return data

def compute_results(data):
    '''
    Determine the annual growth rate as well as the profit margin
    '''
    data = refactor_data(data, 'total_revenue')
    data = refactor_data(data, 'net_income')
    data = refactor_dates(data)
    data = compute_growth_rate(data)
    data = compute_profit_margin(data)
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
    except Exception as error:
        print('Sorry, failure while retrieving {}.\n{}'.format(variable, error))
    return data

def scrap_company_name(data, driver):
    '''
    Scrap the Company name from the data table previously loaded
    '''
    try:
        data["company_name"] = driver.find_element_by_xpath(\
                               '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1').text
    except Exception as error:
        print('Sorry, failure while retrieving the company name.\n{}'.format(error))
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
        "profit_margin": [],
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
    return False

def load_data(ticker):
    """
    Launch a new Chrome driver instance, go to the Yahoo Finance website, then configure the search
    """
    try:
        driver = webdriver.Chrome(executable_path=".//chromedriver")
        driver.get("https://finance.yahoo.com/quote/" + ticker + "/financials?p=" + ticker)
        if is_result(driver, '//*[@id="lookup-page"]/section/div/h2/span', 'Symbols similar to') \
           or is_result(driver, '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span',
                        'N/A'):
            driver.quit()
            return None
    except Exception as error:
        print("Sorry, error while loading data.\n{}".format(error))
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
    Display the margin profit as well as the growth rate of a Company
    '''
    while True:
        ticker = handle_input('Please, choose a Company and insert the corresponding ticker :\n')
        driver = load_data(ticker)
        if driver:
            data = scrap_data(driver)
            data = compute_results(data)
            driver.quit()
            build_profit_margin_graph(data)
            break

if __name__ == '__main__':
    cli()
