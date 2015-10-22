from app import app
import requests
from lxml import html
import json


@app.route("/")
@app.route('/index')
def hello():
    return "Hello World!"


@app.route("/deals")
def get_deals():
    try:
        deals = []
        page = requests.get('https://affiliate-program.amazon.in/offers')
        tree = html.fromstring(page.text)
        element = tree.get_element_by_id("tab-1")
        managedContent = element.find_class("managedContent")

        for content in managedContent:
            for table in content.xpath('table'):
                data = {}
                data['href'] = table.xpath('tr/td/a/@href')[0].replace('YourStoreID', 'bodyf01-21')
                data['heading'] = table.xpath('tr/td/h2')[0].text
                data['imgsrc'] = table.xpath('tr/td/a/img/@src')[0]
                element = table.find_class('rightcell')
                string = element[0].text_content()
                data['text'] = string.split('\n')[2]
                deals.append(data)
        json_data = json.dumps(deals)
    except Exception as e:
        return None   # Will log it later , for time being it none
    return json_data
