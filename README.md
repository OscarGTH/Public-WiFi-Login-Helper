# Public-WiFi-Login-Helper
This program is meant to automate logging in to public/open WiFi networks which force the user to log in using their own network portal.

The need for this program arose from the restriction of only having access to an open WiFi network which prompted the machine to log in through the WiFi provider's portal every now and then. There was a need to connect a Raspberry Pi to the Wifi and inform the machine owner of its assigned IP address. The program is meant to be run every day to check if internet connection is still available/if the network requires another log in, which happens every couple of days. This way the Raspberry Pi will always be connected to the network and its owner gets to know if the assigned external IP address changes, so SSH connection can be established without the need of wired connection to the machine.

The project utilizes Selenium headless to log in to the WiFi and smtplib to email me about changes of the IP address.
Geckodriver has to be in the project folder for this to work.


# How to install
1. Clone repository
2. Run command "npm install -r requirements.txt"
3. Fill out necessary info to "mail_conf.ini.dist" and rename/copy it to "mail_conf.ini".
4. Rename "ip_data.json.dist" into "ip_data.json"
5. Run "python main.py -c mail_conf.ini"

# TODO:
- Writing Debian specific code for listing available WiFi networks and connecting to them.
- Allowing the ip_data.json file to not exist before running the program for the first time.
