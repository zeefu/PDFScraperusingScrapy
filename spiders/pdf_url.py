import scrapy

import re

from pdf_url.items import PdfUrlItem

from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor

class PdfUrlSpider(CrawlSpider):
	
	name = 'pdf_url'

	allowed_domains = ['adobe.com']	

	start_urls = ['https://www.adobe.com']

	rules = [Rule(LinkExtractor(allow=''), callback='http_parseresponse', follow=True)]

	def http_parseresponse(self, response):

		if response.status != 200:
			return None

		print(response.url)

		item = PdfUrlItem() 

		if b'Content-Type' in response.headers.keys():
			links_to_pdf = 'application/pdf' in str(response.headers['Content-Type'])
		else:
			return None

		content_disposition_exists = b'Content-Disposition' in response.headers.keys()
		#print(content_disposition_exists)

		if links_to_pdf:
			if content_disposition_exists: 
				item['filename'] = re.search('filename="(.+)"', str(response.headers['Content-Disposition']).group(1)
				item['url'] = response.url
			else:
			item['filename'] = response.url.split('/')[-1]
			item['url'] = response.url
		else:		
			return None
		

		return item


