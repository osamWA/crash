from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.db.models import Count
from .forms  import createProduct,createCustomer,createOrder,createOrderHistory,createUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def Logout(request):
    return redirect('Login')

def Login(request):
        if request.method == 'POST':
            print('get the post request')
            theusername = request.POST.get('username')
            thepassword = request.POST.get('password')

            theloginuser = authenticate(request, username = theusername, password=thepassword)
            if theloginuser is not None:
                print('get the post request start logining in')
                login(request,theloginuser)
                return redirect('home')
            else:
                messages.info(request,'username or password is incorrect !')
        context={}
        return render(request,'accounts/login.html',context)

def SignUp(request):
    if request.user.is_authenticated:
            return redirect ('home')
    else:    
        form = createUserForm()

        if request.method == 'POST':
            form = createUserForm(request.POST)
            print('here is the form to save user',form)
            if form.is_valid():
                print('form validated')
                form.save()
                theUser = form.cleaned_data.get('email')
                messages.success(request, 'Account created sucssefully for '+theUser)
                return redirect('Login')
        context = {'form':form}
        return render(request,'accounts/Signup.html',context)


@login_required(login_url='Login')
def home(request):
    TotalNumberOfOrders = Order.objects.all().count()
    #orderbycustomer = Order.objects.values('customer','customer_id').annotate(dcount=Count('product_id'))
    orderbycustomer= Order.objects.values('customer_id').annotate(dcount=Count('customer_id')).values('customer_id__name','dcount','customer_id')
    Customers = Customer.objects.all()
    Orders = Order.objects.all().order_by('-date_created')[:4]
    TotalInProgress = Order.objects.filter(status__icontains='للتوصيل').count()
    TotalDelivredOrders = Order.objects.filter(status__icontains='تم التوصيل').count()
    TotalPindingOrders = Order.objects.filter(status__icontains='متأخر').count()
    print('total of orders',orderbycustomer)

    context = {
    'Customers':Customers,
    'TotalNumberOfOrders':TotalNumberOfOrders,
    'TotalDelivredOrders':TotalDelivredOrders,
    'TotalPindingOrders':TotalPindingOrders,
    'TotalInProgress':TotalInProgress,
    'Orders':Orders,
    'orderbycustomer':orderbycustomer
    }
    return render(request,'accounts/dashboard.html',context)


def UserPage(request):
    context={}
    return render(request,'accounts/user.html',context)
@login_required(login_url='Login')
def customers(request,pk):
    customerInfo = Customer.objects.get(id=pk)
    theOrders = customerInfo.order_set.all()
    totaltheOrders = customerInfo.order_set.all().count()
    myfilter = OrderFilter(request.GET,queryset=theOrders)
    theOrders = myfilter.qs
    context = {
            'customerInfo':customerInfo,
            'theOrders':theOrders, 
            'totaltheOrders':totaltheOrders,
            'myfilter':myfilter,
            }
    print('this Total Orders',totaltheOrders)
    return render(request,'accounts/customers.html',context)

@login_required(login_url='Login')
def CustomerProductSearch(request,pk,kw):
    customerInfo = Customer.objects.get(id=pk)
    if request.method == 'POST':
        CustomertheOrders = customerInfo.order_set.filter(product=kw)
    else:
        CustomertheOrders = customerInfo.order_set.all()
    context = {"CustomertheOrders":CustomertheOrders}
    return render(request,)

@login_required(login_url='Login')
def products(request):
    allOrders = Product.objects.all()
    print(allOrders)
    return render(request,'accounts/products.html', {'allOrders':allOrders})

@login_required(login_url='Login')
def create_products(request):
    OrderForm = createProduct()

    if request.method == 'POST':
        saveForm = createProduct(request.POST)
        print(saveForm)
        if saveForm.is_valid():
            saveForm.save()
            return redirect('products')
        else:
            OrderForm = UserForm()
    context = {'OrderForm':OrderForm}
    return render(request,'accounts/create_product.html',context)

