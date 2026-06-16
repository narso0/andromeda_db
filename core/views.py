from django.shortcuts import render
from core.models import Sample

def sample_list(request):
    samples = Sample.objects.all().order_by('-reception_date')
    
    return render(request, 'core/sample_list.html', {'samples': samples})