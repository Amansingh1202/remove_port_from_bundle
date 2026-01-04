from netmiko import ConnectHandler
from dotenv import load_dotenv
import os
import schedule
import time

load_dotenv()
host = os.getenv('EVE_HOST')
username = os.getenv('EVE_USERNAME')
password = os.getenv('EVE_PASSWORD')

connection = {
    'device_type': 'cisco_ios_telnet',
    'host': host,
    'username': username,
    'password': password,
    'port' : 32769,
    "banner_timeout": 200,
    "conn_timeout": 15,
    }
net_connect = ConnectHandler(**connection)
commands = [f"do show ip int br"]
p = net_connect.send_command("show interfaces Port-channel1 | include Member")
p_lines = p.split("\n")
p_lines = [i.split(",")[0].split(":")[1].strip() for i in p_lines]
net_connect.disconnect()

def get_individual_int_data():
    net_connect = ConnectHandler(**connection)
    for value in p_lines:
        individual_int_output = net_connect.send_command("show logging | include Interface "+value +", changed state to administratively down")
        print(individual_int_output)
    net_connect.disconnect()

schedule.every(1).minutes.do(get_individual_int_data)

while True:
    schedule.run_pending()
    time.sleep(1)
