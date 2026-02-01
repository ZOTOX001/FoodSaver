from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.role == 'donor':
        return redirect('donor_dashboard')
    elif request.user.role == 'claimant':
        return redirect('claimant_dashboard')
    elif request.user.role == 'admin':
        return redirect('/admin/')
    return render(request, 'users/dashboard_placeholder.html', {'role': 'Unknown'})

from django.shortcuts import get_object_or_404
from .models import User

def ngo_directory(request):
    # Fetch all claimants (NGOs/Communities)
    # In a real app, we might want to filter by verifiction status too
    ngos = User.objects.filter(role='claimant')
    return render(request, 'users/ngo_directory.html', {'ngos': ngos})

def profile_view(request, user_id):
    user_profile = get_object_or_404(User, pk=user_id)
    # Fetch stats (mock logic or real aggregation)
    impact_stats = {
        'meals_served': 1200 + (user_profile.id * 50), # Mock data
        'volunteers': 5 + (user_profile.id % 20),
        'badges': ['Top Rated', 'Verified'] if user_profile.is_verified else []
    }
    return render(request, 'users/ngo_profile.html', {
        'profile_user': user_profile,
        'stats': impact_stats
    })

@login_required
def connected_ngos(request):
    if request.user.role != 'donor':
        return redirect('dashboard')
    
    # logic: Find NGOs (Claimants) who have successfully claimed from this donor
    # This involves a join: Claim -> Listing -> Donor
    from listings.models import Claim
    
    # Get distinct claimants who have claims on this donor's listings
    connected_claimants_ids = Claim.objects.filter(
        listing__donor=request.user, 
        status__in=['approved', 'completed']
    ).values_list('claimant_id', flat=True).distinct()
    
    connected_ngos_list = User.objects.filter(id__in=connected_claimants_ids)
    
    return render(request, 'users/connected_ngos.html', {'ngos': connected_ngos_list})
