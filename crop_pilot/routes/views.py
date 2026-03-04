from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.views import APIView
from rest_framework.response import Response
from .genetic_algorithm import optimize_route
from .models import Machine 

import os
from django.conf import settings
from .route_visualizer import generate_route_map

@method_decorator(csrf_exempt, name='dispatch')
class RouteOptimizationAPI(APIView):
    def post(self, request):
        try:
            machine_id = request.data.get('machine_id')
            points = request.data.get('points', [])
            
            if not points or len(points) < 2:
                return Response({"error": "Insira pelo menos 2 pontos"}, status=400)
                
            machine = Machine.objects.get(id=machine_id)
            
            best_route = optimize_route(
                points=points,
                machine_capacity=machine.capacity_kg,
                machine_id=machine_id
            )

            map_filename = f"route_machine_{machine_id}.html"
            map_path = os.path.join(settings.MEDIA_ROOT, 'maps', map_filename)
            
            os.makedirs(os.path.dirname(map_path), exist_ok=True)
            
            generate_route_map(points, best_route["optimized_route"], output_file=map_path)
            
            map_url = request.build_absolute_uri(f"{settings.MEDIA_URL}maps/{map_filename}")
            
            return Response({
                "optimized_route": best_route["optimized_route"],
                "total_distance": best_route["total_distance"],
                "map_url": map_url,
                "message": "Rota otimizada com sucesso!"
            })
            
        except Machine.DoesNotExist:
            return Response({"error": "Máquina não encontrada"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)