@login_required(login_url='Login')
def update_products(request,pk):
    theProduct = Product.objects.get(id=pk)
    UpdateForm = createProduct(instance=theProduct)

    if request.method == 'POST':
        UpdateForm = createProduct(request.POST,instance=theProduct)
        if UpdateForm.is_valid():
            UpdateForm.save()
            return redirect('products')
        else:
            UpdateForm = createProduct(instance=theProduct) 

    context = {'UpdateForm':UpdateForm} 
    return render(request,'accounts/updateProduct.html',context)

@login_required(login_url='Login')
def delete_products(request,pk):
    thedeleteproduct = Product.objects.get(id=pk)
    thedeleteproduct.delete()
    return redirect('products')

@login_required(login_url='Login')
def allCustomers(request):
    TheallCustomers = Customer.objects.all()
    context = {'TheallCustomers':TheallCustomers}
    return render(request,'accounts/allCustomers.html',context)

@login_required(login_url='Login')
def create_customer(request):
    CustomerForm = createCustomer()

    if request.method == 'POST':
        saveForm = createCustomer(request.POST)
        print(saveForm)
        if saveForm.is_valid():
            saveForm.save()
            return redirect('/')
        else:
            CustomerForm = createCustomer()
    context = {'CustomerForm':CustomerForm}
    return render(request,'accounts/createCustomer.html',context)


@login_required(login_url='Login')
def update_customer(request,pk):
    theCustomer = Customer.objects.get(id=pk)
    UpdateForm = createCustomer(instance=theCustomer)
    theid = pk
    if request.method == 'POST':
        UpdateForm = createCustomer(request.POST,instance=theCustomer)
        if UpdateForm.is_valid():
            UpdateForm.save()
            return redirect('customers',theid)
        else:
            UpdateForm = createCustomer(instance=theCustomer) 

    context = {'UpdateForm':UpdateForm} 
    return render(request,'accounts/updateCustomer.html',context)

@login_required(login_url='Login')
def delete_customer(request,pk):
    thedeleteCustomer = Customer.objects.get(id=pk)
    thedeleteCustomer.delete()
    return redirect('/')

@login_required(login_url='Login')
def allOrders(request):
    TheallOrders = Order.objects.all()
    myfilter = OrderFilter(request.GET,queryset=TheallOrders)
    TheallOrders = myfilter.qs

    context = {'TheallOrders':TheallOrders,'myfilter':myfilter}
    return render(request,'accounts/allOrders.html',context)

@login_required(login_url='Login')
def create_orders(request): 
    OrderForm = createOrder()
    #in case i want to make a defult value by customer below
    #OrderForm = createOrder(initial={'customer':theCustomer})

    if request.method == 'POST':
        saveForm = createOrder(request.POST)
        if saveForm.is_valid():
            saveForm.save()
            return redirect('/')
        else:
            OrderForm = createOrder()
    context = {'OrderForm':OrderForm}
    return render(request,'accounts/createOrder.html',context)

@login_required(login_url='Login')
def update_orders(request,pk):
    theOrder = Order.objects.get(id=pk)


    theHistory = createOrderHistory({
    'Order': theOrder.id,
    'customer': theOrder.customer, 
    'product': theOrder.product, 
    'date_created': theOrder.date_created,
    'status': theOrder.status, 
    'note': theOrder.note
    }) 

    print('The History of the order ',theHistory)
    UpdateForm = createOrder(instance=theOrder)
    theid = pk
    if request.method == 'POST':
        UpdateForm = createOrder(request.POST,instance=theOrder)
        if theHistory.is_valid():
            if UpdateForm.is_valid():
                theHistory.save()
                UpdateForm.save()
                return redirect('home')
        else:
            UpdateForm = createOrder(instance=theOrder) 

    context = {'UpdateForm':UpdateForm} 
    return render(request,'accounts/updateOrder.html',context)

@login_required(login_url='Login')
def delete_orders(request,pk):
    thedeleteOrder = Order.objects.get(id=pk)
    thedeleteOrder.delete()
    return redirect('/')

@login_required(login_url='Login')
def orderHistory(request,pk):

    theUnion = OrderHistory.objects.filter(Order__id=pk)

    print('the result of the query ',theUnion)
    context = {'theUnion':theUnion}
    return render(request,'accounts/orderHistory.html',context)