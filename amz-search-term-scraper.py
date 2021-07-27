import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class crawlArticle():
    def __init__(self, title, price):
        self.title = title
        self.price = price

class b:

    def article(self, name):
        count = 1
        page = 1
        pageIncrement = 16
        maxRetrieves = 32
        a = []

        url = 'https://amazon.com/s?k=' + name + "&page=" + str(page)

        options = Options()
        options.headless = False
        options.add_experimental_option("detach", True)

        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser.maximize_window()
        browser.get(url)
        browser.set_page_load_timeout(10)

        while True:
            try:
                if pageIncrement*page > maxRetrieves+pageIncrement:
                    break

                if count > pageIncrement:
                    count = 1
                    page += 1

                #Get Title
                xPathTitle = '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[' + str(count) + ']/div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a/span'

                title = browser.find_element(By.XPATH, xPathTitle)
                titleText = title.get_attribute("innerHTML").splitlines()[0]
                title.click()

                print(f'count: {count}')

                xPathPrice = '//*[@id="price_inside_buybox"]'
                price = browser.find_element_by_xpath(xPathPrice)
                priceText = price.get_attribute("innerHTML")

                url = 'https://amazon.com/s?k=' + name + "&page=" + str(page)
                browser.get(url)
                browser.set_page_load_timeout(10)

                info = crawlArticle(titleText, priceText)
                print(f'info: {info}')
                print(f'title: {titleText}')
                print(f'price: {priceText}')
                a.append(info)

                count += 1

            except Exception as e:
                print("Expcetion", count, e)
                count += 1

                if pageIncrement*page > maxRetrieves:
                    break

                if count > pageIncrement:
                    count = 1
                    page += 1

                url = 'https://amazon.com/s?k=' + name + "&page=" + str(page)
                browser.get(url)
                browser.set_page_load_timeout(10)

        return a

fetcher = b()

with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    articleWriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    for article in fetcher.article('iphone 12'):
        articleWriter.writerow([article.title, article.price.strip()])
        print(article.title + " " + article.price.strip())
