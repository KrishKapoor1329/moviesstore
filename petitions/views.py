from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Petition, Vote
from .forms import PetitionForm

def index(request):
    petitions = Petition.objects.all().order_by('-created_at')
    template_data = {'petitions': petitions}
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Your petition has been submitted')
            return redirect('petitions.show', id=petition.id)
    else:
        form = PetitionForm()
    template_data = {'form': form}
    return render(request, 'petitions/create.html', {'template_data': template_data})

def show(request, id):
    petition = get_object_or_404(Petition, id=id)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    template_data = {'petition': petition, 'user_vote': user_vote,}
    return render(request, 'petitions/show.html', {'template_data': template_data})

@login_required
def vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')
        if vote_type in ['up', 'down']:
            vote, created = Vote.objects.update_or_create(
                petition=petition,
                user=request.user,
                defaults={'vote_type': vote_type},
            )

            if created:
                messages.success(request, f"Your {vote.get_vote_type_display()} has been recorded.")
            else:
                messages.success(request, f"Your vote has been updated to a {vote.get_vote_type_display()}")

    return redirect('petitions.show', id=petition.id)
