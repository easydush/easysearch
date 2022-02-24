import lxml
import scrapy
import logging


class CommonSpider(scrapy.Spider):
    name = 'common'
    start_urls = ['https://vc.ru/flood/170561-chto-delat-esli-skuchno-500-ssylok-sobrannyh-za-polgoda']

    def parse(self, response):
        urls = [link for link in response.selector.xpath('//a/@href').getall() if
                not (str(link).startswith('#') or str(link).startswith('/') or 'moz.com' in str(link))]
        for num, url in enumerate(urls):
            logging.debug(f'{num} {url}')
            yield response.follow(url, callback=self.parse_url, meta={'num': num})

    def parse_url(self, response):
        num = response.meta.get('num')
        with open('../index.txt', 'a') as f:
            f.write(f'{num} {response.url} \n')
            f.close()
        filename = f"../pages/{num}.txt"
        tree = lxml.html.fromstring(response.body)
        all_text = tree.text_content().strip()
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(all_text)
        logging.info(f'Saved file {filename}')
