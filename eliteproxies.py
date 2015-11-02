# Copyright (C) 2015 by Elite Proxies (proxies.online) <support@proxies.online>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import json
from scrapy import log

try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2

class EliteProxies(object):
	def __init__(self, settings, crawler):
		self.crawler = crawler
		self.api_key = settings.get('ELITE_PROXIES_API_KEY')
		self.renew_interval = int(settings.get('ELITE_PROXIES_RENEW_INTERVAL'))
		self.current_interval = 0
		self.country = settings.get('ELITE_PROXIES_TARGET_COUNTRY')
		self.proxy_host=None
		self.proxy_port=None
		#self.getProxy()

	def getProxy(self):
		log.msg("get new proxy from Elite Proxies")
		self.current_interval=0
		url = "https://garrylachman-elite-proxies-v1.p.mashape.com/create/http/{0}".format(self.country is None and "untarget" or "traget")
		if self.country:
			url += "/" + self.country

		req = Request(url)
		req.add_header('X-Mashape-Key', self.api_key)
		res = urlopen(req).read()
		
		log.msg(res);
		jsonresponse = json.loads(res)
		if 'error' not in jsonresponse:
			self.proxy_host = jsonresponse['proxy'];
			self.proxy_port = jsonresponse['port'];
		else:
			time.sleep(60)
			self.getProxy()			

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings, crawler)

	def process_request(self, request, spider):
		if 'proxy' in request.meta:
			return

		if self.current_interval >= self.renew_interval or self.proxy_host is None:
			self.getProxy()
		
		self.current_interval += 1
		request.meta['proxy'] = "http://{0}:{1}".format(self.proxy_host, str(self.proxy_port))

	def process_exception(self, request, exception, spider):
        	log.msg('request fail')
		self.getProxy()
