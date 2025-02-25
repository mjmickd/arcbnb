from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Listing, Booking, Feature
from .forms import BookingForm


# Create your views here.
def home(request):
    return render(request, 'home.html')
def listings_index(request):
   listings = Listing.objects.all()
   features = Feature.objects.all()
   return render(request, 'listings/index.html', {
         'listings': listings,
         'features': features,
   })
def index_feature(request, feature_id):
   features = Feature.objects.all()
   listings = Listing.objects.filter(features = feature_id)
   feature = Feature.objects.get(id=feature_id)
   current = feature_id
   return render(request, 'listings/filter/index_feature.html', {
         'listings': listings,
         'feature': feature,
         'features': features,
         'current': current,
   })

def listings_detail(request, listing_id):
   listing = Listing.objects.get(id=listing_id)
   booking_form = BookingForm()
   feature = listing.features.all()
   # id_list = listing.features.
   # features = Feature.objects.filter(id__in=id_list)
   return render(request, 'listings/detail.html', {
      'listing': listing, 'booking_form': booking_form, 'feature': feature,
   })
  
def add_booking(request, listing_id):
   if request.user.is_authenticated:
      user = request.user
      form = BookingForm(request.POST)
      if form.is_valid():
         new_booking = form.save(commit=False)
         new_booking.listing_id = listing_id
         new_booking.user = user
         new_booking.save()
      return redirect('/user/bookings', listing_id=listing_id)
   else:
      return redirect('/listings/detail', listing_id=listing_id)
   
class BookingUpdate(UpdateView):
  model = Booking
  fields = ['guests']

class BookingDelete(DeleteView):
  model = Booking
  success_url = '/user/bookings'



def user_bookings(request):
   user = request.user
   bookings = Booking.objects.filter(user=user)
   print(bookings)
   return render(request, 'user/bookings.html', {
      'user': user,
      'bookings': bookings,
   })


def booking_detail(request, booking_id):
   user = request.user
   booking = Booking.objects.get(id=booking_id)
   return render(request, 'user/booking_detail.html', {
      'booking': booking,
      'user': user
   })



def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - Try Again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)