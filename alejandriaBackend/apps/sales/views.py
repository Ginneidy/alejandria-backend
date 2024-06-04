from rest_framework import viewsets
from .models import Sale, Purchase
from .serializers import SaleSerializer, PurchaseSerializer

class SaleViewSet(viewsets.ModelViewSet):
    
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    
    
class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer