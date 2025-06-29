from django.shortcuts import render, redirect
from .models import Receipt
from .ocr import extract_receipt_data
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .ocr import extract_receipt_data
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

@login_required
def upload_receipt(request):
    if request.method == 'POST' and 'receipt' in request.FILES:
        img = request.FILES['receipt']
        ext = img.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'pdf']:
            return HttpResponse("Only image files allowed", status=400)

        receipt = Receipt.objects.create(user=request.user, image=img)
        data, raw_text = extract_receipt_data(receipt.image.path, return_text=True)
        receipt.vendor = data['vendor']
        receipt.total = data['total']
        receipt.date = data['date']
        receipt.raw_text = raw_text  # Save raw OCR text
        receipt.save()
        return redirect('dashboard')
    return render(request, 'upload.html')


@login_required
def dashboard(request):
    receipts = Receipt.objects.filter(user=request.user)
    
    # Filtering
    vendor = request.GET.get('vendor')
    month = request.GET.get('month')  # format: YYYY-MM

    if vendor:
        receipts = receipts.filter(vendor__icontains=vendor)
    if month:
        year, mon = map(int, month.split('-'))
        receipts = receipts.filter(date__year=year, date__month=mon)

    return render(request, 'dashboard.html', {'receipts': receipts})


from datetime import datetime




@login_required
@csrf_exempt
def edit_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id, user=request.user)
    if request.method == 'POST':
        receipt.vendor = request.POST['vendor']
        receipt.total = request.POST['total']
        date_input = request.POST.get('date', '').strip()
        if date_input:
            try:
                receipt.date = datetime.strptime(date_input, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)
        else:
            receipt.date = None
        receipt.save()
        return redirect('dashboard')
    return render(request, 'edit.html', {'r': receipt})