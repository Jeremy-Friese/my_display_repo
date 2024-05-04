'''Functions and classes dealing with Palo Alto.'''

import base64
import requests
import xml.etree.ElementTree as ET

from typing import Iterable


class PanHAStateUnknown(Exception):
    ...


def pan_ha_state(
    username: str,
    password: str,
    pan_endpoints: Iterable[str] = ('10.10.10.1', '10.10.10.2')
):
    '''Check the state of the Panorama instances, returning the IP address of the current
    active instance. If the active instance cannot be determined raises PanHAStateUnknown exception.

    Args:
        username (str): Panorama API username.
        password (str): Panorama API password.

    Returns:
        str: IP address of active Panorama instance.

    Raises:
        PanHAStateUnknown: If active instance cannot be determined. '''

    key = base64.b64encode(
        f'{username}:{password}'
        .encode('utf-8')
    ).decode('utf-8')

    for endpoint in pan_endpoints:
        try:
            r = requests.get(
                f'https://{endpoint}'
                + '/api?type=op&cmd=<show><high-availability>'
                + '<state></state></high-availability></show>',
                headers={
                    'Authorization': f'Basic {key}'
                },
                verify=False,
            )

            r.raise_for_status()

        except (
                requests.HTTPError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.InvalidURL
        ):
            continue

        contents = ET.fromstring(r.content)

        state = contents.find('./result/local-info/state')
        if state is not None and state.text in ('primary-active', 'secondary-active'):
            return endpoint

    raise PanHAStateUnknown(f'Unable to determine Panorama HA state for {pan_endpoints}')
