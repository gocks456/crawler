import requests
from bs4 import BeautifulSoup

import json

class Methods(object):

    def crawler(self):
        methods_list = self.base_crawler()

        for method in methods_list:
            for key, value in method.items():
                category_list = []
                category = self.category_crawler(value["href"])
                category_list.append(category)
                method[key]["category"] = category_list

    def base_crawler(self):
        url = 'https://paperswithcode.com/methods/'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        select = soup.body.find_all('h4')

        area_list = []

        for h4 in select:
            area = {} # key: area 이름 / value: 주소
            #print(type(h4))
            name = h4.get_text(strip=True)
            href = str(h4).split('<a href=\"')[1].split('\">')[0]

            temp = {}
            temp["href"] = href

            area[name] = temp
            area_list.append(area)

        return area_list


    def category_crawler(self, href):
        url = 'https://paperswithcode.com'
        html = requests.get(url+href)
        soup = BeautifulSoup(html.text, 'lxml')
        select = soup.body.find_all('h2')

        category = {}

        for h2 in select:
            name = h2.get_text(strip=True)
            href = str(h2).split('<a href=\"')[1].split('\">')[0]

            temp = {}
            temp["href"] = href
            temp["methods"] = self.methods_crawler(href)

            category[name] = temp

        return category

    def methods_crawler(self, href):
        url = 'https://paperswithcode.com'
        html = requests.get(url+href)
        soup = BeautifulSoup(html.text, 'lxml')
        select = soup.body.find_all('div', {'class':'method-image'})

        methods = []

        for text in select:
            name = text.get_text(strip=True)
            methods.append(name)

        return methods


    def save(self, directory, file_name="papers_with_code_methods.json", data=None):
        # data = json data
        if data == None:
            print("Data is None, auto crawler start!")
            data = self.crawler()
        with open(directory + file_name, 'w') as f:
            print(json.dump(data, f ,indent='\t'))
