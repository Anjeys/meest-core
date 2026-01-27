from celery import shared_task
from decimal import Decimal
import time
from .models import Parcel


@shared_task
def calculate_customs_duty(parcel_id):
    print(f"[Worker] Processing parcel {parcel_id}")

    time.sleep(5)

    try:
        parcel = Parcel.objects.get(id=parcel_id)
        limit = Decimal('150.00')

        if parcel.declared_value > limit:
            parcel.status = 'CUSTOMS_PROCESSING'
            print(f"[INFO] Duty applied for {parcel.tracking_code}")
        else:
            parcel.status = 'CUSTOMS_CLEARED'
            print(f"[INFO] Cleared: {parcel.tracking_code}")

        parcel.save()

    except Parcel.DoesNotExist:
        print("[ERROR] Parcel not found")