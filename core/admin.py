from django.contrib import admin
from .models import LabUser, Sample, PrimaryBeam, Spectrometer, AcquisitionTOFSIMS, PreProcessingSpectra, Spectra
# Register your models here.

admin.site.register(LabUser)
admin.site.register(Sample)
admin.site.register(PrimaryBeam)
admin.site.register(Spectrometer)
admin.site.register(AcquisitionTOFSIMS)
admin.site.register(PreProcessingSpectra)
admin.site.register(Spectra)