import scrapy
from urlparse import urlparse
from scrapy.selector import Selector
from mediathek_scraper.items import MediathekScraperItem

class MediathekScraperSpider(scrapy.Spider):
    name = "zdf"
    start_urls = ["http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-verpasst/day%s?flash=off" % n for n in range(0,8)] + \
                 ["http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz%s?flash=off" % n for n in range(0,10)]

    def parse(self, response):
        for href in response.css("div.beitragListe li > .image > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_show)

    def parse_show(self, response):
        for href in response.css("div.beitragListe li > .image > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_id)

        next_page = response.css('a.weitereBeitraege::attr("href")')
        if next_page:
          url = response.urljoin(next_page[0].extract())
          yield scrapy.Request(url, callback=self.parse_show)

    def parse_id(self, response):
        id = response.xpath('//div[@class="beitrag"]/div[@id="playerContainer"]/@class').extract()
        if id:
            yield scrapy.Request("http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?id=" + id[0], callback=self.parse_item)

    def parse_item(self, response):
        xml = Selector(response=response, type="xml").xpath('//response/video')

        item = MediathekScraperItem()
        item['id'] = xml.xpath('details/assetId/text()').extract_first()
        item['type'] = xml.xpath('type/text()').extract_first()
        item['channel'] = xml.xpath('details/channel/text()').extract_first()

        item['title'] = xml.xpath('information/title/text()').extract_first()
        item['description'] = xml.xpath('information/detail/text()').extract_first()
        item['url'] = xml.xpath('details/vcmsUrl/text()').extract_first()
        item['fsk'] = xml.xpath('details/fsk/text()').extract_first()
        item['geo'] = xml.xpath('details/geolocation/text()').extract_first()

        item['show'] = xml.xpath('details/originChannelTitle/text()').extract_first()

        item['date'] = xml.xpath('details/airtime/text()').extract_first()
        item['ttl'] = xml.xpath('details/timetolive/text()').extract_first()
        item['duration'] = xml.xpath("details/lengthSec/text()").extract_first()

        item['files'] = {}
        item['files']['hd'] = {}
        item['files']['hd']['url'] = 'http://nrodl.zdf.de' + [urlparse(u).path.replace('/ondemand/zdf/hbbtv', '') for u in xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "veryhigh"][facets/facet/text() = "hbbtv"]/url/text()').extract()][0]
        item['files']['hd']['size'] = xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "veryhigh"][facets/facet/text() = "hbbtv"]/filesize/text()').extract_first()
        item['files']['high'] = {}
        item['files']['high']['url'] = 'http://nrodl.zdf.de' + [urlparse(u).path.replace('/ondemand/zdf/hbbtv', '') for u in xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "hbbtv"]/url/text()').extract()][0]
        item['files']['high']['size'] = xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "hbbtv"]/filesize/text()').extract_first()
        item['files']['low'] = {}
        item['files']['low']['url'] = 'http://nrodl.zdf.de' + [urlparse(u).path for u in xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "progressive"]/url/text()').extract()][0]
        item['files']['low']['size'] = xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "progressive"]/filesize/text()').extract_first()

        yield item
