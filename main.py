from evengsdk.client import EvengClient
from netmiko import ConnectHandler
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv('EVE_HOST')
username = os.getenv('EVE_USERNAME')
password = os.getenv('EVE_PASSWORD')
client = EvengClient(host)
client.login(username=username, password=password)


from flask import Flask, render_template, request
app = Flask(__name__)
node = {}

@app.route("/")
def main_page():
    resp = client.api.list_nodes(
    'port-channel.unl'
    )
    k = resp['data']
    for key, value in k.items():
        node[value['name']] = value['url']
    if request.method == 'GET':
        return render_template(
        'index.html',
        node=node
    )

@app.route("/process_data", methods=['POST'])
def process_data():
    selected_node = request.form.get('node')
    port_channel_input = request.form.get('port_channel')
    selected_int = request.form.get('interface')
    port = node[selected_node].split(":")[-1]
    connection = {
    'device_type': 'cisco_ios_telnet',
    'host': host,
    'username': username,
    'password': password,
    'port' : port,
    "banner_timeout": 200,
    "conn_timeout": 15
    }
    net_connect = ConnectHandler(**connection)
    commands = [f"int {selected_int}",f"no channel-group {port_channel_input} mode active"]
    p = net_connect.send_config_set(commands)
    net_connect.disconnect()
    return f"command sent {commands} received back {p}"

    

if __name__ == '__main__':
    app.run(debug=True)