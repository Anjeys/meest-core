from django.db import models


class Parcel(models.Model):
    # Трек-номер (Индекс для поиска)
    tracking_code = models.CharField(max_length=30, unique=True, db_index=True)

    sender_name = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=2, default='UA')

    # --- ИСПРАВЛЕНО: ДОБАВЛЕНЫ ФИНАНСОВЫЕ ПОЛЯ ---
    # Вес (до 999.999 кг)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=3)
    # Объявленная стоимость (до 99,999,999.99) - НУЖНО ДЛЯ ТАМОЖНИ
    declared_value = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Статусы
    status = models.CharField(max_length=20, default='CREATED', db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'meest_parcels'
        ordering = ['-created_at']

    def __str__(self):
        return self.tracking_code