import scrapy
import json
from mediathek_scraper.items import MediathekScraperItem

class MediathekScraperSpider(scrapy.Spider):
    name = "arte"
    start_urls = [
        "http://www.arte.tv/papi/tvguide/videos/plus7/program/D/L2/ALL/ALL/-1/AIRDATE_DESC/0/0/DE_FR.json",
        # "http://www.arte.tv/papi/tvguide/videos/plus7/program/F/L2/ALL/ALL/-1/AIRDATE_DESC/0/0/DE_FR.json"
    ]

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

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
            item['ttl'] = show['VDO']['VRU']
            item['duration'] = show['VDO']['VDU'] * 60

            url = show['VDO']['videoStreamUrl']
            yield scrapy.Request(url, callback=self.parse_files, meta={'item': item})

    def parse_files(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        item = response.meta['item']
        item['files'] = {}
        item['files']['hd'] = {}
        item['files']['hd']['url'] = [v for v in jsonresponse['video']['VSR'] if v['VFO'] == 'HBBTV' and v['VQU'] == 'SQ'][0].get('VUR', '');
        item['files']['high'] = {}
        item['files']['high']['url'] = [v for v in jsonresponse['video']['VSR'] if v['VFO'] == 'HBBTV' and v['VQU'] == 'EQ'][0].get('VUR', '');
        item['files']['low'] = {}
        item['files']['low']['url'] = [v for v in jsonresponse['video']['VSR'] if v['VFO'] == 'HBBTV' and v['VQU'] == 'HQ'][0].get('VUR', '');

        yield item
