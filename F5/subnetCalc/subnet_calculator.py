from typing import Dict, List, Union


class SubnetCalculator:
    """
    A comprehensive subnet calculator that can perform various subnetting calculations.
    """

    def __init__(
        self,
        ip_address: Union[str, List[int]],
        subnet_mask: Union[str, List[int]] = None, # pyright: ignore
        cidr: int = None, # pyright: ignore
        required_hosts: int = None, # pyright: ignore
    ):
        """
        Initialize the SubnetCalculator with an IP address, subnet mask, CIDR notation,
        and optionally the number of required hosts.

        :param ip_address: IP address as a string or list of integers
        :param subnet_mask: Subnet mask as a string or list of integers
        :param cidr: CIDR notation as an integer
        :param required_hosts: Number of required hosts (optional)
        """        
        
        # Validate and store IP address
        self.ip_address = self._parse_ip_address(ip_address)
        self._validate_ip_address(self.ip_address)
        # Process subnet mask and CIDR
        if subnet_mask is not None:
            self.subnet_mask = self._parse_ip_address(subnet_mask)
            self._validate_subnet_mask(self.subnet_mask)
            self.cidr = self._subnet_mask_to_cidr(self.subnet_mask)
        elif cidr is not None:
            self.cidr = cidr
            self._validate_cidr(self.cidr)
            self.subnet_mask = self._cidr_to_subnet_mask(self.cidr)
        elif required_hosts is not None:
            self.cidr = self._calculate_cidr_from_hosts(required_hosts)
            self.subnet_mask = self._cidr_to_subnet_mask(self.cidr)
        else:
            raise ValueError(
                "Either subnet mask, CIDR notation, or required hosts must be provided."
            )
        self.required_hosts = required_hosts
        self._calculate_network_properties()

    def _parse_ip_address(self, ip: Union[str, List[int]]) -> List[int]:
        """
        Parses the IP address or subnet mask and returns it as a list of integers.

        :param ip: IP address as a string or list of integers
        :return: IP address as a list of integers
        """
        if isinstance(ip, str):
            octets = ip.strip().split(".")
            if len(octets) != 4:
                raise ValueError("IP address must have exactly 4 octets.")
            return [int(octet) for octet in octets]
        elif isinstance(ip, list):
            if len(ip) != 4:
                raise ValueError("IP address must have exactly 4 octets.")
            return ip
        else:
            raise TypeError("IP address must be a string or a list of integers.")

    def _validate_ip_address(self, ip: List[int]) -> None:
        """
        Validates the IP address.

        :param ip: IP address as a list of integers
        """
        for octet in ip:
            if not 0 <= octet <= 255:
                raise ValueError(f"Invalid IP address octet: {octet}")

    def _validate_subnet_mask(self, mask: List[int]) -> None:
        """
        Validates the subnet mask.

        :param mask: Subnet mask as a list of integers
        """
        mask_bin = "".join([format(octet, "08b") for octet in mask])
        if "01" in mask_bin:
            raise ValueError(
                "Invalid subnet mask. Must have contiguous ones followed by zeros."
            )

    def _validate_cidr(self, cidr: int) -> None:
        """
        Validates the CIDR notation.

        :param cidr: CIDR notation as an integer
        """
        if not 0 <= cidr <= 32:
            raise ValueError("CIDR notation must be between 0 and 32.")

    def _subnet_mask_to_cidr(self, mask: List[int]) -> int:
        """
        Converts a subnet mask to CIDR notation.

        :param mask: Subnet mask as a list of integers
        :return: CIDR notation as an integer
        """
        mask_bin = "".join([format(octet, "08b") for octet in mask])
        return mask_bin.count("1")

    def _cidr_to_subnet_mask(self, cidr: int) -> List[int]:
        """
        Converts CIDR notation to a subnet mask.

        :param cidr: CIDR notation as an integer
        :return: Subnet mask as a list of integers
        """
        mask_bin = "1" * cidr + "0" * (32 - cidr)
        return [int(mask_bin[i : i + 8], 2) for i in range(0, 32, 8)]

    def _calculate_cidr_from_hosts(self, hosts: int) -> int:
        """
        Calculates the smallest CIDR notation that can accommodate the required number of hosts.

        :param hosts: Number of required hosts
        :return: CIDR notation as an integer
        """
        if hosts <= 0:
            raise ValueError("Number of required hosts must be positive.")
        for cidr in range(32, -1, -1):
            total_hosts = 2 ** (32 - cidr)
            usable_hosts = total_hosts - 2 if cidr < 31 else total_hosts
            if usable_hosts >= hosts:
                return cidr
        raise ValueError("Cannot accommodate the required number of hosts with IPv4.")

    def _calculate_network_properties(self) -> None:
        """
        Calculates network properties such as network address, broadcast address,
        first and last usable IPs, total hosts, and usable hosts.
        """
        ip_int = self._ip_to_int(self.ip_address)
        mask_int = self._ip_to_int(self.subnet_mask)
        network_int = ip_int & mask_int
        broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)

        self.network_address = self._int_to_ip(network_int)
        self.broadcast_address = self._int_to_ip(broadcast_int)

        if self.cidr <= 30:
            self.first_usable_ip = self._int_to_ip(network_int + 1)
            self.last_usable_ip = self._int_to_ip(broadcast_int - 1)
        else:
            self.first_usable_ip = self.network_address
            self.last_usable_ip = self.broadcast_address

        self.total_hosts = 2 ** (32 - self.cidr)
        if self.cidr <= 30:
            self.usable_hosts = self.total_hosts - 2
        elif self.cidr == 31:
            self.usable_hosts = 2
        else:
            self.usable_hosts = 1

    @staticmethod
    def _ip_to_int(ip: List[int]) -> int:
        """
        Converts an IP address to a 32-bit integer.

        :param ip: IP address as a list of integers
        :return: IP address as a 32-bit integer
        """
        return (ip[0] << 24) + (ip[1] << 16) + (ip[2] << 8) + ip[3]

    @staticmethod
    def _int_to_ip(ip_int: int) -> List[int]:
        """
        Converts a 32-bit integer to an IP address.

        :param ip_int: IP address as a 32-bit integer
        :return: IP address as a list of integers
        """
        return [
            (ip_int >> 24) & 0xFF,
            (ip_int >> 16) & 0xFF,
            (ip_int >> 8) & 0xFF,
            ip_int & 0xFF,
        ]

    def display_info(self) -> None:
        """
        Displays all calculated subnet information.
        """
        print(f"IP Address        : {'.'.join(map(str, self.ip_address))}")
        print(
            f"Subnet Mask       : {'.'.join(map(str, self.subnet_mask))} (/ {self.cidr})"
        )
        print(f"Network Address   : {'.'.join(map(str, self.network_address))}")
        print(f"Broadcast Address : {'.'.join(map(str, self.broadcast_address))}")
        print(f"First Usable IP   : {'.'.join(map(str, self.first_usable_ip))}")
        print(f"Last Usable IP    : {'.'.join(map(str, self.last_usable_ip))}")
        print(f"Total Hosts       : {self.total_hosts}")
        print(f"Usable Hosts      : {self.usable_hosts}")
        print(
            f"IP Address Range  : {'.'.join(map(str, self.first_usable_ip))} - "
            f"{'.'.join(map(str, self.last_usable_ip))}"
        )
        print(f"Subnet Class      : {self.get_subnet_class()}")

    def __str__(self) -> str:
        """
        Returns a string representation of the subnet information.
        """
        info = [
            f"IP Address        : {'.'.join(map(str, self.ip_address))}",
            f"Subnet Mask       : {'.'.join(map(str, self.subnet_mask))} (/ {self.cidr})",
            f"Network Address   : {'.'.join(map(str, self.network_address))}",
            f"Broadcast Address : {'.'.join(map(str, self.broadcast_address))}",
            f"First Usable IP   : {'.'.join(map(str, self.first_usable_ip))}",
            f"Last Usable IP    : {'.'.join(map(str, self.last_usable_ip))}",
            f"Total Hosts       : {self.total_hosts}",
            f"Usable Hosts      : {self.usable_hosts}",
            f"IP Address Range  : {'.'.join(map(str, self.first_usable_ip))} - "
            f"{'.'.join(map(str, self.last_usable_ip))}",
            f"Subnet Class      : {self.get_subnet_class()}",
        ]
        return "\n".join(info)

    def is_ip_in_subnet(self, ip_address: Union[str, List[int]]) -> bool:
        """
        Checks if a given IP address belongs to the calculated subnet.

        :param ip_address: IP address as a string or list of integers
        :return: True if the IP address is in the subnet, False otherwise
        """
        ip_int = self._ip_to_int(self._parse_ip_address(ip_address))
        network_int = self._ip_to_int(self.network_address)
        broadcast_int = self._ip_to_int(self.broadcast_address)
        return network_int <= ip_int <= broadcast_int

    def suggest_subnet_mask(self, required_hosts: int) -> (List[int], int):  # pyright: ignore
        """
        Suggests a subnet mask and CIDR notation based on the number of required hosts.

        :param required_hosts: Number of required hosts
        :return: Tuple of subnet mask as list of integers and CIDR notation
        """
        cidr = self._calculate_cidr_from_hosts(required_hosts)
        subnet_mask = self._cidr_to_subnet_mask(cidr)
        return subnet_mask, cidr

    def get_subnet_class(self) -> str:
        """
        Determines the class of the subnet.

        :return: Subnet class as a string ('A', 'B', 'C', 'D', or 'E')
        """
        first_octet = self.ip_address[0]
        if 1 <= first_octet <= 126:
            return "A"
        elif 128 <= first_octet <= 191:
            return "B"
        elif 192 <= first_octet <= 223:
            return "C"
        elif 224 <= first_octet <= 239:
            return "D"
        elif 240 <= first_octet <= 254:
            return "E"
        else:
            return "Unknown"

    @staticmethod
    def generate_subnets(
        ip_range_start: str, ip_range_end: str, cidr: int
    ) -> List["SubnetCalculator"]:
        """
        Generates a list of all subnets within a given IP range.

        :param ip_range_start: Starting IP address of the range
        :param ip_range_end: Ending IP address of the range
        :param cidr: CIDR notation for the subnets
        :return: List of SubnetCalculator instances representing the subnets
        """
        subnets = []
        start_int = SubnetCalculator._ip_str_to_int(ip_range_start)
        end_int = SubnetCalculator._ip_str_to_int(ip_range_end)
        subnet_size = 2 ** (32 - cidr)
        current_int = start_int

        while current_int <= end_int:
            ip_address = SubnetCalculator._int_to_ip_str(current_int)
            subnet = SubnetCalculator(ip_address=ip_address, cidr=cidr)
            subnets.append(subnet)
            current_int += subnet_size
        return subnets

    @staticmethod
    def _ip_str_to_int(ip_str: str) -> int:
        octets = [int(octet) for octet in ip_str.strip().split(".")]
        return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]

    @staticmethod
    def _int_to_ip_str(ip_int: int) -> str:
        return ".".join(
            map(
                str,
                [
                    (ip_int >> 24) & 0xFF,
                    (ip_int >> 16) & 0xFF,
                    (ip_int >> 8) & 0xFF,
                    ip_int & 0xFF,
                ],
            )
        )

    @staticmethod
    def summarize_subnets(subnets: List["SubnetCalculator"]) -> "SubnetCalculator":
        """
        Performs supernetting/summarization of multiple subnets.

        :param subnets: List of SubnetCalculator instances
        :return: A SubnetCalculator instance representing the summarized network
        """
        network_ints = [
            SubnetCalculator._ip_to_int(subnet.network_address) for subnet in subnets
        ]
        min_network = min(network_ints)
        max_network = max(network_ints)
        xor = min_network ^ max_network
        cidr = 32 - xor.bit_length()
        subnet_mask = SubnetCalculator._cidr_to_subnet_mask_static(cidr)
        ip_address = SubnetCalculator._int_to_ip_static(min_network)
        return SubnetCalculator(ip_address=ip_address, cidr=cidr)

    @staticmethod
    def _cidr_to_subnet_mask_static(cidr: int) -> List[int]:
        mask_bin = "1" * cidr + "0" * (32 - cidr)
        return [int(mask_bin[i : i + 8], 2) for i in range(0, 32, 8)]

    @staticmethod
    def _int_to_ip_static(ip_int: int) -> List[int]:
        return [
            (ip_int >> 24) & 0xFF,
            (ip_int >> 16) & 0xFF,
            (ip_int >> 8) & 0xFF,
            ip_int & 0xFF,
        ]

    def visualize_subnet(self) -> Dict:
        """
        Generates an ASCII visual representation of the subnet.
        """
        ip_bin = self._ip_to_bin(self.ip_address)
        mask_bin = self._ip_to_bin(self.subnet_mask)
        network_bin = self._ip_to_bin(self.network_address)
        broadcast_bin = self._ip_to_bin(self.broadcast_address)


        return  {
            "ip_bin": ip_bin,
            "mask_bin": mask_bin,
            "network_bin": network_bin,
            "broadcast_bin": broadcast_bin
            }
        

    def _ip_to_bin(self, ip: List[int]) -> str:
        """
        Converts an IP address to a 32-bit binary string.

        :param ip: IP address as a list of integers
        :return: IP address as a 32-bit binary string
        """
        return ".".join([format(octet, "08b") for octet in ip])

    def to_dict(self) -> dict:
        """
        Returns all calculated subnet information as a dictionary.
        """
        return {
            'ip_address': '.'.join(map(str, self.ip_address)),
            'subnet_mask': '.'.join(map(str, self.subnet_mask)),
            'cidr': self.cidr,
            'network_address': '.'.join(map(str, self.network_address)),
            'broadcast_address': '.'.join(map(str, self.broadcast_address)),
            'first_usable_ip': '.'.join(map(str, self.first_usable_ip)),
            'last_usable_ip': '.'.join(map(str, self.last_usable_ip)),
            'total_hosts': self.total_hosts,
            'usable_hosts': self.usable_hosts,
            'ip_address_range': f"{'.'.join(map(str, self.first_usable_ip))} - {'.'.join(map(str, self.last_usable_ip))}",
            'subnet_class': self.get_subnet_class(),
        }

