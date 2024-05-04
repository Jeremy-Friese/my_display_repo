'''Functions and classes dealing with ISE.'''
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
import xmltodict
import base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ISEError(Exception):
    """
    Exceptions raised for general errors.
    """

def ise_ha_state(username: str, password: str, ise_devices: list[str]) -> str | tuple | None:
    """
        Checks the HA State of ISE returning the primary device passed in.
        Can find the active in a pair and also determine state of single device.
        Args:
            username (str): ISE API Username.
            password (str): ISE API Password.
            ise_devices (list[string]): Devices passed in as a list of strings.
        Returns:
            Primary LTM in pair that was passed.
    """

    num = len(ise_devices)
    cred = f"{username}:{password}"
    cred_bytes = bytes(cred, 'utf-8')
    cred_64 = base64.b64encode(cred_bytes)
    creds = cred_64.decode()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {creds}"
    }
    for device in ise_devices:
        try:
            url = f"https://{device}:9060/ers/config/node/name/{device}"

            res = requests.get(url, headers=headers, verify=False)

            data = json.loads(res.text)
            state = data["Node"]["primaryPapNode"]
            secondary = data["Node"]["otherPapFqdn"]

            if state == True:
                if num == 1:
                    return device, secondary
                elif num == 2:
                    return device
            elif num == 1 and state == False:
                return None, None
        except json.decoder.JSONDecodeError:
            pass
    
    
def ise_active_dc(ise_username: str, ise_password: str):
    """
    Find active datacenter for ISE.
    
    Args:
        ise_username (str): ISE Username,
        ise_password (str): ISE Password,
    Returns:
        primLab, secLab, or Error
    """
    compareDict = {}
    headers = {
        "Content-Type": "application/json",
    }
    # Change device name as needed
    dcMnst = ["https://secLab01/admin/API/mnt/Session/ActiveCount",
            "https://primLab01/admin/API/mnt/Session/ActiveCount"]
    
    for link in dcMnst:
        url = link.replace("01", "02")
        panDevice, activeUsers = _ise_Connector(link, headers, ise_username, ise_password)
        if "ISE" in panDevice:
            return panDevice
        if panDevice != "Error":
            compareDict[panDevice] = int(activeUsers)
        elif panDevice == "Error":
            panDevice2, activeUsers2 = _ise_Connector(url, headers, ise_username, ise_password)
            if panDevice2 != "Error":
                compareDict[panDevice2] = int(activeUsers2)
            elif panDevice2 == "Error":
                return "Could not determine primary DC"
    
    compareDict = dict(compareDict)


    if len(compareDict) == 1:
        for device, users in compareDict.items():
            if int(users) > 10000:
                if "secLab" in device:
                    dc = "secLab"
                elif "primLab" in device:
                    dc = "primLab"
                else:
                    dc = "Could not determine primary DC"
                return dc
    elif len(compareDict) == 2:
        activeDC = max(compareDict, key=compareDict.get)  # pyright: ignore
        dc = ''
        if "secLab" in str(activeDC):
            dc = "secLab"
        elif "primLab" in str(activeDC):
            dc = "primLab"
        return dc
    
def _ise_Connector(url, headers, ise_username, ise_password):
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(ise_username, ise_password),
            headers=headers,
            verify=False
            )
        response.raise_for_status()
        try:
            res = xmltodict.parse(response.text)
            data = json.loads(json.dumps(res))
            panDevice = url.split(".")[0].strip("https://")
            activeUsers = data["sessionCount"]['count']
            return panDevice, activeUsers
        except json.decoder.JSONDecodeError as err:
            raise ISEError("Unable to decode returned JSON file") from err
    except requests.exceptions.RequestException as err:
        raise ISEError("Error connecting to device") from err