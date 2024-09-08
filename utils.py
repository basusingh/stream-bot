import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from selenium_stealth import stealth

def get_chromedriver_path():
    return subprocess.check_output(["which", "chromedriver"]).decode("utf-8").strip()

def setup_driver_with_proxy(proxy):
    proxy_settings = Proxy()
    proxy_settings.proxy_type = ProxyType.MANUAL
    proxy_settings.http_proxy = proxy
    proxy_settings.ssl_proxy = proxy

    capabilities = DesiredCapabilities.CHROME.copy()
    proxy_settings.add_to_capabilities(capabilities)

    return webdriver.Chrome(desired_capabilities=capabilities)

def setup_driver_with_user_agent():
    ua = UserAgent()
    options = Options()
    options.add_argument(f"user-agent={ua.random}")
    return webdriver.Chrome(options=options)

def randomize_fingerprint(driver):
    width = random.randint(1024, 1920)
    height = random.randint(768, 1080)
    driver.set_window_size(width, height)
    
    driver.execute_script("""
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => %d
        });
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => %d
        });
    """ % (random.randint(1, 16), random.choice([2, 4, 8, 16])))

def setup_stealth_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(options=options)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def clear_session_data(driver):
    driver.delete_all_cookies()
    driver.execute_script("localStorage.clear();")

def set_geolocation(driver, latitude, longitude):
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })

def set_network_conditions(driver, latency, download_throughput, upload_throughput):
    driver.set_network_conditions(
        offline=False,
        latency=latency,
        download_throughput=download_throughput,
        upload_throughput=upload_throughput
    )

def simulate_user_actions(driver, url):
    driver.get(url)
    # Add your custom user simulation logic here
    # For example:
    # - Scroll the page
    # - Click on elements
    # - Fill forms
    # - etc.