from django.http import JsonResponse

class SubscriptionRequiredMiddleware:
    """
    Middleware ограничивает доступ к эндпоинтам заказов и тарифов,
    если у пользователя нет активной подписки.
    Все остальные пути пропускаются.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Middleware работает только на этих путях
        protected_paths = [
            '/api/orders/',
            '/api/tariffs/',
        ]

        if any(path.startswith(p) for p in protected_paths):
            if not request.user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required.'}, status=401)

            # Проверка наличия подписки
            user = request.user
            if not user.subscriptions.exists():
                return JsonResponse({'detail': 'Нет активной подписки.'}, status=403)

        return self.get_response(request)
