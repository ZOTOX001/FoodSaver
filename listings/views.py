from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing, Claim
from .forms import ListingForm

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.save()
            return redirect('donor_dashboard')
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})

@login_required
def donor_dashboard(request):
    if request.user.role != 'donor' and not request.user.is_superuser:
         return redirect('dashboard')
         
    listings = Listing.objects.filter(donor=request.user).order_by('-created_at')
    # Fetch claims for these listings
    claims = Claim.objects.filter(listing__in=listings).order_by('-claimed_at')
    
    return render(request, 'listings/donor_dashboard.html', {'listings': listings, 'claims': claims})

@login_required
def claim_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        Claim.objects.create(listing=listing, claimant=request.user)
        listing.status = 'claimed'
        listing.save()
        return redirect('claimant_dashboard')
    return render(request, 'listings/claim_confirm.html', {'listing': listing})

@login_required
def approve_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    if request.user == claim.listing.donor:
        claim.status = 'approved'
        claim.save()
    return redirect('donor_dashboard')

@login_required
def complete_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    if request.user == claim.listing.donor:
        claim.status = 'completed'
        claim.save()
        claim.listing.status = 'completed'
        claim.listing.save()
    return redirect('donor_dashboard')

@login_required
def claimant_dashboard(request):
    if request.user.role != 'claimant' and not request.user.is_superuser:
        return redirect('dashboard')
    
    # Get active listings for list view
    listings = Listing.objects.filter(status='active').order_by('expiry_time')
    return render(request, 'listings/claimant_dashboard.html', {'listings': listings})

from django.http import JsonResponse

def listing_api(request):
    listings = Listing.objects.filter(status='active')
    data = []
    for listing in listings:
        data.append({
            'id': listing.id,
            'food_type': listing.get_food_type_display(),
            'quantity': listing.quantity_kg,
            'lat': listing.donor.latitude if listing.donor.latitude else 0,
            'lng': listing.donor.longitude if listing.donor.longitude else 0,
            'expiry': listing.expiry_time.isoformat(),
            'donor_name': listing.donor.username,
        })
    return JsonResponse({'listings': data})
