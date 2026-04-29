from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db import transaction
from .models import Order, Payment
from .serializers import PaymentInitializeSerializer, PaymentVerifySerializer
from users.models import UserProfile
from notifications.views import create_notification
import paystack
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initialize_payment(request):
    serializer = PaymentInitializeSerializer(data=request.data)
    if serializer.is_valid():
        order_id = serializer.validated_data['order_id']
        email = serializer.validated_data['email']
        amount = serializer.validated_data['amount']
        callback_url = serializer.validated_data.get('callback_url', '')
        
        try:
            order = Order.objects.get(id=order_id, buyer=request.user)
            
            # Create payment record
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={'amount': amount}
            )
            
            # Initialize Paystack transaction
            paystack_instance = paystack.Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
            
            response = paystack_instance.transaction.initialize(
                reference=payment.paystack_reference or f'pay_{order.id}_{datetime.now().timestamp()}',
                email=email,
                amount=int(amount * 100),  # Convert to kobo
                callback_url=callback_url,
                metadata={
                    'order_id': order.id,
                    'custom_fields': [
                        {
                            'display_name': 'Order ID',
                            'variable_name': 'order_id',
                            'value': order.id
                        }
                    ]
                }
            )
            
            if response['status']:
                payment.paystack_reference = response['data']['reference']
                payment.save()
                
                return Response({
                    'status': 'success',
                    'data': response['data']
                })
            else:
                return Response({
                    'status': 'error',
                    'message': response['message']
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    reference = request.GET.get('reference')
    
    if not reference:
        return Response({'error': 'Reference is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        paystack_instance = paystack.Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
        response = paystack_instance.transaction.verify(reference)
        
        if response['status'] and response['data']['status'] == 'success':
            # Update payment record
            payment = Payment.objects.get(paystack_reference=reference)
            payment.status = 'success'
            payment.paid_at = datetime.now()
            payment.save()
            
            # Update order status
            order = payment.order
            order.status = 'accepted'  # Auto-accept order on successful payment
            order.save()
            
            # Update seller's total sales
            profile, created = UserProfile.objects.get_or_create(user=order.seller)
            profile.total_sales += order.total_amount
            profile.save()
            
            # Create notification
            create_notification(
                order.buyer, 'order', 'Payment Successful',
                f'Your payment for order {order.id} has been confirmed',
                order.id
            )
            create_notification(
                order.seller, 'order', 'Payment Received',
                f'Payment received for order {order.id}',
                order.id
            )
            
            return Response({
                'status': 'success',
                'message': 'Payment verified successfully',
                'data': response['data']
            })
        else:
            # Update payment status to failed
            payment = Payment.objects.get(paystack_reference=reference)
            payment.status = 'failed'
            payment.save()
            
            return Response({
                'status': 'error',
                'message': 'Payment verification failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])
def paystack_webhook(request):
    # Verify webhook signature (optional but recommended)
    # You should verify the webhook signature here
    
    event = request.data.get('event')
    data = request.data.get('data')
    
    if event == 'charge.success':
        reference = data.get('reference')
        try:
            payment = Payment.objects.get(paystack_reference=reference)
            if payment.status != 'success':
                payment.status = 'success'
                payment.paid_at = datetime.now()
                payment.save()
                
                # Update order and create notifications
                order = payment.order
                order.status = 'accepted'
                order.save()
                
                profile, created = UserProfile.objects.get_or_create(user=order.seller)
                profile.total_sales += order.total_amount
                profile.save()
                
                create_notification(
                    order.buyer, 'order', 'Payment Successful',
                    f'Your payment for order {order.id} has been confirmed',
                    order.id
                )
                create_notification(
                    order.seller, 'order', 'Payment Received',
                    f'Payment received for order {order.id}',
                    order.id
                )
        except Payment.DoesNotExist:
            pass
    
    elif event == 'charge.failed':
        reference = data.get('reference')
        try:
            payment = Payment.objects.get(paystack_reference=reference)
            payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    return Response({'status': 'success'})
