import subprocess
import platform
from django.http import JsonResponse
from .models import F5DeviceModel

def ping_device(ip_address):
    """
    Pings a device to check if it's reachable.
    Returns "Success" if the device is reachable, otherwise "Unreachable".
    """
    # Determine the appropriate ping command based on the OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip_address]

    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2, check=True)
        return "Success"
    except subprocess.CalledProcessError:
        return "Unreachable"
    except Exception as e:
        return f"Error: {str(e)}"

def get_device_list(request):
    """
    API to get the list of F5 devices, with real-time ping status.
    """
    devices = F5DeviceModel.objects.all()
    data = [
        {
            "name": device.name,
            "ip_address": device.ip_address,
            "status": ping_device(device.ip_address)
        }
        for device in devices
    ]
    return JsonResponse({"devices": data})
