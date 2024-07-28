import os

import time
import json
from lxml import html
import logging
from urllib.parse import urljoin, urlencode, urlparse, urlunparse, parse_qsl
import httpx
import ssl
import urllib.parse

logger = logging.getLogger(__name__)

headers = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Referer': 'https://www.coop.ch/de/',
    'Sec-Ch-Device-Memory': '8',
    'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Arch': '"arm"',
    'Sec-Ch-Ua-Full-Version-List': '"Google Chrome";v="123.0.6312.107", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.107"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Model': '""',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

ssl_ctx = ssl.SSLContext()
ssl_ctx.set_alpn_protocols(["h2", "http/1.1"])
ssl_ctx.set_ecdh_curve("prime256v1")
ssl_ctx.set_ciphers(
    "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:"
    "TLS_AES_128_GCM_SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:"
    "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:"
    "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:"
    "DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:"
    "ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:"
    "ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:"
    "DHE-RSA-AES256-SHA256:ECDHE-ECDSA-AES128-SHA256:"
    "ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA256:"
    "ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:"
    "DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:"
    "ECDHE-RSA-AES128-SHA:DHE-RSA-AES128-SHA:"
    "RSA-PSK-AES256-GCM-SHA384:DHE-PSK-AES256-GCM-SHA384:"
    "RSA-PSK-CHACHA20-POLY1305:DHE-PSK-CHACHA20-POLY1305:"
    "ECDHE-PSK-CHACHA20-POLY1305:AES256-GCM-SHA384:"
    "PSK-AES256-GCM-SHA384:PSK-CHACHA20-POLY1305:"
    "RSA-PSK-AES128-GCM-SHA256:DHE-PSK-AES128-GCM-SHA256:"
    "AES128-GCM-SHA256:PSK-AES128-GCM-SHA256:AES256-SHA256:"
    "AES128-SHA256:ECDHE-PSK-AES256-CBC-SHA384:"
    "ECDHE-PSK-AES256-CBC-SHA:SRP-RSA-AES-256-CBC-SHA:"
    "SRP-AES-256-CBC-SHA:RSA-PSK-AES256-CBC-SHA384:"
    "DHE-PSK-AES256-CBC-SHA384:RSA-PSK-AES256-CBC-SHA:"
    "DHE-PSK-AES256-CBC-SHA:AES256-SHA:PSK-AES256-CBC-SHA384:"
    "PSK-AES256-CBC-SHA:ECDHE-PSK-AES128-CBC-SHA256:ECDHE-PSK-AES128-CBC-SHA:"
    "SRP-RSA-AES-128-CBC-SHA:SRP-AES-128-CBC-SHA:RSA-PSK-AES128-CBC-SHA256:"
    "DHE-PSK-AES128-CBC-SHA256:RSA-PSK-AES128-CBC-SHA:"
    "DHE-PSK-AES128-CBC-SHA:AES128-SHA:PSK-AES128-CBC-SHA256:PSK-AES128-CBC-SHA")
dir_path = os.path.dirname(os.path.realpath(__file__))
proxies = {
    "http://": "http://rockywei2010.gmail.com:hy2jn8@gate2.proxyfuel.com:2000",
    "https://": "http://rockywei2010.gmail.com:hy2jn8@gate2.proxyfuel.com:2000",
}
proxy_str = "rockywei2010.gmail.com:hy2jn8@gate2.proxyfuel.com:2000"

try:
    with open(dir_path+"/cookies_datadome.json", 'r') as json_file:
        cookie_value = json.load(json_file)
    cookies = {'datadome': cookie_value}
except:
    cookies = {}



