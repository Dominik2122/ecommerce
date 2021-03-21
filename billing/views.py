from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.


import stripe
stripe.api_key = 'sk_test_51IXW3aCkhkhAd2s3znmhkXSYIzCuKI4eB46wGwcfFO5yjkx7eXCmfgfXq8sUiAltXuyZJti88K59JHvC2r9HavWG00dgpPm050'
STRIPE_PUB_KEY = 'pk_test_51IXW3aCkhkhAd2s3FSB27u0ycISe07B0tQEGMhcKmqfZDDv2rMxIRAebwsd0EYrtCFPCurNhewcrrBqop69axiFv00vLk5rsta'

def payment_method_view(request):
    return render(request,'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY})

def payment_method_createview(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'Done'})
    return HttpResponse('error', status_code=402)
