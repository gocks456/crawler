import requests
from bs4 import BeautifulSoup

import json


class KCI(object):

    def crawler(self):

        # 자연과학: C 
        # 공학: D
        # 의약학: E
        # 농수해양학: F
        kci_data = [
                        {
                                'major':'자연과학', 
                                'code':'C'
                                },
                        {
                                'major':'공학',
                                'code':'D'
                                },
                        {
                                'major':'의약학',
                                'code':'E'
                                },
                        {
                                'major':'농수해양학',
                                'code':'F'
                                }
                        ]

        # post headers
        headers = {
                        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
                        }

        # 대분류 클릭 url
        big_category_url = 'https://www.kci.go.kr/kciportal/po/search/poFielResearchTrendList.kci'

        for category in kci_data:
            code = category['code']
            big_category_data = {
                            'clasSearchBean.largMajorCd': code,
                            'clasSearchBean.middMajorCd': 'All',
                            'poResearchTrendSearchBean.largMajorCd': code,
                            'poResearchTrendSearchBean.yearFrom': '2017',
                            'poResearchTrendSearchBean.yearTo': '2021',
                            'poResearchTrendSearchBean.researchTrend': 'field'
                            }

            html = requests.post(big_category_url, data=big_category_data, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            select = soup.body.find_all('input', {'name':'poResearchTrendSearchBean.middMajorCds'})

            middleMajor = []

            for tag in select:
                temp = {}
                temp["name"] = tag['title']
                temp["code"] = tag['value']
                temp["keyword"] = self.get_keyword(code, temp["code"])
                middleMajor.append(temp)

            category['middleMajor'] = middleMajor

        return kci_data


    def get_keyword(self, majorCode, middleCode):
        # post headers
        headers = {
                        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
                        }
        # open keyword url
        keyword_url = 'https://www.kci.go.kr/kciportal/po/search/poKeywordListAjax.kci'

        key_word_data = {
                        'clasSearchBean.largMajorCd':majorCode,
                        'clasSearchBean.middMajorCd':'All',
                        'poResearchTrendSearchBean.largMajorCd':majorCode,
                        'poResearchTrendSearchBean.yearFrom':'2017',
                        'poResearchTrendSearchBean.yearTo':'2021',
                        'poResearchTrendSearchBean.middMajorCds':middleCode
                        }

        # html text를 넣어서 하위 키워드 이름 추출
        html = requests.post(keyword_url, data=key_word_data, headers=headers)
        json = html.json()
        data_list = json["list"]
        
        keyword_list = []
        for data in data_list:
            keyword_list.append(data["KWD"])

        return keyword_list

    def save(self, directory, file_name='kci_keyword.json', data=None):
        # data = json data
        if data == None:
            print("Data is None, auto crawler start!")
            data = self.crawler()
        with open(directory + file_name, 'w') as f:
            print(json.dump(data, f ,indent='\t', ensure_ascii=False))
