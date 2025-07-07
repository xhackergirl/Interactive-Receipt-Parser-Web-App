from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import generics, status
from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.db.models import Sum

from .models import Receipt
from .serializers import ReceiptSerializer, RegisterSerializer
from .ocr import extract_receipt_data


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_receipts(request):
    receipts = Receipt.objects.filter(user=request.user)
    serializer = ReceiptSerializer(receipts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_receipt_api(request):
    parser_classes = [MultiPartParser]
    file = request.FILES.get('image')
    if not file:
        return Response({'error': 'No file provided'}, status=400)

    receipt = Receipt.objects.create(user=request.user, image=file)
    data, raw = extract_receipt_data(receipt.image.path, return_text=True)
    receipt.vendor = data.get('vendor', '')
    receipt.total = data.get('total', None)
    receipt.date = data.get('date', None)
    receipt.raw_text = raw
    receipt.save()
    return Response(ReceiptSerializer(receipt).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_receipt(request, receipt_id):
    try:
        receipt = Receipt.objects.get(id=receipt_id, user=request.user)
    except Receipt.DoesNotExist:
        return Response({'error': 'Receipt not found'}, status=404)

    receipt.vendor = request.data.get('vendor', receipt.vendor)
    receipt.total = request.data.get('total', receipt.total)
    receipt.date = request.data.get('date', receipt.date)
    receipt.save()
    return Response(ReceiptSerializer(receipt).data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("Incoming data:", request.data)  # Debug print
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Errors:", serializer.errors)  # Debug print
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReceiptListView(generics.ListCreateAPIView):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_summary(request):
    summary = (
        Receipt.objects.filter(user=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('total'))
        .order_by('month')
    )
    return Response(list(summary))
