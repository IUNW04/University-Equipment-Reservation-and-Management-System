from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q, Count
from .forms import BookingAdminForm, BookingUserForm, CreateItemForm, UpdateItemForm
from .models import Item, Booking, ItemType, ItemStatus
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import UserForm, UserUpdateForm
from.forms import ReportForm
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def user_is_staff(user):
    return user.is_staff

    
@user_passes_test(user_is_staff)
@login_required
def equipmentManagement(request):
    
    user = request.user
    is_staff = user.is_staff

    itemtypes = ItemType.objects.all()
    itemstatus = ItemStatus.objects.all()

    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    item = Item.objects.filter(
        Q(type__type__icontains=q) |
        Q(name__icontains=q) |
        Q(deviceSerialNumber__icontains=q) |
        Q(CPU__icontains=q) |
        Q(GPU__icontains=q) |
        Q(RAM__icontains=q) |
        Q(location__icontains=q) |
        Q(status__status__icontains=q)
    )
    totalInventory = item.count()

    context = {'item': item, 'itemtypes': itemtypes, 'itemstatus': itemstatus, 'totalInventory': totalInventory, 'is_staff': is_staff}
    return render(request, "equipmentManagement.html", context)


@login_required
def equipmentView(request):
    
    user = request.user

   
    is_staff = user.is_staff

    itemtypes = ItemType.objects.all()
    itemstatus = ItemStatus.objects.all()

    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    sort_by = request.GET.get('sort')

    items = Item.objects.filter(
        Q(type__type__icontains=q) |
        Q(name__icontains=q) |
        Q(deviceSerialNumber__icontains=q) |
        Q(CPU__icontains=q) |
        Q(GPU__icontains=q) |
        Q(RAM__icontains=q) |
        Q(location__icontains=q) |
        Q(status__status__icontains=q)
    )

    if status_filter:
        items = items.filter(status__status=status_filter)
    if type_filter:
        items = items.filter(type__type=type_filter)
    if sort_by:
        items = items.order_by(sort_by)

    totalInventory = items.count()

    
    booking_form = BookingUserForm()

    context = {
        'items': items,
        'itemtypes': itemtypes,
        'itemstatus': itemstatus,
        'totalInventory': totalInventory,
        'booking_form': booking_form,  
        'is_staff': is_staff
    }
    return render(request, 'equipmentView.html', context)



@login_required
def book_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        form = BookingUserForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.item = item
            booking.user = request.user
            booking.save()
            
            if item.quantity is not None:
                item.quantity = int(item.quantity)
                item.quantity -= 1
                item.save()  
            messages.success(request, 'Equipment booked successfully!')
            return redirect('bookings_view')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BookingUserForm()

    return render(request, 'booking_form.html', {'form': form, 'item': item})


@login_required
def bookings_view(request):
   
    user = request.user
 
    is_staff = user.is_staff
    
    filter_criteria = request.GET.get('filter')
    search_query = request.GET.get('search')

    if filter_criteria == 'earliestEndDate':
        
        current_bookings = Booking.objects.filter(user=user, end_date__gte=timezone.now().date()).order_by('end_date')
    elif filter_criteria == 'latestEndDate':
        
        current_bookings = Booking.objects.filter(user=user, end_date__gte=timezone.now().date()).order_by('-end_date')
    else:
        
        current_bookings = Booking.objects.filter(user=user, end_date__gte=timezone.now().date())

    return render(request, 'bookings.html', {'bookings': current_bookings, 'is_staff': is_staff})

@login_required
def historical(request):
    user = request.user

    is_staff = user.is_staff

    filter_criteria = request.GET.get('filter')

    if filter_criteria == 'earliestEndDate':
        
        historical_bookings = Booking.objects.filter(user=user, end_date__lt=timezone.now().date()).order_by('end_date')
    elif filter_criteria == 'latestEndDate':
        
        historical_bookings = Booking.objects.filter(user=user, end_date__lt=timezone.now().date()).order_by('-end_date')
    else:
        
        historical_bookings = Booking.objects.filter(user=user, end_date__lt=timezone.now().date())

    return render(request, 'historical.html', {'historical_bookings': historical_bookings, 'is_staff': is_staff})




