# Scrapy Elite Proxies

Scrapy Elite Proxies (http://elite.proxies.online) middleware
http://rev.proxies.online

Grab new proxy from your Elite Proxies account.

**settings.py**
```
ELITE_PROXIES_API_KEY = "YOUR_API_KEY_FROM_MASHAPE"
ELITE_PROXIES_RENEW_INTERVAL = 20 # renew proxy every x requests
ELITE_PROXIES_COUNTRY = "BR" # remove for untarget proxy

DOWNLOADER_MIDDLEWARES = {
	'projectname.eliteproxies.EliteProxies': 100
}
```
