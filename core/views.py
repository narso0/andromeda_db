from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import Sample, User
from .models import Sample, User, AcquisitionTOFSIMS, Laboratory
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SampleForm, UserForm

class SampleDetailView(LoginRequiredMixin, DetailView):
    model = Sample
    template_name = 'core/sample_detail.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Sample.objects.all()
        core_profile = getattr(self.request.user, 'core_profile', None)
        return core_profile.samples.all() if core_profile else Sample.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acquisitions'] = self.object.acquisition.select_related(
            'spectro_params', 'spectro_params__equipment'
        ).order_by('-run_date')
        return context
    

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'core/user_detail.html'

class AcquisitionDetailView(LoginRequiredMixin, DetailView):
    model = AcquisitionTOFSIMS
    template_name = 'core/acquisition_detail.html'
    context_object_name = 'acquisition'

    def get_queryset(self):
        base = AcquisitionTOFSIMS.objects.select_related(
            'sample', 'primary_beam', 'spectro_params', 'spectro_params__equipment'
        ).prefetch_related('pre_processings__spectra')
        if self.request.user.is_superuser:
            return base
        core_profile = getattr(self.request.user, 'core_profile', None)
        return base.filter(sample__user=core_profile) if core_profile else base.none()

def home(request):
    stats = {
        'samples': Sample.objects.count(),
        'acquisitions': AcquisitionTOFSIMS.objects.count(),
        'users': User.objects.count(),
    }
    return render(request, 'core/home.html', {'stats': stats})


@login_required
def sample_list(request):
    if request.user.is_superuser:
        samples = Sample.objects.all()
    else:
        core_profile = getattr(request.user, 'core_profile', None)
        samples = core_profile.samples.all() if core_profile else Sample.objects.none()
    samples = samples.select_related('user').order_by('-reception_date')
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