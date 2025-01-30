from django.http import JsonResponse
from .subnet_calculator import SubnetCalculator
import json

def subnet_calculator(request):
    if request.method == 'POST':
        query_type = request.GET.get('type')
        print(query_type)
        try:
            
            # Parse input JSON
            data = json.loads(request.body)
            ip_address = data.get('ip_address')
            subnet_mask = data.get('subnet_mask')
            cidr = data.get('cidr')
            required_hosts = data.get('required_hosts')
            checkIP = data.get("ip_check") or None

            # Validate input
            if not ip_address:
                return JsonResponse({"error": "IP address is required"}, status=400)

            # Initialize the calculator
            subnet_calc = SubnetCalculator(
                    ip_address=ip_address,
                    subnet_mask=subnet_mask, # pyright: ignore
                    cidr=cidr, # pyright: ignore
                    required_hosts=required_hosts # pyright: ignore
                )
            vis = subnet_calc.visualize_subnet()
            result = subnet_calc.to_dict()
            if query_type:
                check = subnet_calc.is_ip_in_subnet(checkIP)  # pyright: ignore
                return JsonResponse({'ip_in_subnet': check})
            return JsonResponse({
                'result': result,
                'visualization': vis
            })
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)