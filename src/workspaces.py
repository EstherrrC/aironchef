import requests
import yaml
from prettyprinter import pprint

def workspaces(
    api_key: str,
    base_url: str
) -> None:
    """
    Prints formatted json info about the available workspaces. Used
    to identify the correct workspace slug for the chat api call.

    Inputs:
        - api_key (string): your api key
        - base_url (string): the endpoint of the AnythingLLM local server
    """
    workspaces_url = base_url + "/workspaces"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    workspaces_response = requests.get(
        workspaces_url,
        headers=headers
    )

    if workspaces_response.status_code == 200:
        print("Successful authentication")
    else:
        print("Authentication failed")

    pprint(workspaces_response.json())

if __name__ == "__main__":
    # load config from yaml
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # get the api_key and base_url from the config file
    api_key = config["api_key"]
    base_url = config["model_server_base_url"]

    # call the workspaces function
    workspaces(api_key, base_url)