import scrapy

class PagesSpider(scrapy.Spider):
    name = "pages"

    def start_requests(self):
        urls = [
            f'https://er.ru/party/program/?page={i}'
            for i in range(2, 19)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url[-2:]
        if page[0] == '=':
          page = page[1]

        filename = f'/content/scrap_ur/program_text/page_{page}.txt'
        with open(filename, 'w') as f:
            f.write(response.xpath("//div[@class='download__title']/text()").get() + '\n')
            
            title = response.xpath("//p[@class='MsoNormal']//strong/span/text()").get()
            if title is not None:
              f.write(title + '\n')

            for text in response.xpath("//p[@class='MsoNormal']/span/text()").getall():
              f.write(text + '\n')

        self.log(f'Saved file {filename}')
