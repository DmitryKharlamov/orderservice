from rest_framework import viewsets
from .models import Tariff, UserSubscription
from .serializers import TariffSerializer, UserSubscriptionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TariffViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Только подписки текущего пользователя
        return UserSubscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
