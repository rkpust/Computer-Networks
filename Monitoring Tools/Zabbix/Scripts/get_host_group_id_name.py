import requests
import json

# Zabbix server details
ZABBIX_API_URL = "http://192.168.44.157:8443/api_jsonrpc.php"  # Correct Zabbix API URL
API_TOKEN = "904118cc0b604ff4ee76e75e14a064ba47f17f8a8aeafbb310e9c58cadc57471"  # Replace with your generated API token

# Function to get all host groups in Zabbix
def get_groups(api_token):
    headers = {
        "Content-Type": "application/json"
    }

    # Use the API token directly in the request headers for authentication
    headers["Authorization"] = f"Bearer {api_token}"

    payload = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {},
        "id": 1 # user_id
    }

    try:
        # Send the POST request to the Zabbix API
        response = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
        print(response.content, '\n')

        if response.status_code != 200:
            print(f"Error: Received HTTP status code {response.status_code}")
            print(f"Response content: {response.text}")
            return None

        results = response.json()

        if "result" in results:
            groups = results["result"]
            for group in groups:
                print(f"Group ID: {group['groupid']}, Group Name: {group['name']}")
            
            print('\n')

            return groups
        else:
            print(f"Error retrieving groups: {results.get('error', {}).get('data')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {str(e)}")
        return None


if __name__ == "__main__":
    # Get all available host groups
    groups = get_groups(API_TOKEN)

    if groups:
        print(f"Available Groups: {groups}")
    else:
        print("Failed to retrieve host groups.")
