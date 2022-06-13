from uuid import uuid4
import scrapy
from urllib import request
import base64
from collections import OrderedDict
import re


class LittleFriendsSpider(scrapy.Spider):
    name = 'LittleFriendsSpider'
    start_urls = [
        'http://www.little-friends.ru/loss/?album_id=11&time_dog=all'
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
        posts_links = response.xpath('//div[@align="right"]/a/@href').extract()

        for l in posts_links:
            yield scrapy.Request(response.urljoin(l), callback=self.parse_post)

        # линки следующей страницы
        next_page = None
        if next_page:
            yield scrapy.Requestscr(response.urljoin(next_page), callback=self.parse)

    def parse_post(self, response):
        """

        https://poiskzoo.ru/kazan/najdena-sobaka/najdena-sobaka-kazan-94897.html

        :param response:
        :return:
        """

        data = []
        message_id = str(uuid4())
        source = 'little-friends.ru'

        text = response.xpath('//text()').extract()

        # адрес
        try:
            address = text[text.index('Где: ') + 1]
        except Exception as e:
            print(e)
            address = None

        # текст объявления
        msg = response.xpath('//table/tr/td/img/@title').extract_first()

        # название объявления
        caption = response.xpath('//title/text()').extract_first()

        # вид млекопитающего
        animal_type = 'собака'

        # дата размещения
        try:
            date = text[text.index('Когда: : ') + 1]
            date = date.replace(' г.', '')
            year = int(date.split(' ')[-1])
            if year < 2017:
                return None
        except Exception as e:
            print(e)
            date = None

        # контакты
        try:
            contacts_phone = text[text.index('Контакты: ') + 1]
        except Exception as e:
            print(e)
            contacts_phone = None

        # изображения
        img_list = response.xpath('//table/tr/td/img/@src').extract()
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
            'entity': 'address',
            'value': address
        })
