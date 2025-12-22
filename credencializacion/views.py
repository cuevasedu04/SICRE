from rest_framework import viewsets
from .models import Enrolamiento
from .serializers import EnrolamientoSerializer

class EnrolamientoViewSet(viewsets.ModelViewSet):
    queryset = Enrolamiento.objects.all().order_by('-fecha_registro')
    serializer_class = EnrolamientoSerializer