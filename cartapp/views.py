from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from ecommerce_app.models import Book
from .models import Cart,Checkout
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



@login_required(login_url='signin')
def cart(request):
    try:
        cart = Cart.objects.filter(user=request.user,ordered=False).order_by('-created_at')
    except ObjectDoesNotExist:
        pass
    context = {'cart':cart}

    return render(request,'cart.html',context)


@login_required(login_url='signin')
def add_to_cart(request, book_id):
    book = get_object_or_404(Book,id=book_id)
    
    cart_item,created = Cart.objects.get_or_create(book=book,user=request.user,ordered=False)

    if not created:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='signin')
def quantity_plus(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    if cart.quantity >= 1:
        cart.quantity +=1
        cart.save()

    return redirect('cart')

@login_required(login_url='signin')
def quantity_minus(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()
    
    return redirect('cart')


@login_required(login_url='signin')
def remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect('cart')



@login_required(login_url='signin')
def checkout(request,cart_id):
    payment = ""
    cart = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        book = request.POST.get('book_title')
        amount = int(request.POST.get('amount'))*100
        client = razorpay.Client(auth=('rzp_test_j3CDH5AT9kIHCA', 'G4gthDwLFYppB5jpJvNsqpj2'))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        print(payment)

        payments = Checkout.objects.create(cart=cart, amount=amount, payment_id=payment['id'],book=book)
        payments.save()

    return render(request, 'checkout.html',{'cart':cart,'payment':payment} )    

@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        order = Checkout.objects.filter(payment_id=order_id).first()
        order.paid = True
        order.save()
        
        cart = Cart.objects.get(id=order.cart.id)   
        if order.paid == True: 
            cart.ordered = True
            cart.save()

            book = cart.book
            print("old",book.stock)
            if book.stock>=cart.quantity:
                book.stock-=cart.quantity
                book.save()
                print("now",book.stock)
            else:
                print("not enough")

        print(cart.ordered)
        print(a)
    return render(request,'success.html')


@login_required(login_url='signin')
def orders(request):
    orders = Checkout.objects.filter(cart__user=request.user, paid=True).order_by('-id')
    return render(request,'orders.html',{'orders':orders})