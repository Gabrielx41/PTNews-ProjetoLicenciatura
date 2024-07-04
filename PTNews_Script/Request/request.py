import requests
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0 "}

def request(url):
    global headers
    return requests.get(url, headers=headers, timeout = 50)