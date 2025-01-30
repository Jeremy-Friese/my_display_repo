import json
import asyncio
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.device_object import F5Device, F5DeviceException


class BuildF5ConfigurationView(APIView):
    """API to build F5 configurations using the REST API (Non-AS3)"""

    def sanitize_name(self, name):
        """Replace spaces with underscores and strip invalid characters."""
        name = name.replace(" ", "_")  # Replace spaces with underscores
        return "".join(c for c in name if c.isalnum() or c in ["_", "-", ":", "."])  # Allow only valid characters

    def sanitize_config(self, config):
        """Sanitize configuration names by replacing spaces with underscores."""
        if config:
            for virtual_server in config.get("virtual_server", []):
                virtual_server["name"] = self.sanitize_name(virtual_server["name"])
            for pool in config.get("pool", []):
                pool["name"] = self.sanitize_name(pool["name"])
                for member in pool.get("members", []):
                    member["name"] = self.sanitize_name(member["name"])
            for monitor in config.get("monitors", []):
                monitor["name"] = self.sanitize_name(monitor["name"])
            for node in config.get("nodes", []):
                node["name"] = self.sanitize_name(node["name"])
        return config

    async def async_task(self, device, config):
        """Perform the non-AS3 build process and send updates."""
        channel_layer = get_channel_layer()

        try:
            # Step 1: Create Nodes
            for node in config.get("nodes", []):
                node_name = self.sanitize_name(node["name"])
                response = device.post("/mgmt/tm/ltm/node", {
                    "name": node_name,
                    "address": node["address"]
                })
                message = self.handle_response(
                    response,
                    f"Node {node_name} added",
                    f"Node {node_name} could not be added"
                )
                await channel_layer.group_send("device_status", message)

            # Step 2: Create Monitors
            for monitor in config.get("monitors", []):
                monitor_name = self.sanitize_name(monitor["name"])
                response = device.post("/mgmt/tm/ltm/monitor/http", {
                    "name": monitor_name,
                    "send": monitor["send"],
                    "recv": monitor["recv"]
                })
                message = self.handle_response(
                    response,
                    f"Monitor {monitor_name} added",
                    f"Monitor {monitor_name} could not be added"
                )
                await channel_layer.group_send("device_status", message)

            # Step 3: Create Pools and Add Members
            for pool in config.get("pool", []):
                backend_port = pool.get("backend_port", 80)
                monitor_name = "http" if backend_port == 80 else "https" if backend_port == 443 else None

                # Validate monitor_name
                if not monitor_name:
                    raise F5DeviceException("Monitor name is missing for pool creation.")

                # Sanitize pool name
                pool_name = self.sanitize_name(pool["name"])

                # Check if pool exists
                existing_pool = device.get(f"/mgmt/tm/ltm/pool/{pool_name}")
                if existing_pool.get("code") == 200:
                    await channel_layer.group_send(
                        "device_status",
                        {"type": "send_status_update", "data": {"message": f"Pool {pool_name} already exists", "response": existing_pool}}
                    )
                else:
                    # Create pool if it doesn't exist
                    response = device.post("/mgmt/tm/ltm/pool", {"name": pool_name, "monitor": f"/Common/{monitor_name}"})
                    message = self.handle_response(
                        response,
                        f"Pool {pool_name} created",
                        f"Pool {pool_name} could not be created"
                    )
                    await channel_layer.group_send("device_status", message)

                # Add members to pool
                for member in pool.get("members", []):
                    # Ensure valid port and sanitize member name
                    port = member.get("port", backend_port)
                    if port == 0:
                        port = 80  # Default to port 80 if no valid port is specified
                    member_base_name = member["name"].split(":")[0] 
                    member_name = self.sanitize_name(f"{member_base_name}:{port}")

                    response = device.post(f"/mgmt/tm/ltm/pool/{pool_name}/members", {
                        "name": member_name,
                        "address": member["address"]
                    })
                    message = self.handle_response(
                        response,
                        f"Member {member_name} added to {pool_name}",
                        f"Member {member_name} could not be added to {pool_name}"
                    )
                    await channel_layer.group_send("device_status", message)

            # Step 4: Create Virtual Servers
            for vs in config.get("virtual_server", []):
                # Sanitize virtual server name
                vs_name = self.sanitize_name(vs["name"])
                response = device.post("/mgmt/tm/ltm/virtual", {
                    "name": vs_name,
                    "destination": vs["destination"],
                    "pool": f"/Common/{self.sanitize_name(vs['pool'])}",
                    "profiles": vs["profiles"],
                    "sourceAddressTranslation": vs["sourceAddressTranslation"]
                })
                message = self.handle_response(
                    response,
                    f"Virtual Server {vs_name} created",
                    f"Virtual Server {vs_name} could not be created"
                )
                await channel_layer.group_send("device_status", message)

            # Notify Completion
            await channel_layer.group_send(
                "device_status",
                {"type": "send_status_update", "data": {"message": "LTM Build Completed!", "status": "success"}}
            )

        except F5DeviceException as e:
            await channel_layer.group_send(
                "device_status",
                {"type": "send_status_update", "data": {"message": f"Error: {str(e)}", "status": "error"}}
            )

    def handle_response(self, response, success_msg, error_msg):
        """Handle the API response and return the appropriate message."""
        if response.get("code") in (200, 201):
            return {"type": "send_status_update", "data": {"message": success_msg, "response": response}}
        return {"type": "send_status_update", "data": {"message": error_msg, "response": response}}

    def post(self, request):
        device_ip = request.data.get("device_ip")
        config = request.data.get("config")

        if not device_ip or not config:
            return Response({"error": "Missing device IP or configuration data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create F5Device instance
            device = F5Device(device_ip)

            # Check if AS3 is installed
            as3_installed = device.is_as3_installed()
            if as3_installed:
                return Response({"message": "AS3 build path selected. Not yet implemented."}, status=status.HTTP_501_NOT_IMPLEMENTED)

            # Sanitize configuration data
            config = self.sanitize_config(config)

            # Run the non-AS3 build asynchronously
            async_to_sync(self.async_task)(device, config)

            return Response({"message": "Non-AS3 build started", "device_ip": device_ip}, status=status.HTTP_202_ACCEPTED)

        except F5DeviceException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
