import click
from selenium import webdriver

def scrap_data(driver):
    '''
    Scrap the total revenue and the net income
    '''
    return

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
        if is_result_empty(driver):
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
