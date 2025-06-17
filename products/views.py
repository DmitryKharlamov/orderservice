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
        serializer.save(user=self.request.user)

        from accounts.models import CustomUser
        updated_user = CustomUser.objects.get(pk=self.request.user.pk)
        notify_telegram(updated_user)

