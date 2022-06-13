from uuid import uuid4
import scrapy
from urllib import request
import base64
from collections import OrderedDict
import re


class PoiskZooSpider(scrapy.Spider):
    name = 'PoiskZooSpider'
    start_urls = [
        'https://poiskzoo.ru/najdena'
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
    }

    def parse(self, response):
        """

        :param response:
        :return:
        """

        # линки постов
        posts_links = response.xpath('//div[contains(@class, "podronee  blockdivbaza")]/a/@href').extract()
        # удаляем дубликаты
        posts_links = list(OrderedDict.fromkeys(posts_links))
        for l in posts_links:
            yield scrapy.Request(response.urljoin(l), callback=self.parse_post)

        # линки следующей страницы
        next_page = response.xpath('//div[@class="pagebar"]/a[text()="Следующая"]/@href').extract()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_post(self, response):
        """

        https://poiskzoo.ru/kazan/najdena-sobaka/najdena-sobaka-kazan-94897.html

        :param response:
        :return:
        """

        data = []
        message_id = str(uuid4())
        source = 'poiskzoo.ru'

        # регион
        region = response.xpath('//span[@class="bd_item_city" and @itemprop="addressLocality"]/a/text()').extract()
        # region = garbage_cleaner(','.join(region))

        # адрес
        address = response.xpath('//strong[text()="Адрес где искать:"]/text()/following::text()[1]').extract()
        # address = re.sub('\n', '', address)

        # порода
        animal_breed = response.xpath('//strong[text()="Порода:"]/text()/following::text()[1]').extract()

        # пол
        animal_sex = response.xpath('//strong[text()="Пол животного:"]/text()/following::text()[1]').extract()

        # цвет
        animal_color = response.xpath('//strong[text()="Окрас:"]/text()/following::text()[1]').extract()
        # animal_color = re.sub('\n', '', animal_color)

        # текст объявления
        msg = response.xpath('//div[@itemprop="description"]/text()').extract()
        msg = ' '.join(msg)
        # msg = garbage_cleaner(msg)

        # название объявления
        caption = response.xpath('//div[@itemprop="description"]/h1/text()').extract()

        # вид млекопитающего
        animal_type = ''
        if 'собака' in caption:
            animal_type = 'собака'
        if ('кошка' in caption) | ('кот' in caption):
            animal_type = 'кошка'

        # дата размещения
        try:
            date = response.xpath('//span[@class="bd_item_date"]/text()').extract()
            date = date.replace(' г.', '')
            year = int(date.split(' ')[-1])
            if year < 2017:
                return None
        except Exception as e:
            print(e)
            date = None

        # контакты
        contacts_phone = \
            response.xpath('//strong[text()="Ссылка на объявление:"]/following-sibling::text()[1]').extract()

        # изображения
        img_list = response.xpath('//meta[@itemprop="image"]/@content').extract()
        for img_link in set(img_list):
            try:
                img_link = response.urljoin(img_link)
                img_file = request.urlopen(img_link).read()
                encoded = base64.b64encode(img_file).decode()

                data.append({
                    'message_id': message_id,
                    'entity': 'img',
                    'value': encoded,
                    'img_link': img_link
                })
            except Exception as e:
                print(img_link)
                print(e)

        data.append({
            'message_id': message_id,
            'entity': 'рубрика',
            'value': 'Найдена ' + animal_type
        })

        data.append({
            'message_id': message_id,
            'entity': 'вид млекопитающего',
            'value': animal_type
        })

        # url данного обявления
        data.append({
            'message_id': message_id,
            'entity': 'url',
            'value': response.request.url
        })

        data.append({
            'message_id': message_id,
            'entity': 'source',
            'value': source
        })

        data.append({
            'message_id': message_id,
            'entity': 'название объявления',
            'value': caption
        })

        data.append({
            'message_id': message_id,
            'entity': 'msg',
            'value': msg
        })

        data.append({
            'message_id': message_id,
            'entity': 'date',
            'value': date
        })

        data.append({
            'message_id': message_id,
            'entity': 'contacts_phone',
            'value': contacts_phone
        })

        data.append({
            'message_id': message_id,
            'entity': 'animal_breed',
            'value': animal_breed
        })

        data.append({
            'message_id': message_id,
            'entity': 'animal_color',
            'value': animal_color
        })

        data.append({
            'message_id': message_id,
            'entity': 'animal_sex',
            'value': animal_sex
        })

        data.append({
            'message_id': message_id,
            'entity': 'region',
            'value': region
        })

        data.append({
            'message_id': message_id,
            'entity': 'address',
            'value': address
        })


