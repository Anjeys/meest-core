import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Parcel
from .serializers import ParcelSerializer

# 1. Получаем логгер (имя 'international' важно, чтобы он прошел фильтры)
logger = logging.getLogger('international')


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'tracking_code'

    # 2. Перехватываем создание, чтобы записать лог
    def perform_create(self, serializer):
        instance = serializer.save()

        # 3. Пишем чистый текстовый лог (без эмодзи)
        logger.info(f"Parcel created: {instance.tracking_code}")