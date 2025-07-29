import requests
import json

# Zabbix server details
ZABBIX_API_URL = "http://192.168.44.157:8443/api_jsonrpc.php"  # Correct Zabbix API URL
API_TOKEN = "904118cc0b604ff4ee76e75e14a064ba47f17f8a8aeafbb310e9c58cadc57471"  # Replace with your generated API token

# Function to create a host in Zabbix
def create_host(api_token, host_name, interface_ip, group_ids, template_ids):
    headers = {
        "Content-Type": "application/json"
    }

    # Use the API token directly in the request headers for authentication
    headers["Authorization"] = f"Bearer {api_token}"

    payload = {
       "jsonrpc": "2.0",
       "method": "host.create",
       "params": {
             "host": host_name, # Host name will be visible in Zabbix
             "port": 10051, # Zabbix server port, not web server port
             "groups":[
                {
                   "groupid": group_ids # Group ID
                }
             ],
             "templates":[
                {
                   "templateid": template_ids # Template ID
                }
             ],
            "interfaces": [
                {
                    "type": 2,  # Type 1 is agent interface, 2 is SNMP interface
                    "main": 1, # 1 indicates it's the main interface
                    "useip": 1, # 1 to use IP address, 0 for DNS
                    "ip": interface_ip,  # IP of the host (ensure this IP is accessible via SNMP)
                    "dns": "", # Since adding IP, so DNS is empty
                    "port": "161",  # Default SNMP port
                    "details": {
                        "version": "2",  # SNMP version (can be 1, 2, or 3 depending on your configuration)
                        "bulk": 1, # Enable bulk requests for SNMPv2c/v3
                        "community": "Letmeview"  # SNMP community string
                    }
                }
            ]
          },
       "id": 1 # user_id
       }

    try:
        # Send the POST request to the Zabbix API
        response = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
        print(response.content)

        if response.status_code != 200:
            print(f"Error: Received HTTP status code {response.status_code}")
            print(f"Response content: {response.text}")
            return None

        results = response.json()

        if "result" in results:
            print(f"Host created successfully: {results['result']}")
            return results["result"]
        else:
            print(f"Error creating host: {results.get('error', {}).get('data')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {str(e)}")
        return None


if __name__ == "__main__":
    # Define your host parameters
    host_name = "Test Host" # Host name will be visible in Zabbix, must be unique
    interface_ip = "10.253.118.92"  # IP of the new host
    group_ids = 5  # Group ID for "Discovered hosts"
    template_ids = 10218  # Template ID for "Cisco IOS by SNMP"

    # Use the API token for authentication and create the host
    result = create_host(API_TOKEN, host_name, interface_ip, group_ids, template_ids)

    if result:
        print(f"Host creation result: {result}")
    else:
        print("Failed to create the host.")
