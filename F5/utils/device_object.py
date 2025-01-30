"""Creates F5 Object"""

import logging
import requests
import urllib3
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from netmiko import (
    ConnectHandler,
    ConnectionException,
    NetMikoTimeoutException,
    NetMikoAuthenticationException,
    ReadTimeout,
    ReadException,
)

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

logger  = logging.getLogger(__package__)
load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class F5DeviceException(Exception):
    """F5 Device Exception"""
    pass

class F5Device:
    """Create object of F5 Device"""

    def __init__(self, device):
        self.device = device
        self.username, self.password = self._get_auth()
        self.connection = None
        self.is_connected = False
        self.session = self._create_session()

        # Setup Netmiko connection
        self.device_config = {
            "device_type": "f5_ltm",
            "host": self.device,
            "username": self.username,
            "password": self.password,
            "global_delay_factor": 2,
        }

        logger.info("Device %s has been initialized", self.device)

    def _get_auth(self):
        """
        Obtain Credentials to login to F5 devices
        """
        username = os.getenv("F5_User")
        password = os.getenv("F5_Password")
        return username, password

    @retry(
        retry=retry_if_exception_type((ConnectionException, NetMikoTimeoutException, NetMikoAuthenticationException)),
        stop=stop_after_attempt(3),
        wait=wait_fixed(5),
    )
    def connect_to_device(self):
        """
        Attempt to connect to the device.

        Retries if Timout or Read error.
        Raises F5DeviceException if authenitcation fails.
        """
        try:
            self.connection = ConnectHandler(**self.device_config)
            self.is_connected = True
            logger.info("Connected to device %s", self.device)
        except NetMikoAuthenticationException as auth_error:
            logger.error("Authentication failed for device %s", self.device)
            raise F5DeviceException(f"Authentication failed for device {self.device}") from auth_error
        except Exception as error:
            logger.error("Failed to connect to device %s", self.device)
            raise F5DeviceException(f"Failed to connect to device {self.device}") from error

    def is_connection_live(self):
        """Validates that the SSH session is still active"""
        if self.connection and hasattr(self.connection, "is_alive"):
            return self.connection.is_alive()
        return False

    @retry(
        retry=retry_if_exception_type((ReadTimeout, ReadException, NetMikoTimeoutException)),
        stop=stop_after_attempt(3),
        wait=wait_fixed(5),
    )
    def run_command_with_retry(self, command, **kwargs):
        """
        Try sending the command multiple times.

        timeout is set by default here, but leaving an option for 'expect_string' or other command specific needs
        """
        output = self.connection.send_command(command, **kwargs) # type: ignore[reportOptionalMember]
        return output

    def run_command(self, command, **kwargs):
        """
        Run command on the device.

        Raises F5DeviceException if the command fails.
        """
        if not self.is_connection_live():
            try:
                self.connect_to_device()
            except F5DeviceException as error:
                logger.error("Failed to run command %s on device %s", command, self.device)
                raise F5DeviceException(f"Failed to run command {command} on device {self.device}") from error
        try:
            output = self.run_command_with_retry(command, **kwargs)
            return output
        except (ReadException, ReadTimeout, NetMikoTimeoutException) as error:
            logger.error("Failed to run command %s on device %s", command, self.device)
            try:
                output = self.run_command_with_retry(command, **kwargs)
                return output
            except (ReadException, ReadTimeout, NetMikoTimeoutException) as error2:
                logger.exception("All retry methods exhausted for command %s on device %s", command, self.device)
                return "ERROR"
        except ConnectionException as connErr:
            logger.exception("Connection exception occured connecting to %s with exception %s", self.device, connErr)
            return "ERROR"
        except Exception as error:
            logger.exception("General Error, Failed to run command %s on device %s", command, self.device)
            return "ERROR"

    def close_connection(self):
        if self.connection:
            try:
                self.connection.disconnect()
            except Exception as error:
                logger.error("Failed to disconnect from device %s", self.device)
                raise F5DeviceException(f"Failed to disconnect from device {self.device}") from error

    def get_auth_token(self):
        url = f"https://{self.device}/mgmt/shared/authn/login"
        payload = {
            "username": self.username,
            "password": self.password,
            "loginProviderName": "tmos"
        }
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()  # Ensure it raises an error if unauthorized
        return response.json().get('token')

    def _create_session(self):
        session = requests.Session()
        token = self.get_auth_token()
        session.headers.update({"X-F5-Auth-Token": token["token"]})
        session.verify = False
        return session

    
    def _clean_endpoint(self, endpoint):
        if endpoint.startswith("/"):
            return endpoint
        return f"/{endpoint}"

    def get(self, endpoint):
        endpoint = self._clean_endpoint(endpoint)
        url = f"https://{self.device}{endpoint}"
        try:
            response = self.session.get(url)
            return response.json()
        except requests.RequestException as error:
            logger.error("Failed to get data from %s: %s", url, error)
            raise F5DeviceException(f"Failed to get data from {url}") from error
    
    def post(self, endpoint, data):
        endpoint = self._clean_endpoint(endpoint)
        url = f"https://{self.device}{endpoint}"
        try:
            response = self.session.post(url, json=data)
            response_data = response.json()
            if "code" not in response_data:
                response_data["code"] = 200

            return response_data
        except requests.RequestException as error:
            logger.error("Failed to post data to %s", url)
            raise F5DeviceException(f"Failed to post data to {url}") from error
    
    def put(self, endpoint, data):
        endpoint = self._clean_endpoint(endpoint)
        url = f"https://{self.device}{endpoint}"
        try:
            response = self.session.put(url, json=data)
            return response.json()
        except requests.RequestException as error:
            logger.error("Failed to put data to %s", url)
            raise F5DeviceException(f"Failed to put data to {url}") from error

    def delete(self, endpoint):
        endpoint = self._clean_endpoint(endpoint)
        url = f"https://{self.device}{endpoint}"
        try:
            response = self.session.delete(url)
            return response.json()
        except requests.RequestException as error:
            logger.error("Failed to delete data from %s", url)
            raise F5DeviceException(f"Failed to delete data from {url}") from error

    def patch(self, endpoint, data):
        endpoint = self._clean_endpoint(endpoint)
        url = f"https://{self.device}{endpoint}"
        try:
            response = self.session.patch(url, json=data)
            return response.json()
        except requests.RequestException as error:
            logger.error("Failed to patch data to %s", url)
            raise F5DeviceException(f"Failed to patch data to {url}") from error
    
    def is_as3_installed(self) -> bool:
        """
        Checks if AS3 is installed on this F5 device.
        Returns True if installed, False if not.
        """
        # The "appsvcs/info" endpoint typically returns 200 and JSON if AS3 is installed
        try:
            endpoint = "/mgmt/shared/appsvcs/info"
            response_data = self.get(endpoint)
            # If there's a 'version' or 'release' field, that's a good sign
            if "version" in response_data or "release" in response_data:
                return True
            # Otherwise, treat it as not installed
            return False
        except F5DeviceException:
            # If it 404s or something, it's likely not installed
            return False

