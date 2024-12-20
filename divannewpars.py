import scrapy
import csv

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/perm/category/svet"]

    def __init__(self):
        # Создаём список для хранения собранных данных
        self.parsed_data = []

    def parse(self, response):
        svets = response.css('div.LlPhw')
        for svet in svets:
            # Собираем данные и добавляем их в список
            item = {
                'name': svet.css('div.lsooF span::text').get(),
                'price': svet.css('div.pY3d2 span::text').get(),
                'url': svet.css('a').attrib['href']
            }
            self.parsed_data.append([item['name'], item['price'], item['url']])

    def closed(self, reason):
        # Сохранение данных в CSV при завершении работы паука
        with open("svet.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Записываем заголовки
            writer.writerow(['Название', 'Цена', 'Ссылка'])
            # Записываем данные
            writer.writerows(self.parsed_data)
