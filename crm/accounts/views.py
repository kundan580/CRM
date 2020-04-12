from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *

from .forms import *

# Create your views here.

def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all().order_by('-date_created')[:5]

	# filter after slicing isn't working
	total_customer = customers.count()
	total_orders = Order.objects.all().count()
	delivered_orders = Order.objects.all().filter(status='Delivered').count()
	pending_orders = Order.objects.all().filter(status='Pending').count()

	context = {'customers':customers, 'orders': orders,
			 'total_orders': total_orders, 'delivered_orders': delivered_orders,
			 'pending_orders': pending_orders}

	return render(request, 'accounts/dashboard.html', context)

def products(request):
	products = Product.objects.all()
	context = {'products': products}

	return render(request, 'accounts/products.html', context)

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()


	context = {'customer':customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'accounts/customer.html',context)


def createOrder(request, pk):

	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
	customer = Customer.objects.get(id=pk)
	# form = OrderForm(initial={"customer": customer})
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {"formset" : formset}
	return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'formset':form}
	return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete_order.html', context)