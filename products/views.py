from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from .telegram_notify import notify_telegram

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        notify_telegram(self.request.user)
