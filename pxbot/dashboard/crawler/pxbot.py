import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.proxy import Proxy, ProxyType

import os
import logging
import time

import os.path
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))


logging.basicConfig(filename="{}/logs.txt".format(PROJECT_PATH),
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(level=logging.INFO)



class Pxbot:

    def __init__(self, env='prod'):
        logging.info("===========Bot loaded==============")
        self.env = env
        _proxy = self._rotate_proxies()

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': _proxy,
            'ftpProxy' : _proxy,
            'sslProxy' : _proxy,
            'noProxy'  : ''
        })

        options = Options()
        # options.headless = True

        try:
            self.driver = webdriver.Firefox(
                executable_path="{}/dashboard/crawler/drivers/win-geckodriver.exe".format(os.path.relpath('.')), options=options, proxy=proxy)
        except OSError as ex1:
            logging.exception("Windows error")
            try:
                self.driver = webdriver.Firefox(
                    executable_path="{}/dashboard/crawler/drivers/linux-geckodriver".format(PROJECT_PATH),
                    options=options, proxy=proxy)
            except Exception as ex2:
                logging.exception(ex2)
        except Exception as ex:
            logging.exception(ex)



        logging.info("Drivers initialized")

    def _rotate_proxies(self):
        return '93.145.17.219'

    def authenticate(self, username, password):
        # TODO decrypted password

        logging.info('Logging in {} ...'.format(username))

        if self.env == 'prod':
            self.driver.get('https://office.preneurx.com/members/login')
        else:
            self.driver.get('file:///home/jessy/Documents/test_site/Site Login.html')
            return True

        txt_username = self.driver.find_element(By.ID, 'user')
        txt_password = self.driver.find_element(By.ID, 'password')
        btn_login = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/form/button')

        txt_username.send_keys(username)
        txt_password.send_keys(password)
        btn_login.click()

        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.title_is('Dashboard'))
            logging.info('Sucessfully logged in {}'.format(username))
            return True
        except Exception as ex:
            logging.exception(ex)

        logging.error('Invalid credentials')
        return False

    def init_update(self):

        logging.info('Initializing metrics ...')

        wait = WebDriverWait(self.driver, 10)
        time.sleep(10)

        if self.env == 'prod':
            self.driver.get('https://office.preneurx.com/members')
        else:
            self.driver.get('file:///home/jessy/Documents/test_site/Dashboard.html')

        def float_conv(x): return float(x.replace('$ ', ''))

        expired = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div/div[4]/div/div/div/div/div/span/strong'))
        ).get_attribute('innerHTML')

        member_id = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div/div[7]/div[1]/div/div[2]/div/table/tbody/tr[1]/td[2]/a'))
        ).get_attribute('innerHTML')

        deposit = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div/div[7]/div[3]/div/div[2]/div/table/tbody/tr[1]/td[2]/a'))
        ).get_attribute('innerHTML')

        payout = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div/div[7]/div[3]/div/div[2]/div/table/tbody/tr[2]/td[2]/a'))
        ).get_attribute('innerHTML')

        earnings = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div/div[7]/div[3]/div/div[2]/div/table/tbody/tr[3]/td[2]/a'))
        ).get_attribute('innerHTML')

        total_earned = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div/div[7]/div[3]/div/div[2]/div/table/tbody/tr[7]/td[2]'))
        ).get_attribute('innerHTML')

        expired = ' '.join([x for x in expired.split(' ')[:-2]])

        deposit = float_conv(deposit)
        payout = float_conv(payout)
        earnings = float_conv(earnings)
        total_earned = float_conv(total_earned)

        metrics = {'expired': expired,
                   'member_id': member_id,
                   'deposit': deposit,
                   'payout': payout,
                   'earnings': earnings,
                   'total_earned': total_earned
                   }
        logging.info('Done! Metrics: {}'.format(metrics))
        return metrics

    def transfer_finance(self, amount, to_wallet):

        logging.info('Transferring amount to {} ...'.format(to_wallet))

        wait = WebDriverWait(self.driver, 10)
        time.sleep(10)

        if self.env == 'prod':
            self.driver.get('https://office.preneurx.com/plugins/revshare/rmember/transfer')
        else:
            self.driver.get('file:///home/jessy/Documents/test_site/Transfer.html')

        txt_amount = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div/form/div/div/input'))
        )

        txt_amount.send_keys(str(amount))

        to_wallet_select = Select(self.driver.find_element(By.CSS_SELECTOR, 'select.form-control:nth-child(11)'))

        to_wallet_select.select_by_value(to_wallet)
        btn_transfer = self.driver.find_element(By.XPATH, '//*[@id="button"]')

        btn_transfer.click()

        logging.info('Done transferring amount')

        if self.env == 'prod':
            result = wait.until(EC.presence_of_element_located((
                By.CLASS_NAME, 'alert'))
            ).get_attribute('innerHTML')

            logging.info('PreneurX message: {}'.format(result))
        else:
            return 'successfully'

        return result.strip()

    def buy_revshares(self, from_wallet):
        logging.info('Buying revhsares ...')

        wait = WebDriverWait(self.driver, 10)
        time.sleep(10)

        if self.env == 'prod':
            self.driver.get('https://office.preneurx.com/plugins/revshare/rmember/purchase/&id=6')
        else:
            self.driver.get('file:///home/jessy/Documents/test_site/Revshares.html')

        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'select.form-control:nth-child(12)'))
        )
        wallet_select = Select(self.driver.find_element(By.CSS_SELECTOR, 'select.form-control:nth-child(12)'))
        wallet_select.select_by_value(from_wallet)

        btn_pay = self.driver.find_element(By.XPATH, '//*[@id="button"]')
        btn_pay.click()

        logging.info('Done buying revshares')
        if self.env == 'prod':
            result = wait.until(EC.presence_of_element_located((
                By.CLASS_NAME, 'alert'))
            ).get_attribute('innerHTML')

            logging.info('PreneurX message: {}'.format(result))
        else:
            return 'successfully'

        return result.strip()

    def upgrade_membership(self, from_wallet):
        logging.info('Upgrading membership ...')

        wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(10)

        if self.env == 'prod':
            self.driver.get('https://office.preneurx.com/members/upgrademembership')
        else:
            self.driver.get('file:///home/jessy/Documents/test_site/Upgrade.html')

        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'select.form-control:nth-child(8)'))
        )

        wallet_select = Select(self.driver.find_element(By.CSS_SELECTOR, 'select.form-control:nth-child(12)'))
        wallet_select.select_by_value(from_wallet)

        btn_pay = self.driver.find_element(By.XPATH, '//*[@id="button"]')
        btn_pay.click()

        logging.info('Done upgrading membership')

        if self.env == 'prod':
            result = wait.until(EC.presence_of_element_located((
                By.CLASS_NAME, 'alert'))
            ).get_attribute('innerHTML')

            logging.info('PreneurX message: {}'.format(result))
        else:
            return 'successfully'

        return result.strip()

    def end(self):
        self.driver.quit()


