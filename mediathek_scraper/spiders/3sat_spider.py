import scrapy
from urlparse import urlparse, parse_qs
from scrapy.selector import Selector
from mediathek_scraper.items import MediathekScraperItem

class MediathekScraperSpider(scrapy.Spider):
    name = "3sat"
    start_urls = [
        "http://www.3sat.de/mediathek/?mode=verpasst0&type=1",
        "http://www.3sat.de/mediathek/?mode=sendungenaz"
    ]

    def parse(self, response):
        for href in response.css(".BoxHeadline a.MediathekLink::attr('href')"):
            query = parse_qs(urlparse(href.extract()).query)
            id = query.get('obj')
            if not id:
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse)
            else:
                url = "http://www.3sat.de/mediathek/xmlservice/web/beitragsDetails?id=" + id[0]
                yield scrapy.Request(url, callback=self.parse_item)

        next_page = response.css('a.TargetDimFull::attr("href")')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, callback=self.parse)

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