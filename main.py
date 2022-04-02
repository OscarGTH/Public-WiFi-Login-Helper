# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
# Imports from std. lib
import socket
import logging
import time
import subprocess
# Own module imports
from check_ip import run_ip_checker
from config_parser import get_configuration

# Setting Selenium logger loglevel
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)
# Setting urllib loglevel
urllib_logger = logging.getLogger('urllib3.connectionpool')
urllib_logger.setLevel(logging.WARNING)
# Configuring own logger
logger = logging.getLogger('ip_logger.wifi_logger')


class WifiLogger:

    def __init__(self) -> None:
        self.conf = get_configuration()
        # Configuring Selenium to run in headless mode.
        options = Options()
        options.headless = True
        # Creating the webdriver.
        self.driver = webdriver.Firefox(options=options)
        

    def is_connected(self):
        ''' Checking if machine has working internet connection. '''

        try:
            # Timing out after 2 seconds
            socket.setdefaulttimeout(2)
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("1.1.1.1", 53))
            return True
        except OSError:
            pass
        return False


    def login_to_wifi(self):
        ''' Logs into Wifi using Selenium. '''

        logger.info("-Logging in to WiFi")
        try:
            # Trying to get a page which will surely prompt the Wifi login screen.
            self.driver.get(self.conf.wifi_checking_page)
            # Finding input fields.
            username_input = self.driver.find_element(By.NAME, 'user')
            password_input = self.driver.find_element(By.NAME, 'password')
            # If both input fields were found, continue
            if username_input and password_input:
                # Filling in credentials
                username_input.send_keys(self.conf.wifi_user)
                password_input.send_keys(self.conf.wifi_pass)
                # Clicking login button
                self.driver.find_element(By.NAME, 'origin').click()
                self.driver.close()
        except WebDriverException:
            logger.error("-Machine is not connected to WiFi.")


    def connect_to_wifi(self):
        ''' Connects to WiFi network. '''
        
        if self.conf.os == "Windows":
            results = subprocess.check_output(["netsh", "wlan", "show", "network"])
            results = results.decode("ascii").replace("\r","").split("\n")[4:]
            x = 0
            while x < len(results):
                # Getting every 5th element of list to capture only SSID.
                if x % 5 == 0:
                    # Splitting string to get only WiFi name and nothing else.
                    splitted_ssid = results[x].split(': ')
                    # If the ssid string was successfully split into two parts, check the name.
                    if len(splitted_ssid) > 1 and splitted_ssid[1] == self.conf.wifi_name:
                        # If the name was the one that we want to connect to, then connect to it.
                        logger.info("-Connecting to WiFi network.")
                        # Connecting to WiFi network
                        output = subprocess.check_output(["netsh", "wlan", "connect", self.conf.wifi_name])
                        # If connection was successful, return True.
                        if "successfully" in output.decode("ascii"):
                            logger.info("-Successfully connected to " + self.conf.wifi_name)
                            return True
                x += 1
            return False
        else:
            # TODO: Connect to Wifi in Debian environment.
            return False

    def run_connection_check(self):
        ''' Checks if machine has internet and connects to it, if it doesn't. '''

        logger.info("-Checking connection status.")
        if self.is_connected() == False:
            logger.info("-Machine is not connected to internet.")
            # Connecting to WiFi if machine is not already connected to it.
            if self.connect_to_wifi():
                logger.info("-Connected to WiFi.")
                time.sleep(3)
                # Logging in to wifi
                self.login_to_wifi()
                # If network is connected now.
                if self.is_connected():
                    # Checking if IP address changed and notifying by email if it has.
                    run_ip_checker()
                    logger.info("-Connection established.")
                else:
                    logger.info("-Connection was not established.")
            else:
                logger.error("-Could not connect to WiFi.")
        else:
            # Running IP checker just in case IP had changed.
            run_ip_checker()
            logger.info("-Connection to internet was already established.")
        # Closing the webdriver.
        self.driver.quit()


if __name__ == '__main__':
    # Initializing instance of Wifi logger
    wlogger = WifiLogger()
    # Running main method of checking the internet connection.
    wlogger.run_connection_check()

        