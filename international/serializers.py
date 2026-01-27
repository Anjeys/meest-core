from rest_framework import serializers
from .models import Parcel
from .tasks import calculate_customs_duty

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']

    def create(self, validated_data):
        parcel = super().create(validated_data)
        calculate_customs_duty.delay(parcel.id)
        return parcel