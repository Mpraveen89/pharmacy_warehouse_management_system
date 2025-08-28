from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Address(models.Model):
    name = models.CharField(max_length=200, help_text="Party/Branch name")
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

class Location(models.Model):
    name = models.CharField(max_length=100, help_text="Warehouse name")
    code = models.CharField(max_length=20, unique=True)
    aisle = models.CharField(max_length=20, blank=True)
    shelf = models.CharField(max_length=20, blank=True)
    bin = models.CharField(max_length=20, blank=True)

    def __str__(self):
        parts = [self.name, self.aisle, self.shelf, self.bin]
        return " / ".join([p for p in parts if p])

DOSAGE_FORMS = [
    ("tablet","Tablet"),
    ("capsule","Capsule"),
    ("syrup","Syrup"),
    ("injection","Injection"),
    ("insulin","Insulin"),
    ("ointment","Ointment"),
    ("other","Other"),
]

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="General")
    dosage_form = models.CharField(max_length=20, choices=DOSAGE_FORMS, default="tablet")
    strength = models.CharField(max_length=50, blank=True, help_text="e.g., 500 mg")
    description = models.TextField(blank=True)
    upc = models.CharField(max_length=64, blank=True, help_text="Barcode/UPC/GTIN")

    class Meta:
        unique_together = ("name", "strength", "dosage_form")

    def __str__(self):
        return f"{self.name} {self.strength}".strip()

class Batch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="batches")
    lot_no = models.CharField(max_length=64)
    mfg_date = models.DateField()
    exp_date = models.DateField()
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="batches")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("medicine", "lot_no")

    @property
    def is_expired(self):
        return self.exp_date < timezone.localdate()

    @property
    def days_to_expiry(self):
        return (self.exp_date - timezone.localdate()).days

    def __str__(self):
        return f"{self.medicine} | Lot {self.lot_no} | Qty {self.quantity}"

MOVE_TYPES = [
    ("IN","Inbound (Receiving)"),
    ("OUT","Outbound (Shipping)"),
]

class StockMovement(models.Model):
    move_type = models.CharField(max_length=3, choices=MOVE_TYPES)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name="movements")
    quantity = models.PositiveIntegerField()
    ref_no = models.CharField(max_length=64, blank=True, help_text="Invoice/PO/SO/Reference")
    counterparty = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    moved_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def apply(self):
        if self.move_type == "IN":
            self.batch.quantity += self.quantity
        else:
            if self.quantity > self.batch.quantity:
                raise ValueError("Cannot ship more than available quantity.")
            self.batch.quantity -= self.quantity
        self.batch.save()

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)
        if new:
            self.apply()

    def __str__(self):
        return f"{self.move_type} {self.quantity} of {self.batch}"
