from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from .models import Medicine, Batch, StockMovement, Address
from .forms import SignUpForm, MedicineForm, BatchForm, MovementForm, AddressForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "auth/signup.html", {"form": form})

@login_required
def dashboard(request):
    today = timezone.localdate()
    expiring_soon_days = int(request.GET.get("exp_days", 30))
    low_stock_threshold = int(request.GET.get("low", 20))

    total_items = Medicine.objects.count()
    total_batches = Batch.objects.count()
    total_qty = Batch.objects.aggregate(q=Sum("quantity"))["q"] or 0
    expiring_soon = Batch.objects.filter(exp_date__lte=today + timezone.timedelta(days=expiring_soon_days),
                                         exp_date__gte=today, quantity__gt=0)
    expired = Batch.objects.filter(exp_date__lt=today, quantity__gt=0)
    low_stock = Batch.objects.filter(quantity__lte=low_stock_threshold)

    recent_moves = StockMovement.objects.order_by("-moved_at")[:10]

    context = dict(
        total_items=total_items,
        total_batches=total_batches,
        total_qty=total_qty,
        expiring_soon=expiring_soon,
        expired=expired,
        low_stock=low_stock,
        recent_moves=recent_moves,
        exp_days=expiring_soon_days,
        low=low_stock_threshold,
    )
    return render(request, "dashboard.html", context)

@login_required
def medicine_list(request):
    q = request.GET.get("q","").strip()
    qs = Medicine.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q)|Q(category__icontains=q)|Q(upc__icontains=q))
    return render(request, "medicine/list.html", {"items": qs, "q": q})

@login_required
def medicine_create(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, "Medicine created.")
            return redirect("medicine_detail", pk=item.pk)
    else:
        form = MedicineForm()
    return render(request, "medicine/form.html", {"form": form})

@login_required
def medicine_detail(request, pk):
    item = get_object_or_404(Medicine, pk=pk)
    batches = item.batches.order_by("exp_date")
    return render(request, "medicine/detail.html", {"item": item, "batches": batches})

@login_required
def batch_list(request):
    q = request.GET.get("q","").strip()
    qs = Batch.objects.select_related("medicine","location").all().order_by("exp_date")
    if q:
        qs = qs.filter(Q(medicine__name__icontains=q)|Q(lot_no__icontains=q)|Q(location__name__icontains=q))
    return render(request, "batch/list.html", {"items": qs, "q": q})

@login_required
def batch_create(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            b.created_by = request.user
            b.save()
            messages.success(request, "Batch created.")
            return redirect("batch_detail", pk=b.pk)
    else:
        form = BatchForm()
    return render(request, "batch/form.html", {"form": form})

@login_required
def batch_detail(request, pk):
    b = get_object_or_404(Batch, pk=pk)
    moves = b.movements.order_by("-moved_at")
    return render(request, "batch/detail.html", {"b": b, "moves": moves})

@login_required
def movement_list(request):
    qs = StockMovement.objects.select_related("batch","batch__medicine","counterparty").order_by("-moved_at")
    return render(request, "movement/list.html", {"items": qs})

@login_required
def movement_create(request):
    if request.method == "POST":
        form = MovementForm(request.POST)
        if form.is_valid():
            move = form.save(commit=False)
            move.created_by = request.user
            try:
                move.save()
                messages.success(request, "Stock movement recorded.")
                return redirect("movement_list")
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = MovementForm(initial={"move_type":"IN"})
    return render(request, "movement/form.html", {"form": form})

@login_required
def address_list(request):
    qs = Address.objects.all()
    return render(request, "address/list.html", {"items": qs})

@login_required
def address_create(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Address saved.")
            return redirect("address_list")
    else:
        form = AddressForm()
    return render(request, "address/form.html", {"form": form})
