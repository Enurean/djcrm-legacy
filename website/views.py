from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Customer


def home(request):
    customers = Customer.objects.all()
    # Check login status
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in sucessfully")
            return redirect('home')
        else:
            messages.success(request, "Error logging in, try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {"customers":customers})


# def login_user(request):
#     pass


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Login user automatically
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You've been successfully registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {"form":form})
    
    return render(request, 'register.html', {"form":form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Check for customer records
        customer_record = Customer.objects.get(id=pk)
        return render(request, 'customer_record.html', {"customer_record":customer_record})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')
    

def delete_customer(request, pk):
    if request.user.is_authenticated:
        delete_it = Customer.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Customer deleted")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')
    

def add_customer(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, "Customer added")
                return redirect('home')
        return render(request, 'add_customer.html', {"form":form})
    else:
        messages.success(request, "You must be logged in to add customers")
        return redirect('home')
    
def update_customer(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        # Work with updated record instance
        form = AddRecordForm(request.POST or None, instance=current_customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated")
            return redirect('home')
        return render(request, 'update_customer.html', {"form":form})
    else:
        messages.success(request, "You must be logged in to update customers")
        return redirect('home')