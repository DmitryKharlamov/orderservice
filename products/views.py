from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from .telegram_notify import notify_telegram

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только заказы текущего пользователя
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

        notify_telegram(user)
