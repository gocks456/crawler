import requests
from bs4 import BeautifulSoup

import json

class FilterByTask(object):

    def crawler(self):
        url = 'https://paperswithcode.com/datasets'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        select = soup.body.find_all('div', {'class':'datasets-filter p-md-2 p-lg-3'})

        text_data = str(select[1])

        soup = BeautifulSoup(text_data, 'lxml')
        select = soup.body.find_all('a', {'class':'filter-item'})

        task_list = []

        tasks = {}

        temp = []

        for a_tag in select:
            href = a_tag["href"]
            data = str(a_tag).split("page=1\">")[1].split("<span class")[0]

            name = data.strip()
            temp.append(name)

        tasks['tasks'] = temp
        task_list.append(tasks)

        return task_list

    def save(self, directory, file_name="papers_with_code_task_list.json", data=None):
        # data = json data
        if data == None:
            print("Data is None, auto crawler start!")
            data = self.crawler()
        with open(directory + file_name, 'w') as f:
            print(json.dump(data, f ,indent='\t'))
