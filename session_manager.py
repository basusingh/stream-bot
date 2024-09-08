import random
import logging
from utils import *
from proxy_manager import FreeProxy

logging.basicConfig(filename='session.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SessionManager:
    def __init__(self, private_urls, public_urls):
        self.private_urls = private_urls
        self.public_urls = public_urls
        self.proxy_manager = FreeProxy()
        self.proxy_list = self.proxy_manager.get_proxy_list()
        logging.info(f"Initialized with {len(self.proxy_list)} valid proxies")

    def create_session(self):
        technique = random.choice(["proxy", "user_agent", "fingerprint", "stealth", "geolocation", "network"])
        logging.info(f"Creating session with {technique} technique")

        if technique == "proxy":
            if not self.proxy_list:
                logging.warning("No valid proxies available. Refreshing proxy list.")
                self.proxy_list = self.proxy_manager.get_proxy_list()
            if self.proxy_list:
                proxy = random.choice(self.proxy_list)
                driver = setup_driver_with_proxy(proxy)
            else:
                logging.error("Failed to get valid proxies. Falling back to user_agent technique.")
                driver = setup_driver_with_user_agent()
        elif technique == "user_agent":
            driver = setup_driver_with_user_agent()
        elif technique == "fingerprint":
            driver = webdriver.Chrome(service=Service(get_chromedriver_path()))
            randomize_fingerprint(driver)
        elif technique == "stealth":
            driver = setup_stealth_driver()
        elif technique == "geolocation":
            driver = webdriver.Chrome(service=Service(get_chromedriver_path()))
            set_geolocation(driver, random.uniform(-90, 90), random.uniform(-180, 180))
        elif technique == "network":
            driver = webdriver.Chrome(service=Service(get_chromedriver_path()))
            set_network_conditions(driver, random.randint(50, 200), random.randint(500, 2000) * 1024, random.randint(500, 2000) * 1024)

        clear_session_data(driver)
        return driver

    def run_session(self, num_streams):
        for _ in range(num_streams):
            private_url = random.choice(self.private_urls)
            public_url = random.choice(self.public_urls)

            driver = self.create_session()
            
            try:
                logging.info(f"Accessing private URL: {private_url}")
                simulate_user_actions(driver, private_url)
                
                logging.info(f"Accessing public URL: {public_url}")
                simulate_user_actions(driver, public_url)
            except Exception as e:
                logging.error(f"Error during session: {str(e)}")
            finally:
                driver.quit()

        logging.info(f"Completed {num_streams} streams")