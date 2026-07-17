from django.shortcuts import redirect, render
from django.views.generic import DetailView
from .models import Sample, User
from .forms import SampleForm, UserForm

class SampleDetailView(DetailView):
    model = Sample
    template_name = 'core/sample_detail.html'

class UserDetailView(DetailView):
    model = User
    template_name = 'core/user_detail.html'

def home(request):
    return render(request, 'core/home.html')
def sample_list(request):
    samples = Sample.objects.all().order_by('-reception_date')
    return render(request, 'core/sample_list.html', {'samples': samples})
def add_sample(request):
    if not request.user.has_perm('core.add_sample'):
        return redirect('sample_list')
    if request.method == 'POST':
        form = SampleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sample_list')
    else:
        form = SampleForm()
    return render(request, 'core/sample_form.html', {'form': form})

def user_list(request):
    users = User.objects.all().order_by('last_name')
    return render(request, 'core/user_list.html', {'users': users})

def add_user(request):
    if not request.user.has_perm('core.add_user'):
        return redirect('user_list')
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'core/user_form.html', {'form': form})