@login_required
def rebook(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = BookingUserForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.item = item
            booking.user = request.user
            booking.save()
            
            if item.quantity is not None:
                item.quantity = int(item.quantity)
                item.quantity -= 1
                item.save()  
            messages.success(request, 'Equipment booked successfully!')
            return redirect('bookings_view')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BookingUserForm()

    return render(request, 'booking_form.html', {'form': form, 'item': item})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    item = booking.item  
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking canceled successfully!')
        if item.quantity is not None:
            item.quantity += 1  
            item.save()  
        return redirect('bookings_view')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_passes_test(user_is_staff)
@login_required
def booking_management(request):
    
    user = request.user
    is_staff = user.is_staff
    bookings = Booking.objects.all()
    filter_criteria = request.GET.get('filter')

    if filter_criteria == 'earliestEndDate':
        
        bookings = Booking.objects.order_by('end_date')
    elif filter_criteria == 'latestEndDate':
        
        bookings = Booking.objects.order_by('-end_date')

    
    if request.method == 'POST':
        form = BookingAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('booking_management')  
        else:
            messages.error(request, 'Form is not valid. Please check the input data.')
    else:
        form = BookingAdminForm()

    
    return render(request, 'bookingManagement.html', {'bookings': bookings, 'form': form, 'is_staff': is_staff})


@login_required
def updateItem(request, id):
    item = Item.objects.get(id=id)
    listitem = Item.objects.get(id=id)
    if request.method == "POST":
        form = UpdateItemForm(request.POST, instance=listitem)
        if form.is_valid():
            listitem.save()
            return redirect('equipmentManagement')
    else:
        form = UpdateItemForm(instance=listitem)
    context = {'listitem': listitem, 'form': form, 'item': item}
    return render(request, "updateItem.html", context)

@login_required
def createItem(request):
    if request.method == "POST":
        form = CreateItemForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect("equipmentManagement")
    else:
        form = CreateItemForm()
    return render(request, "createItem.html", {"form": form})

@login_required
def deleteItem(request, id):
    item = Item.objects.get(id=id)
    if request.method == "POST":
        item.delete()
        return redirect('equipmentManagement')
    return render(request, "deleteItem.html", {'item': item})

@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('booking_management')  
        else:
            messages.error(request, 'Form is not valid. Please check the input data.')
    else:
        form = BookingAdminForm()
    return render(request, 'booking_create.html', {'form': form})

@login_required
def booking_update(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        form = BookingAdminForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('booking_management')
    else:
        form = BookingAdminForm(instance=booking)
    return render(request, 'booking_update.html', {'form': form, 'booking': booking})

@login_required
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
        return redirect('booking_management')
    return render(request, 'booking_delete.html', {'booking': booking})


@user_passes_test(user_is_staff)
@login_required
def user_management(request):
    
    user = request.user
    is_staff = user.is_staff
    users = User.objects.all()
    form = UserForm(request.POST or None)
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(username__icontains=search_query)

    
    filter_criteria = request.GET.get('filter')
    if filter_criteria == 'staff':
        users = users.filter(is_staff=True)
    elif filter_criteria == 'nonStaff':
        users = users.filter(is_staff=False)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('user_management')

    return render(request, 'userManagement.html', {'users': users, 'form': form, 'is_staff': is_staff})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
           
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User added successfully!')
            return redirect('user_management')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserUpdateForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user_management')

    return render(request, 'userUpdate.html', {'form': form})
@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_management')
    return render(request, 'userDelete.html', {'user': user})

@user_passes_test(user_is_staff)
@login_required
def reports(request):
   
    user = request.user
    is_staff = user.is_staff
 
    items = Item.objects.all()
    total_inventory = items.count()
    types_inventory_query = Item.objects.values('type__type').annotate(count=Count('type'))
    types_inventory = {item['type__type']: item['count'] for item in types_inventory_query}

    
    if request.method == 'GET':
        item_id = request.GET.get('item')
        if item_id:
            item = Item.objects.get(id=item_id)
            return render(request, 'reports.html', {'items': items, 'item_id': item_id, 'item': item, 'totalInventory': total_inventory, 'typesInventory': types_inventory, 'is_staff': is_staff})
    
    
    return render(request, 'reports.html', {'items': items, 'totalInventory': total_inventory, 'typesInventory': types_inventory, 'is_staff': is_staff})


@login_required
def current_inventory_status(request, item_id):
    item = Item.objects.get(id=item_id)
    current_bookings = Booking.objects.filter(item=item, end_date__gte=timezone.now().date())
    return render(request, 'current_inventory_status.html', {'item': item, 'current_bookings': current_bookings})

@login_required
def equipment_usage_history(request, item_id):
    item = Item.objects.get(id=item_id)
    bookings = Booking.objects.filter(item=item).order_by('-start_date')
    return render(request, 'equipment_usage_history.html', {'item': item, 'bookings': bookings})

@login_required
def warranty_report(request, item_id):
    item = Item.objects.get(id=item_id)
    warranty_expiration_date = None
    if item.warranty_duration:  
        
        warranty_expiration_date = item.warranty_duration

    return render(request, 'warranty_report.html', {'item': item, 'warranty_expiration_date': warranty_expiration_date})



@login_required
def overdue_equipment(request, item_id):
    item = Item.objects.get(id=item_id)
    overdue_bookings = Booking.objects.filter(item=item, is_overdue=True)
    return render(request, 'overdue_equipment.html', {'item': item, 'overdue_bookings': overdue_bookings})


@login_required
def all_current_inventory_status(request):
    current_inventory = Item.objects.all()
    return render(request, 'all_current_inventory_status.html', {'current_inventory': current_inventory})

def user_login(request):
     
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        account_id = request.POST.get('accountid')
        password = request.POST.get('password')
        user = authenticate(username=account_id, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile_management')  
        else:
            messages.error(request, 'Invalid login credentials.')

   

    return render(request, 'login.html')


def user_register(request):
    if request.method == 'POST':
        account_id = request.POST.get('accountid')
        email = request.POST.get('email')  
        password = request.POST.get('password')

        if User.objects.filter(username=account_id).exists():
            messages.error(request, 'Account already registered.')
            return render(request, 'register.html')

        encrypted_password = make_password(password)

       
        User.objects.create_user(
            username=account_id,
            email=email,  
            password=password
        )

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')

@login_required
def profile_management(request):
    
    user = request.user
    initial = user.username[0].upper()

    is_staff = user.is_staff

    return render(request, 'profile_management.html', {'user': user, 'initial': initial, 'is_staff': is_staff})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print("Form bound:", form.is_bound)  
        print("Form data:", request.POST)  
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile_management')
        else:
            print(form.errors)  
            for error in form.errors.values():
                messages.error(request, error.as_text())
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