class Offers:
    def __init__(self):
        self.my_captcha_key = "9b6f94de703aaed9158398eda570ee66"
        self.req_client = httpx.Client(verify=ssl_ctx,headers=headers, cookies=cookies,follow_redirects=True)

    def get_subdomain(self,main_url):
        try:
            response = self.req_client.get(main_url)
            url = 'https://www.coop.ch'
            webpage_content = response.content
            print(response.status_code)
            if response.status_code == 403:
                dd = response.text.split('dd=')[1]
                dd = dd.split('</script')[0]
                dd = json.loads(dd.replace("'", '"'))
                cid = response.headers.get('Set-Cookie').split('datadome=')[1]
                cid = cid.split(';')[0]
                captcha_url = (
                    f"https://geo.captcha-delivery.com/captcha/?"
                    f"initialCid={dd['cid']}&hash={dd['hsh']}&"
                    f"cid={cid}&t={dd['t']}&referer={urllib.parse.quote_plus(main_url)}&"
                    f"s={dd['s']}&e={dd['e']}"
                )
                data = {
                    "key": self.my_captcha_key,
                    "method": "datadome",
                    "captcha_url": captcha_url,
                    "pageurl": url,
                    "json": 1,
                    "proxy": proxy_str,
                    "proxytype": "http",
                    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                }
                responsex = httpx.post("https://2captcha.com/in.php?", data=data)
                print(responsex)
                s = responsex.json()["request"]  # Getting the request ID
                while True:
                    solu = httpx.get(f"https://2captcha.com/res.php?key={self.my_captcha_key}&action=get&json=1&id={s}").json()
                    if solu["request"] == "CAPCHA_NOT_READY":
                        time.sleep(5)
                    elif "ERROR" in solu["request"]:
                        print(f"Error in solving puzzle ",solu["request"])
                        exit(0)
                    else:
                        break
                cookie_value = solu["request"].split(";")[0].split("=")[1]
                with open(dir_path+"/cookies_datadome.json", 'w') as json_file:
                    json.dump(cookie_value, json_file)
                try:
                    with open(dir_path+"/cookies_datadome.json", 'r') as json_file:
                        cookie_value = json.load(json_file)
                    cookies = {'datadome': cookie_value}
                    response = self.req_client.get(main_url,cookies=cookies)
                    url = 'https://www.coop.ch'
                    webpage_content = response.content
                except Exception as e:
                    print(f"Error in solving puzzle {e}")
                    pass
            # Parse the webpage content
            tree = html.fromstring(webpage_content)

            # XPath to get all links
            xpath_links = "//a[@class='cmsList__itemLink']"

            # Get all the <a> elements that match the XPath
            links = tree.xpath(xpath_links)

            urls = []
            for link in links:
                # Check if the <span> inside <a> has text not equal to 'Alle Produkte'
                span_text = link.xpath("span[@class='cmsList__itemText']/text()")
                if span_text and span_text[0].strip() != "Alle Produkte":
                    href = link.get("href")
                    if href:
                        # Join with the base URL if the link is relative
                        full_url = urljoin(url, href)

                        # Parse the URL and append query parameters
                        url_parts = list(urlparse(full_url))
                        query = dict(parse_qsl(url_parts[4]))
                        query.update({"q": ":relevance", "sort": "relevance", "pageSize": "500"})
                        url_parts[4] = urlencode(query)
                        final_url = urlunparse(url_parts)
                        urls.append(final_url)
            return urls
        except Exception as e:
            print(f"Error in getting sub domains {e}")
            pass


    def offers_page(self):
        offers_pages = []

        urls = [
            "https://www.coop.ch/de/aktionen/wochenaktionen/c/m_1011",
             "https://www.coop.ch/de/",
              "https://www.coop.ch/de/tttt/c/m_9769/",
             "https://www.coop.ch/de/weine/meine-weine/c/m_5432",
             "https://www.coop.ch/de/haushalt-tier/c/m_0277",
             "https://www.coop.ch/de/kosmetik-gesundheit/c/m_0333",
             "https://www.coop.ch/de/weine/alle-weine/c/m_2508",
             "https://www.coop.ch/de/aktionen/digitale-bons/c/m_9300",
             "https://www.coop.ch/de/lebensmittel/spezielle-ernaehrung/c/Specific_Diets",
             "https://www.coop.ch/de/weine/c/m_0222",
             "https://www.coop.ch/de/lebensmittel/c/supermarket",
             "https://www.coop.ch/de/haushalt-tier/c/m_0277",
             "https://www.coop.ch/de/kosmetik-gesundheit/c/m_0333",
             "https://www.coop.ch/de/baby-kind/c/m_0368",
             "https://www.coop.ch/de/marken-inspiration/c/m_0927",
             "https://www.coop.ch/de/baby-kind/windeln/aktionen-windeln/c/m_5120?page=1&pageSize=60&q=%3Arelevance&sort=relevance",
             "https://www.coop.ch/de/lebensmittel/getraenke/bier/c/m_0260?q=%3Arelevance%3AspecialOfferFacet%3Atrue&sort=relevance&pageSize=60",
             "https://www.coop.ch/de/marken-inspiration/saisonale-promotionen/rund-ums-grillieren/poulet/c/m_9971"
        ]

        for url in urls:
            sub_domains = self.get_subdomain(url)

        urls.extend(sub_domains)

        for url in urls:
            # print(f"len of sub domians {sub_domains}")
            offers_pages.extend(self.get_offers_page(url))
        return offers_pages

    def get_offers_page(self, url):
        print(url)
        all_offers = []
        res = self.req_client.get(url)
        xpath = "//div[@data-pagecontent-json-url]"
        var = "data-pagecontent-json-url"

        # Define the list of parts of URL
        parts_of_url = [
            "m_1011",
            "m_9769",
            "m_5432",
            "m_9300",
            "m_2508",
            "m_0222",
            "m_0277",
            "m_0333",
            "m_0368",
            "m_0927",
            "supermarket",
            "Specific_Diets",
        ]

        # Check if the URL contains '/c/' and none of the parts_of_url
        if "/c/" in url and not any(part in url for part in parts_of_url):

            xpath = "//meta[@data-pagecontent-json]"
            var = "data-pagecontent-json"

        try:
            content = html.fromstring(res.content).xpath(xpath)

            for offer in content:
                val = offer.get(var)
                if "/c/" in url and not any(part in url for part in parts_of_url):
                    # print(f"c in url")
                    all_offers.append(val)
                else:
                    all_offers.append(f"https://www.coop.ch{val}")
        except Exception as e:
            print(f"Error in for loop {e}")
            pass

        # print(f"xpath {xpath}")
        # print(f"all_offers {all_offers}")
        return all_offers

    def get_one_page_offers(self, page):
        # print(f'page {page.keys()}')
        if page.startswith('{"anchors":'):
            data = json.loads(page)
            return data["anchors"]

        else:
            headers = {"Host": "www.coop.ch"}
            try:
                res = self.req_client.get(page).json()
                return res["contentJsons"]["anchors"]
            except:
                return []

    def combine_offers(self, offers):
        all_offers = []
        for offer in offers:
            if type(offer) is str:
                offer = json.loads(offer).get("anchors")[0]
            try:
                for element in offer["json"].get("elements", []):
                    url = element.get("href")
                    if "/p/" in url:
                        all_offers.append(offer)
                    else:
                        url = f"http://www.coop.ch{url}"
                        time.sleep(1)
                        all_offers.extend(
                            self.combine_offers(self.get_offers_page(url))
                        )
            except Exception as e:
                pass
        return all_offers

    def get_all_offers(self):
        try:
            # Collect all offers from all pages in one list comprehension
            all_offers = [
                offer
                for page in self.offers_page()
                for offer in self.combine_offers(self.get_one_page_offers(page))
            ]
            #print(f"len {len(all_offers)}")
            return all_offers
        except Exception as e:
            logger.error(f"Error in get_all_offers: {e}")
            return None



if __name__ == "__main__":
    o = Offers()
    offers = o.get_all_offers()
    print(offers)
    print(len(offers))
