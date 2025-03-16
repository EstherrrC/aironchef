import requests
import yaml

def auth(
    api_key: str,
    base_url: str,
) -> None:
    """
    Confirms the auth token is valid

    Inputs:
        - api_key (string): your api key
        - base_url (string): the endpoint of the AnythingLLM local server
    """
    auth_url = base_url + "/auth"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }
    auth_response = requests.get(
        auth_url,
        headers=headers
    )

    if auth_response.status_code == 200:
        print("Successful authentication")
    else:
        print("Authentication failed")

    print(auth_response.json())

if __name__ == "__main__":
    # load config from yaml
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # get the api_key and base_url from the config file
    api_key = config["api_key"]
    base_url = config["model_server_base_url"]

    # call the auth function
    auth(api_key, base_url)