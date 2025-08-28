from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Medicine, Batch, StockMovement, Address

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username","email","password1","password2")

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = "__all__"

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ("medicine","lot_no","mfg_date","exp_date","quantity","unit_price","location")

class MovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ("move_type","batch","quantity","ref_no","counterparty","notes","moved_at")

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
