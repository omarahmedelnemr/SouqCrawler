from bs4 import BeautifulSoup
import requests
import time
import pandas


class SouqCrawler():
    """
        SouqCrawler is a Tool To Scrape Souq.com in fast and Easy Way (average 16 product/seconds)\n
        getFor(Product Name) : Set products name for search procces\n
        start() : start scraping ,you can set a limit for scraped products'\n
        self.page :starting page\n
        self.data : the data\n
        self.showProcess : Print each step on the console
    """

    def __init__(self):
        self.url = ''
        self.current_url = ''
        self.before = 0
        self.after = 0
        self.page = 1
        self.maximum_pages = 0
        self.data = []
        self.total_products = 0
        self.showProccess = True
        self.productName = ''
        self.productName = ''

    def getFor(self, productName) -> object:
        self.url = f'https://egypt.souq.com/eg-en/{productName}/s/?as=1&section=2&page='
        self.productName = productName

    def start(self, limit=-1):
        if self.showProccess:  # Explain the Proccess
            print('Getting Information ...')
        current_url = self.url + '1'  # Fix Url For Current Page
        html = requests.get(current_url).text  # get html response
        soup = BeautifulSoup(html, 'html.parser')  # parse it to BeautifulSoup
        self.productName = soup.find(name='li', class_='crumbs').text
        self.total_products = self.getNum(soup.find(name='li', class_='total').text)  # get the total products number
        self.maximum_pages = round(self.total_products / 60)

        if self.showProccess:  # Explain the Proccess
            print(f'Collecting Data For {self.total_products} Product For {self.productName}...')
            self.before = time.time()  # set Start Time

        if self.total_products > limit and limit != -1:  # Apply The Limit On The Data Number
            self.total_products = limit
            if self.showProccess:  # Explain the Proccess
                print(f'Select First {self.total_products} Product Starting From Page {self.page}...')
        self.data = self.getData()

        if self.showProccess:  # Explain the Proccess
            self.after = time.time()  # Set End Time
            print(f'Data Collected in {self.after - self.before} Seconds')  # Calculate Total Time

    def getNum(self, num):  # Get Total Number Of Products
        num = num[2:]
        num = num.split('Items')
        num = num[0]
        num = num.split(',')
        num = int(''.join(num))
        return num

    def fixTitle(self, text):
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = text.replace('  ', '')
        return text

    def getData(self):  # Collecting The Data

        data = []
        while len(data) < self.total_products:
            # if self.page > self.maximum_pages:
            #     break;
            self.current_url = self.url + str(self.page)
            html = requests.get(self.current_url).text
            soup = BeautifulSoup(html, 'html.parser')
            img = soup.select('.single-item img')
            info = soup.select('.single-item .itemTitle')
            price = soup.select('.single-item .itemPrice')
            link = soup.select('.single-item .item-content .itemLink')
            for i in range(len(info)):  # Save Data For One Page
                if len(data) >= self.total_products:  # check if The Numebr Of The Data Reached The Given Limit
                    if self.showProccess:  # Explain the Proccess
                        print(f'Current Page {self.page} ,Collected Data {len(data)}')
                    return data
                singleItem = {
                    'img': img[i].get('data-src'),
                    'info': self.fixTitle(info[i].text),
                    'price': price[i].text,
                    'link': link[i].get('href')
                }
                data.append(singleItem)

            if self.showProccess:  # Explain the Proccess
                print(f'Current Page {self.page} ,Collected Data {len(data)}')

            self.page += 1

        return data

    def save(self, name=None):
        df = pandas.DataFrame(self.data)
        if name:
            df.to_csv(f'{name}.csv')
        else:
            df.to_csv(f'{self.productName}.csv')
