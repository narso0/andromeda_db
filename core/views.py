from django.shortcuts import redirect, render
from .models import Sample
from .forms import SampleForm


def sample_list(request):
    samples = Sample.objects.all().order_by('-reception_date')
    return render(request, 'core/sample_list.html', {'samples': samples})
def add_sample(request):
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sample_list')
    else:
        form = SampleForm()
    return render(request, 'core/sample_form.html', {'form': form})