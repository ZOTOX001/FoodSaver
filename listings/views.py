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
    
    # Split claims into Pending and History
    pending_claims = Claim.objects.filter(listing__in=listings, status='pending').order_by('-claimed_at')
    # History includes completed, rejected, and approved (if any legacy exist)
    history_claims = Claim.objects.filter(listing__in=listings, status__in=['completed', 'rejected', 'approved']).order_by('-claimed_at')
    
    return render(request, 'listings/donor_dashboard.html', {
        'listings': listings, 
        'pending_claims': pending_claims,
        'history_claims': history_claims
    })

@login_required
def claim_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        # Create claim with default status 'pending'
        Claim.objects.create(listing=listing, claimant=request.user)
        return redirect('claimant_dashboard')
    return render(request, 'listings/claim_confirm.html', {'listing': listing})

@login_required
def approve_claim(request, claim_id):
    # Single step approval: Pending -> Completed
    claim = get_object_or_404(Claim, id=claim_id)
    if request.user == claim.listing.donor:
        claim.status = 'completed'
        claim.save()
        
        # Mark listing as completed
        listing = claim.listing
        listing.status = 'completed'
        listing.save()
        
    return redirect('donor_dashboard')

@login_required
def reject_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    if request.user == claim.listing.donor:
        claim.status = 'rejected'
        claim.save()
        # Listing remains active for others to claim
    return redirect('donor_dashboard')

# Legacy verify view can be removed or redirected if no longer used
@login_required
def complete_claim(request, claim_id):
    return approve_claim(request, claim_id)

@login_required
def claimant_dashboard(request):
    if request.user.role != 'claimant' and not request.user.is_superuser:
        return redirect('dashboard')
    
    # Get active listings for list view
    listings = Listing.objects.filter(status='active').order_by('expiry_time')
    
    # Get IDs of listings this user has already claimed (pending)
    my_pending_claims_ids = Claim.objects.filter(
        claimant=request.user, 
        status='pending'
    ).values_list('listing_id', flat=True)

    return render(request, 'listings/claimant_dashboard.html', {
        'listings': listings, 
        'pending_claim_ids': my_pending_claims_ids
    })

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

@login_required
def my_claims(request):
    if request.user.role != 'claimant':
        return redirect('dashboard')
    
    # Active claims (pending or approved)
    claims = Claim.objects.filter(claimant=request.user, status__in=['pending', 'approved']).order_by('-claimed_at')
    return render(request, 'listings/my_claims.html', {'claims': claims})

@login_required
def history_view(request):
    if request.user.role != 'claimant':
        return redirect('dashboard')
        
    # Past claims (completed or rejected)
    claims = Claim.objects.filter(claimant=request.user, status__in=['completed', 'rejected']).order_by('-claimed_at')
    return render(request, 'listings/history.html', {'claims': claims})

