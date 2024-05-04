'''Functions and classes dealing with F5.'''
import requests
from requests.auth import HTTPBasicAuth
from benedict import benedict
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def f5_ha_state(username: str, password: str, ltms: list[str]) -> str | tuple | None:
    """
    Checks the HA State of F5 returning the primary device passed in.  If only one device is passed in
    then it must be passed in as a list.
    Args:
        username (str): F5 API Username.
        password (str): F5 API Password.
        ltms (list[string]): LTMs passed in as a list of strings.
    Returns:
        If a pair of LTMs is passed in it will return the Primary LTM in the pair, and returns None
        if unable to determine primary.
        If only one device is passed in then will return primary and seconary device,
        in that order regardless if device passed in is secondary.  
        If error connecting and determining primary will return "None, None".
        The call should reflect recieving two variables for a single LTM passed in.
    Example:
        One LTM Passed in:
        primaryDevice, secondaryDevice = f5_ha_state(username, password, [ltmDevice])

        Two LTM Passed in:
        activeDevice = f5_ha_state(username, password, [ltmDevice1, ltmDevice2])
    """
    headers = {
        "Content-Type": "application/json",
    }

    for ltm in ltms:
        try:
            url = f"https://{ltm}/mgmt/tm/cm/failover-status"
            r = requests.get(
                url,
                auth=HTTPBasicAuth(username, password),
                headers=headers,
                verify=False
            )

            data = benedict(r.text, format='json')
            desc_keypath = (
                'entries.https://localhost/mgmt/tm/cm/failover-status/0'
                + '.nestedStats.entries.status.description'
            )

            state = data[desc_keypath]
            if len(ltms)  == 2:
                if str(state).lower() == "active":
                    return ltm
            elif len(ltms) == 1:
                if str(state).lower() == "active":
                    try:
                        secondary_device = (
                                'entries.https://localhost/mgmt/tm/cm/failover-status/1'
                                + '.nestedStats.entries.remoteDeviceName.description'
                            )
                        return ltm, data[secondary_device]
                    except Exception as err:
                        return ltm, None
                elif str(state).lower() == "standby":
                    try:
                        primary_device = (
                                'entries.https://localhost/mgmt/tm/cm/failover-status/1'
                                + '.nestedStats.entries.remoteDeviceName.description'
                            )
                        return data[primary_device], ltm
                    except Exception as err:
                        return None, ltm
        except Exception:
            if len(ltms) == 1:
                    return None, None
            else:
                return None
