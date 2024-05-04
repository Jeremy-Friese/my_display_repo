# Standard Imports
import re
import logging
from socket import gethostname


# Azure Imports
import azure.core.exceptions
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import (
    PublicIPAddress,
    LoadBalancingRule,
    TransportProtocol,
    SubResource,
    FrontendIPConfiguration,
    SubResource,
)

class AZConnectionError(Exception):
    pass

class AZBuilder():
    def __init__(self, inputs):
        # Setup Logging
        # Will only log locally.  SPLUNK and other report logging is from custom imports.
        logging.basicConfig(filename="./logs.txt", level=logging.DEBUG)
        self._logger = logging.getLogger()

        # Setting credentials
        creds = self._get_cred()
        client_secret = creds[0]
        tenant_id = creds[1]
        client_id = creds[2]
        subscription_id = creds[3]

        # Define variables
        self.url = inputs["url"]
        self.rule_name = self.url.replace("-", "_").replace(".", "_")
        self.ip_address = inputs["ip_address"]
        self.server = inputs["server"]

        # These can be changed as needed, passed in from the front end, or retrieved from a vault.
        self.subscription_id = subscription_id
        self.backend_loadbalancer = "Set Variable here"
        self.resource_group_name = "Set Variable here"
        self.gateway_lb = "Set Variable here"
        self.load_balancer_name = "Set Variable here"
        

        # Define ID variables
        # Create Global Load Balancer ID to be added to wrapper.
        self.gwlb_id = f'/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Network/loadBalancers/{self.gateway_lb}/frontendIPConfigurations/FrontendGWLBIp'

        # Create frontend ip config id to be added to wrapper.
        self.frontend_ip_configuration_id = f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Network/loadBalancers/{self.load_balancer_name}/frontendIPConfigurations/{self.url}"

        # Create a variable with the ip information to be added to wrapper.
        self.ip_address_id = f'/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Network/publicIPAddresses/{self.ip_address}'

        
        self. credential = ClientSecretCredential(
                        tenant_id = tenant_id,
                        client_id = client_id,
                        client_secret = client_secret,
                    )

        # Setting how to connect and interact with Azure.
        self.network_client = NetworkManagementClient(self.credential, self.subscription_id)

    def _get_cred(self):
        # Get credentials from here.  Depending on password vault used
        # on how and what to retrieve.
        azureCreds = ["client_secret", "tenant_id", "client_id", "subscription_id"]
        return azureCreds
    
    def buildLB(self):
        try:
            # Get load balancer information.
            load_balancer = self.network_client.load_balancers.get(self.resource_group_name, self.load_balancer_name)

            # Use Azure wrapper to create FrontendIPConfiguration item.
            new_frontend_ip_config = FrontendIPConfiguration(
                name=self.url,
                public_ip_address=PublicIPAddress(id=self.ip_address_id),
                gateway_load_balancer=SubResource(id=self.gwlb_id),
                )

            # Make sure that the frontend configs exist.
            if load_balancer.frontend_ip_configurations is None:
                load_balancer.frontend_ip_configurations = []

            # Append the information to the configuration list.
            load_balancer.frontend_ip_configurations.append(new_frontend_ip_config)

            # Update the LB with the new config info recieved from the frontend.
            updated_load_balancer = self.network_client.load_balancers.begin_create_or_update(
                self.resource_group_name,
                self.load_balancer_name,
                parameters=load_balancer
                )

            # Wait for the update to finish.
            updated_load_balancer.wait()
            self._logger.info({
                    "message": f"ALB {self.url} successfully created with IP {self.ip_address}"
                    })
            # Return status of frontend build.
            return updated_load_balancer.status()

        except azure.core.exceptions.HttpResponseError as err:
            # raise error and logging goes here.
            if "has two child resources with the same name" in str(err): 
                self._logger.critical({
                    "exception": str(err),
                    "message": f"Duplicate name for ALB {self.url}"
                    })
                raise AZConnectionError(
                    {
                        "message": f"duplicate name (url) {self.url}",
                        "exception": str(err)
                    }
                    )
            elif "is referenced by multiple ipconfigs in resource" in str(err):
                self._logger.critical({
                    "exception": str(err),
                    "message": f"IP address {self.ip_address} already assigned"
                    })
                raise AZConnectionError( 
                    {
                        "message": f"IP {self.ip_address} already assigned",
                        "exception": str(err)
                    }
                    )
            else:
                self._logger.critical({
                    "exception": str(err),
                    "message": f"Error occured creating ALB"
                    })
                raise AZConnectionError(
                    {
                        "message": "Error occurred creating ALB.",
                        "exception": str(err)
                    }
                )


    def addRule(self):
        try:
            # Get load balancer information.
            load_balancer = self.network_client.load_balancers.get(self.resource_group_name, self.load_balancer_name)

            # Create new rule.  Can be added statically or passed in from the frontend.
            new_load_balancing_rule = LoadBalancingRule(
            name=self.rule_name,
            protocol=TransportProtocol.tcp, # type: ignore
            frontend_port=443,
            backend_port=443,
            enable_floating_ip=True,
            idle_timeout_in_minutes=4,
            load_distribution="Default",
            disable_outbound_snat=True,
            frontend_ip_configuration=SubResource(id=self.frontend_ip_configuration_id),
            backend_address_pool={
                "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Network/loadBalancers/{self.load_balancer_name}/backendAddressPools/{self.backend_loadbalancer}" # type: ignore
            },
            probe={
                "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Network/loadBalancers/{self.load_balancer_name}/probes/http_probe" # type: ignore
            }
            )

            # Validate if load balancing rules exist.
            if load_balancer.load_balancing_rules is None:
                load_balancer.load_balancing_rules = []
            
            # Append new rule.
            load_balancer.load_balancing_rules.append(new_load_balancing_rule)

            # Update the Load Balancer with the new configuration
            updated_load_balancer = self.network_client.load_balancers.begin_create_or_update(
                    self.resource_group_name,
                    self.load_balancer_name,
                    parameters=load_balancer
                    )

            # Wait for the update operation to complete
            updated_load_balancer.wait()

            self._logger.info({
                    "message": f"Rules created and assigned to {self.url}"
                    })
            # Return status of adding rule to front end build.
            return updated_load_balancer.status()

        except azure.core.exceptions.HttpResponseError as err:
            if "has two child resources with the same name" in str(err):
                self._logger.critical({
                    "exception": str(err),
                    "message": f"Duplicate rule name for ALB {self.rule_name}"
                    }) 
                raise AZConnectionError(
                    {
                        "message": f"duplicate rule name {self.rule_name}",
                        "exception": str(err)
                    }
                    )
            elif "is referenced by multiple ipconfigs in resource" in str(err):
                self._logger.critical({
                    "exception": str(err),
                    "message": f"IP {self.ip_address} already assigned"
                    })
                raise AZConnectionError( 
                    {
                        "message": f"IP {self.ip_address} already assigned",
                        "exception": str(err)
                    }
                    )
            else:
                self._logger.critical({
                    "exception": str(err),
                    "message": f"Error occurred creating and assigning rule for {self.url}."
                    })
                raise AZConnectionError(
                    {
                        "message": f"Error occurred creating and assigning rule for {self.url}.",
                        "exception": str(err)
                    }
                )


    def validateBuild(self):
        failList = []
        load_balancer = self.network_client.load_balancers.get(self.resource_group_name, self.load_balancer_name)

        # Check for rules.
        if [rule for rule in load_balancer.load_balancing_rules if rule.name == self.rule_name]: # type: ignore
            pass
        else:
            failList.append("LB Rule")

        # Check for frontend configs.
        if [fic for fic in load_balancer.frontend_ip_configurations if fic.name == self.url]: # type: ignore
            pass
        else:
            failList.append("front end configs")
        
        # Check for the gateway load balancer config.
        if [gw for gw in load_balancer.frontend_ip_configurations if gw.gateway_load_balancer.id == self.gwlb_id]: # type: ignore
            # All frontend configs share the same gateway load balancer so check if the name is in the url.
            if [fic for fic in load_balancer.frontend_ip_configurations if fic.name == self.url]: # type: ignore
                pass
            else:
                failList.append("gateway loadbalancer")

        # Check if the ip address has been configured.
        if [ip for ip in load_balancer.frontend_ip_configurations if ip.public_ip_address.id == self.ip_address_id]: # type: ignore
            pass
        else:
            failList.append("ip config")

        # Return successful if all checks are passed
        # Return the failed list if any checks are failed.
        if len(failList) == 0:
            return "Succeeded"
        else:
            return failList


    def nextAvailable(self):
        # Function to find missing integers in list
        def missingIPs(ipList):
            start, end = ipList[0], ipList[-1]
            return sorted(set(range(start, end + 1)).difference(ipList))
        
        # Find environment script is running in.
        host = gethostname()
        if "prod" in host:
            env = "prd"
        else:
            env = "nonprd"
        ipList, failList = [], []
        try:
            # Get a list of all resources of for defined region
            load_balancer = self.network_client.load_balancers.list(self.resource_group_name)
            for item in load_balancer:
                if item.frontend_ip_configurations is None:
                    self._logger.critical({
                    "message": f"ALB returned empty list for frontend_ip_configurations on {self.load_balancer_name}"
                    })
                    raise AZConnectionError(
                        {
                            "message": "ALB returned empty list for frontend_ip_configurations",
                        }
                    )
                for fip in item.frontend_ip_configurations:
                    if fip.public_ip_address != None:
                        # Get IP address from the id.
                        ipAddress = str(fip.public_ip_address.id).split("/")[-1]
                        # Ignore the id that have letters instead of IP addresses.
                        if re.search('[a-zA-Z]', ipAddress):
                            pass
                        else:
                            ipList.append(ipAddress)
                            failList.append(int(ipAddress.split(".")[-1]))


            # If Dev Environment allow to pick highest available IP from Azure and redefine the vip IP 
            # For testing.
            if self.ip_address in ipList:
                # Dev EUS2 build.
                if host == "dev01" or host == "dev02" and "10.10" in self.server:
                    last_octet = max(missingIPs(sorted(failList)))
                    nextIP = "192.168.55." + str(last_octet)
                    return [True, nextIP]
                # Dev EU build.
                elif host == "dev01" or host == "dev" and "10.11" in self.server:
                    last_octet = max(missingIPs(sorted(failList)))
                    nextIP = "172.16.112." + str(last_octet)
                    return [True, nextIP]
                # Dev US Cent build.ab
                elif host == "dev01" or host == "dev" and "10.15" in self.server:
                    last_octet = max(missingIPs(sorted(failList)))
                    nextIP = "172.16.220." + str(last_octet)
                    return [True, nextIP]
                else:
                    return [True]
            else:
                return [False]
        
        except azure.core.exceptions.HttpResponseError as err:
            self._logger.critical({
                    "exception": str(err),
                    "message": f"Error connecting to ALB to determine available IPs in {self.resource_group_name}"
                    })
            raise AZConnectionError(
                {
                    "message": f"Error connecting to ALB to determine available IPs in {self.resource_group_name}",
                    "exception": str(err)
                }
            )
        
        
    def deleteLB(self):
        # Cannot delete a frontend ip configuration if there is only one configured on the load balancer.
        # Not required to delete associated rule assigned in order to delete the frontend config.
        try:
            load_balancer = self.network_client.load_balancers.get(self.resource_group_name, self.load_balancer_name)

            # Validate if load balancing rules exist and are not None.
            if load_balancer.load_balancing_rules is None:
                load_balancer.load_balancing_rules = []

            if load_balancer.frontend_ip_configurations is None:
                load_balancer.frontend_ip_configurations = []
            

            # remove the frontend config from the list.
            load_balancer.load_balancing_rules[:] = [rule for rule in load_balancer.load_balancing_rules if rule.name != self.rule_name]

            # remove the rule from the list.
            load_balancer.frontend_ip_configurations[:] = [fic for fic in load_balancer.frontend_ip_configurations if fic.name != self.url]
            

            update_result = self.network_client.load_balancers.begin_create_or_update(
                resource_group_name=self.resource_group_name,
                load_balancer_name=self.load_balancer_name,
                parameters=load_balancer
                )

            update_result.result()
            # Return status of deleting frontend build.
            return update_result.status()

        except azure.core.exceptions.HttpResponseError as err:
            self._logger.critical({
                    "exception": str(err),
                    "message": f"Only one frontend IP configuration on device.  ALB must have at least one configured."
                    })
            if "does not have Frontend IP Configuration, but it has other child resources." in str(err):
                raise AZConnectionError(
                    {
                        "message": "Only one frontend IP configuration on device.  ALB must have at least one configured.",
                        "exception": str(err)
                    }
                )
            else:
                self._logger.critical({
                    "exception": str(err),
                    "message": f"Error deleting ALB, rule, and backend load balancer for {self.url}, {self.ip_address}"
                    })
                raise AZConnectionError(
                    {
                        "message": "Error deleting configured frontend IP configuration.",
                        "exception": str(err)
                    }
                )
 