import ipaddress
from datetime import datetime
import json

# Flask Imports
from flask_restful import Resource
class ConnectionException(Exception):
    pass

class subnetCalc(Resource):
    def __init__(self, inputs):
        print(inputs)
        self.auth = self._get_auth()
        self._instance_key = datetime.now().strftime("%m/%d/%y %H:%M:%S")
        self.info = inputs
        self.ip = inputs["Subnet"]["ip"]
        self.hosts = int(inputs["Subnet"]["hosts"])
        # self.ip = "1"
        # self.hosts = 1

    def _get_auth(self):
        # Auth to backend goes here
        pass

    def _cidr_to_subnet_mask(self, cidr_prefix):
        mask = (0xffffffff >> (32 - cidr_prefix)) << (32 - cidr_prefix)
        return str(ipaddress.IPv4Address(mask))

    def _number_of_hosts(self, cidr):
        network = ipaddress.ip_network(cidr, strict=False)
        number_of_hosts = network.num_addresses - 2
        
        return number_of_hosts

    def _find_smallest_cidr(self):
        host_bits = 0
        while (2 ** host_bits) < (self.hosts + 2):
            host_bits += 1

        cidr_prefix = 32 - host_bits
        cidr = f"{self.ip}/{cidr_prefix}"
        subnet_mask = self._cidr_to_subnet_mask(cidr_prefix)
        try:
           cidr_network = ipaddress.ip_network(cidr, strict=False)
           nID = cidr_network.network_address
           bID = cidr_network.broadcast_address
           print(nID +  1)
        except ValueError as err:
            return "Invalid"
        numHosts = self._number_of_hosts(cidr_network)
        returnDict = [{
            "cidr_network": cidr_network.with_prefixlen,
            "subnetMask": subnet_mask,
            "numberHosts": numHosts,
            "NetworkID": str(nID),
            "BroadcastID": str(bID),
            "First": str(nID + 1),
            "Last": str(bID - 1)
        }]

        return json.dumps(returnDict)


# ip_address = "192.168.1.0"
# number_of_hosts = 2000

# inputs = {
#     "ip": "192.168.1.0",
#     "hosts": "200"
# }

# test = subnetCalc(inputs)

# print(test._find_smallest_cidr())

# print(find_smallest_cidr(ip_address, number_of_hosts))
