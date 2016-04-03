import scrapy
import json
# from urlparse import urlparse, parse_qs
# from scrapy.selector import Selector
from mediathek_scraper.items import MediathekScraperItem

class MediathekScraperSpider(scrapy.Spider):
    name = "arte"
    start_urls = [
        "http://www.arte.tv/papi/tvguide/videos/plus7/program/D/L2/ALL/ALL/-1/AIRDATE_DESC/0/0/DE_FR.json",
        # "http://www.arte.tv/papi/tvguide/videos/plus7/program/F/L2/ALL/ALL/-1/AIRDATE_DESC/0/0/DE_FR.json"
    ]

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        print jsonresponse
        for show in jsonresponse['programDEList']:
            item = MediathekScraperItem()

            item['id'] = show['PID']
            item['type'] = "NONE" # TODO
            item['channel'] = 'ARTE.' + show['VDO']['language']

            item['title'] = show['TIT'] if not show.get('STL') else show['TIT'] + " - " + show.get('STL')
            item['description'] = show['DTW']
            item['url'] = show['permalink']
            item['fsk'] = show['mediaRatingD']
            item['geo'] = "NONE" # TODO

            item['show'] = show['VDO'].get('clusterTitle', show['GEN'])

            item['date'] = show['VDO']['VDA']
            item['ttl'] = "NONE" # TODO
            item['duration'] = show['VDO']['VDU'] * 60

            yield item

    # def parse_item(self, response):
    #     xml = Selector(response=response, type="xml").xpath('//response/video')

    #     item = MediathekScraperItem()
    #     item['id'] = xml.xpath('details/assetId/text()').extract_first()
    #     item['type'] = xml.xpath('type/text()').extract_first()
    #     item['channel'] = xml.xpath('details/channel/text()').extract_first()

    #     item['title'] = xml.xpath('information/title/text()').extract_first()
    #     item['description'] = xml.xpath('information/detail/text()').extract_first()
    #     item['url'] = xml.xpath('details/vcmsUrl/text()').extract_first()
    #     item['fsk'] = xml.xpath('details/fsk/text()').extract_first()
    #     item['geo'] = xml.xpath('details/geolocation/text()').extract_first()

    #     item['show'] = xml.xpath('details/originChannelTitle/text()').extract_first()

    #     item['date'] = xml.xpath('details/airtime/text()').extract_first()
    #     item['ttl'] = xml.xpath('details/timetolive/text()').extract_first()
    #     item['duration'] = xml.xpath("details/lengthSec/text()").extract_first()

    #     item['files'] = {}
    #     item['files']['hd'] = {}
    #     item['files']['hd']['url'] = 'http://nrodl.zdf.de' + [urlparse(u).path.replace('/ondemand/zdf/hbbtv', '') for u in xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "veryhigh"][facets/facet/text() = "hbbtv"]/url/text()').extract()][0]
    #     item['files']['hd']['size'] = xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "veryhigh"][facets/facet/text() = "hbbtv"]/filesize/text()').extract_first()
    #     item['files']['high'] = {}
    #     item['files']['high']['url'] = 'http://nrodl.zdf.de' + [urlparse(u).path.replace('/ondemand/zdf/hbbtv', '') for u in xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "hbbtv"]/url/text()').extract()][0]
    #     item['files']['high']['size'] = xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "hbbtv"]/filesize/text()').extract_first()
    #     item['files']['low'] = {}
    #     item['files']['low']['url'] = 'http://nrodl.zdf.de' + [urlparse(u).path for u in xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "progressive"]/url/text()').extract()][0]
    #     item['files']['low']['size'] = xml.xpath('formitaeten/formitaet[@basetype="h264_aac_mp4_http_na_na"][quality/text() = "high"][facets/facet/text() = "progressive"]/filesize/text()').extract_first()

    #     yield item