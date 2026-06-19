from django.contrib import admin
from .models import Laboratory, User, Sample, PrimaryBeam, SpectrometerParameters, Equipment, AcquisitionTOFSIMS, PreProcessingSpectra, Spectra# Register your models here.

admin.site.register(Laboratory)
admin.site.register(User)
admin.site.register(Sample)
admin.site.register(PrimaryBeam)
admin.site.register(SpectrometerParameters)
admin.site.register(Equipment)
admin.site.register(AcquisitionTOFSIMS)
admin.site.register(PreProcessingSpectra)
admin.site.register(Spectra)