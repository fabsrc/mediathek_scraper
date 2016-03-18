import scrapy
import urllib2
import re
from mediathek_scraper.items import MediathekScraperItem

class MediathekScraperSpider(scrapy.Spider):
    name = "mediathek"
    start_urls = [
        "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz0?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz1?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz2?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz3?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz4?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz5?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz6?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz7?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz8?flash=off",
        # "http://www.zdf.de/ZDFmediathek/hauptnavigation/sendung-a-bis-z/saz9?flash=off"
    ]

    def parse(self, response):
        for href in response.css("div.beitragListe li > .image > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_show)

    def parse_show(self, response):
        for href in response.css("div.beitragListe li > .image > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)

        next_page = response.css('a.weitereBeitraege::attr("href")')
        if next_page:
          url = response.urljoin(next_page[0].extract())
          yield scrapy.Request(url, callback=self.parse)

    def parse_item(self, response):
        id = response.xpath('//div[@class="beitrag"]/div[@id="playerContainer"]/@class').extract()[0]
        item = MediathekScraperItem()
        item['title'] = response.xpath('//h1[@class="beitragHeadline"]/text()').extract()[0]
        item['show'] = response.xpath('//div[@class="beitrag"]/p[@class="datum"]/text()').extract()[0].split(', ')[0]
        item['date'] = response.xpath('//div[@class="beitrag"]/p[@class="datum"]/text()').extract()[0].split(', ')[1]
        item['type'] = response.xpath('//div[@class="beitrag"]/p[@class="datum"]/text()').extract()[1].split(', ')[0]
        item['duration'] = response.xpath('//div[@class="beitrag"]/p[@class="datum"]/text()').extract()[1].split(', ')[1]
        item['desc'] = response.xpath('//div[@class="beitrag"]/p[@class="kurztext"]/text()').extract()[0]
        item['files'] = response.xpath('//div[@class="beitrag"]/ul[@class="dslChoice"]//a[@class="play"]/@href').extract()
        yield item

    # def getUrl(self, url):
    #     req = urllib2.Request(url)
    #     req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
    #     response = urllib2.urlopen(req)
    #     link = response.read()
    #     response.close()
    #     return link

    # def get_urls(self, id):
    #     content = self.getUrl("http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?id=" + id)
    #     match = {}
    #     match[0] = re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">.+?<quality>hd</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    #     match[1] = re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">.+?<quality>veryhigh</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    #     match[2] = re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">.+?<quality>high</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    #     match[3] = re.compile('<formitaet basetype="h264_aac_ts_http_m3u8_http" isDownload="false">.+?<quality>high</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    #     match["UT"] = re.compile('<caption>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    #     return match