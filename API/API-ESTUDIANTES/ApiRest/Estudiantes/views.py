from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Estudiante
from .serializers import EstudianteSerializer

class EstudianteListCreateView(APIView):
    def get(self, request):
        estudiantes = Estudiante.objects.all()
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EstudianteDetailView(APIView):
    def get_object(self, pk):
        try:
            return Estudiante.objects.get(pk=pk)
        except Estudiante.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        estudiante = self.get_object(pk)
        serializer = EstudianteSerializer(estudiante)
        return Response(serializer.data)

    def put(self, request, pk):
        estudiante = self.get_object(pk)
        serializer = EstudianteSerializer(estudiante, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        estudiante = self.get_object(pk)
        estudiante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EstudianteSearchView(APIView):
    def get(self, request):
        query_param = request.query_params.get('q')
        estudiantes = Estudiante.objects.filter(Nombre__icontains=query_param) if query_param else Estudiante.objects.all()
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)
