import scrapy
import json
from urlparse import urlparse, parse_qs
from scrapy.selector import Selector
from mediathek_scraper.items import MediathekScraperItem

class MediathekScraperSpider(scrapy.Spider):
    name = "ard"
    letters = "0-9 A B C D E F G H I K L M N O P Q R S T U V W Z".split(' ')
    start_urls = ["http://www.ardmediathek.de/tv/sendungen-a-z?buchstabe=" + l for l in letters]

    def parse(self, response):
        for href in response.css("div.teaser a.mediaLink::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_show)

    def parse_show(self, response):
        for href in response.css("div.teaser div.media a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)

        next_page = response.css('a[aria-labelledby="cursorRight"]:not([aria-disabled="true"])::attr("href")')
        if next_page:
          url = response.urljoin(next_page[0].extract())
          yield scrapy.Request(url, callback=self.parse_show)

    def parse_item(self, response):
      item = MediathekScraperItem()

      item['id'] =  parse_qs(urlparse(response.url).query)['documentId'][0]
      item['channel'] = response.xpath('//meta[@itemprop="productionCompany"]/@content').extract_first()

      item['title'] = response.xpath("//meta[@name='dcterms.title']/@content").extract_first()
      item['description'] = response.xpath('//p[@itemprop="description"]/text()').extract_first()
      item['url'] = response.xpath('//meta[@itemprop="url"]/@content').extract_first()
      # item['fsk'] = response.xpath('details/fsk/text()').extract_first() # TODO

      item['show'] = response.xpath('//meta[@name="dcterms.isPartOf"]/@content').extract_first()

      item['date'] = response.xpath('//meta[@name="dcterms.date"]/@content').extract_first()
      item['ttl'] = response.xpath('//meta[@itemprop="expires"]/@content').extract_first()
      item['duration'] = response.xpath('//meta[@property="video:duration"]/@content').extract_first()

      url = "http://www.ardmediathek.de/play/media/%s?devicetype=pc&features=flash" % item['id']
      yield scrapy.Request(url, callback=self.parse_files, meta={'item': item})

    def parse_files(self, response):
      jsonresponse = json.loads(response.body_as_unicode())

      item = response.meta['item']
      item['type'] = jsonresponse['_type']
      item['geo'] = jsonresponse['_geoblocked']

      item['files'] = {}
      item['files']['hd'] = {}
      item['files']['hd']['url'] = [v for v in jsonresponse['_mediaArray'][0]['_mediaStreamArray'] if v['_quality'] == 3][0].get('_stream', '')
      item['files']['high'] = {}
      item['files']['high']['url'] = [v for v in jsonresponse['_mediaArray'][0]['_mediaStreamArray'] if v['_quality'] == 2][0].get('_stream', '')
      item['files']['low'] = {}
      item['files']['low']['url'] = [v for v in jsonresponse['_mediaArray'][0]['_mediaStreamArray'] if v['_quality'] == 1][0].get('_stream', '')

      yield item
