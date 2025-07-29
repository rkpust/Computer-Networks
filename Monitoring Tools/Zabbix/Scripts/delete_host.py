import requests
import json

# Zabbix server details
ZABBIX_API_URL = "http://192.168.44.157:8443/api_jsonrpc.php"  # Correct Zabbix API URL
API_TOKEN = "904118cc0b604ff4ee76e75e14a064ba47f17f8a8aeafbb310e9c58cadc57471"  # Replace with your generated API token

# Function to create a host in Zabbix
def delete_host(api_token, host_ids):
    headers = {
        "Content-Type": "application/json"
    }

    # Use the API token directly in the request headers for authentication
    headers["Authorization"] = f"Bearer {api_token}"

    payload = { 
        "jsonrpc":"2.0",
        "method":"host.delete",
        "params":[
            host_ids
            ],
        "id":1
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
            print(f"Host deleted successfully: {results['result']}")
            return results["result"]
        else:
            print(f"Error deleting host: {results.get('error', {}).get('data')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {str(e)}")
        return None


if __name__ == "__main__":
    # Host ID which you want to delete
    host_ids = "10677"

    # Use the API token for authentication and delete the host
    result = delete_host(API_TOKEN, host_ids)

    if result:
        print(f"Host deletion result: {result}")
    else:
        print("Failed to delete the host.")
