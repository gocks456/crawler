import requests
from bs4 import BeautifulSoup

import json

class HuggingFace(object):

    def crawler(self):
        url = 'https://huggingface.co/datasets'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        select = soup.body.find_all('a', {'class':'tag-red'})

        task_category = []

        for a_tag in select:
                name = a_tag.get_text(strip=True)
                name = name.replace('-', ' ')
                task_category.append(name)
        
        print(len(task_category))

        select = soup.body.find_all('a', {'class':'tag-purple'})
        task = []
        for a_tag in select:
                name = a_tag.get_text(strip=True)
                name = name.replace('-', ' ')
                task.append(name)

        print(len(task))

        temp ={}
        temp["task_category"] = task_category
        temp["task"] = task

        task_list = []
        task_list.append(temp)
        return task_list

    def save(self, directory, file_name='hugging_face_task_list.json', data=None):
        # data = json data
        if data == None:
            print("Data is None, auto crawler start!")
            data = self.crawler()
        with open(directory + file_name, 'w') as f:
            print(json.dump(data, f ,indent='\t'))
