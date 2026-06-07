from django.db import models

class LabUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True, blank=True)
    lab = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=200, null=True, blank=True)

class Sample(models.Model):
    MATERIAL_CHOICES = [
        ('Ceramic', 'Ceramic'), ('Lipids', 'Lipids'), ('Metals', 'Metals'),
        ('Micrometeorite', 'Micrometeorite'), ('Minerals', 'Minerals'), 
        ('Organic', 'Organic'), ('Oxides', 'Oxides'), ('Polymers', 'Polymers'),
        ('Substrate', 'Substrate'), ('Thin organic films', 'Thin organic films'),
    ]

    TYPE_SAMPLE_CHOICES = [
        ('Sample', 'Sample'), ('Substrate', 'Substrate'), ('Standard', 'Standard'),
    ]
    sample_id = models.AutoField(primary_key=True)
    sample_code = models.CharField(max_length=100, null=True, blank=True)
    batch_id = models.CharField(max_length=100, null=True, blank=True)

    type_sample = models.CharField(max_length=100, choices=TYPE_SAMPLE_CHOICES, null=True, blank=True)
    project_name = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey(LabUser, on_delete=models.RESTRICT, related_name='samples')

    material_classification = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
   
    description = models.TextField(null=True, blank=True)
    preparation_date = models.DateField()

    reception_date = models.DateField(null=True, blank=True)
    storage_conditions = models.CharField(max_length=200, null=True, blank=True)

    file_sample = models.FileField(upload_to='samples/pdfs/', null=True, blank=True)
    file_experiment_pdf = models.FileField(upload_to='samples/experiments/', null=True, blank=True)

class PrimaryBeam(models.Model):
    irradiation_id = models.AutoField(primary_key=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='irradiations')

    PRIMARY_ION_CHOICES = [
        ('Au +', 'Au +'),
        ('Au2 +', 'Au2 +'),
        ('Au3 +', 'Au3 +'),
        ('Au400 4+', 'Au400 4+'),
    ]
    
    ION_SOURCE_CHOICES = [
        ('Liquid metal', 'Liquid metal'),
        ('ECR', 'ECR'),
    ]
    SPOT_SIZE_CHOICES = [
        (100.0, '100 µm'),
        (200.0, '200 µm'),
        (400.0, '400 µm'),
        (800.0, '800 µm'),
    ]
    # required fields
    irradiation_date = models.DateField()
    primary_ion_species = models.CharField(max_length=50, choices=PRIMARY_ION_CHOICES)
    energy_MeV = models.FloatField()
    spot_size_um = models.FloatField(choices=SPOT_SIZE_CHOICES)
    pulse_beam_kV = models.FloatField()
    repetition_rate_kHz = models.FloatField()
    
    # optional fields
    accelerator_name = models.CharField(max_length=100, null=True, blank=True)
    ion_source_type = models.CharField(max_length=100, choices=ION_SOURCE_CHOICES, null=True, blank=True)
    fluence_ions_cm2 = models.FloatField(null=True, blank=True)
    current_nA = models.FloatField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    file_accelerator_log = models.FileField(upload_to='beams/logs/', null=True, blank=True)

class Spectrometer(models.Model):
    spectrometer_id = models.AutoField(primary_key=True)
    primary_beam = models.ForeignKey(PrimaryBeam, on_delete=models.CASCADE, related_name='spectrometers')

    POLARITY_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
    ]
    ANALYSER_CHOICES = [
        ('direct', 'direct'),
        ('reflecteur', 'reflecteur'),
    ]
    POSITION_CHOICES = [
        ('Substrate', 'Substrate'),
        ('Target', 'Target'),
    ]

    #required fields
    spectrometer_date = models.DateField()
    analyser_type = models.CharField(max_length=50, choices=ANALYSER_CHOICES)
    lens_ext = models.FloatField()
    lens_SI = models.FloatField()
    detector_bias = models.FloatField()
    sample_bias_kV = models.FloatField()
    polarity = models.CharField(max_length=20, choices=POLARITY_CHOICES)

    #optional fields
    instrument_name = models.CharField(max_length=100, null=True, blank=True)
    name_position = models.CharField(max_length=100, choices=POSITION_CHOICES, null=True, blank=True)
    analysis_area_um2 = models.FloatField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    file_slowcontrol_log_txt = models.FileField(upload_to='spectrometers/logs/', null=True, blank=True)
    spectrometer_metadata = models.JSONField(null=True, blank=True)


class AcquisitionTOFSIMS(models.Model):
    run_id = models.AutoField(primary_key=True)

    spectrometer = models.ForeignKey(Spectrometer, on_delete=models.CASCADE, related_name='acquisitions')
    SOFTWARE_CHOICES = [
        ('slow control EVE', 'slow control EVE'),
        ('Narval', 'Narval'),
        ('C-Visu', 'C-Visu'),
        ('mmass', 'mmass'),
        ('Origin', 'Origin'),
    ]
    ACQUISITION_CHOICES = [('local', 'local'), ('scan', 'scan')]

    #required fields
    run_date = models.DateField()

    #optional fields
    software_name = models.CharField(max_length=100, choices=SOFTWARE_CHOICES, null=True, blank=True)
    software_version = models.CharField(max_length=50, null=True, blank=True)
    type_acquisition = models.CharField(max_length=20, choices=ACQUISITION_CHOICES, null=True, blank=True)
    event_number = models.IntegerField(null=True, blank=True)
    tof_bin_width_ns = models.FloatField(null=True, blank=True)
    number_of_tof_bins = models.IntegerField(null=True, blank=True)

    file_acquisition_log = models.FileField(upload_to='acquisitions/logs/', null=True, blank=True)


class PreProcessingSpectra(models.Model):
    raw_spectrum_id = models.AutoField(primary_key=True)
    
    acquisition = models.ForeignKey(AcquisitionTOFSIMS, on_delete=models.CASCADE, related_name='pre_processings')

    DATA_TYPE_CHOICES = [('1D', '1D'), ('Map 2D', 'Map 2D')]
    FILTER_CHOICES = [
        ('ion_correlated', 'ion_correlated'),
        ('multiplicity_correlated', 'multiplicity_correlated'),
        ('position_detector_correlated', 'position_detector_correlated'),
    ]
    
    SOFTWARE_CHOICES = [
        ('slow control EVE', 'slow control EVE'),
        ('Narval', 'Narval'), ('C-Visu', 'C-Visu'),
        ('mmass', 'mmass'), ('Origin', 'Origin'),
    ]
    #required fields
    data_type = models.CharField(max_length=50, choices=DATA_TYPE_CHOICES)
    nb_impact = models.IntegerField()
    #optional fields
    software_name = models.CharField(max_length=100, choices=SOFTWARE_CHOICES, null=True, blank=True)
    software_version = models.CharField(max_length=50, null=True, blank=True)
    filtered_spectrum = models.CharField(max_length=100, choices=FILTER_CHOICES, null=True, blank=True)
    normalized_spectrum = models.CharField(max_length=100, null=True, blank=True)
    analyse_note = models.TextField(null=True, blank=True)
    
    file_acquisition_log = models.FileField(upload_to='acquisitions/logs/', null=True, blank=True)

class Spectra(models.Model):
    mz_spectra_id = models.AutoField(primary_key=True)

    pre_processing = models.OneToOneField(PreProcessingSpectra, on_delete=models.CASCADE, related_name='spectra')
    SOFTWARE_CHOICES = [
        ('slow control EVE', 'slow control EVE'),
        ('Narval', 'Narval'), ('C-Visu', 'C-Visu'),
        ('mmass', 'mmass'), ('Origin', 'Origin'),
    ]
    #required fields
    date_mz_spectra = models.DateField()
    expert_validation = models.BooleanField(default=False)
    file_tag = models.FileField(upload_to='spectra/tags/')
    #optional fields
    comment = models.TextField(null=True, blank=True)
    software_name = models.CharField(max_length=100, choices=SOFTWARE_CHOICES, null=True, blank=True)
    software_version = models.CharField(max_length=50, null=True, blank=True)
    
    file_peak_label = models.FileField(upload_to='spectra/peak_labels/', null=True, blank=True)
    file_peak_list = models.FileField(upload_to='spectra/peak_lists/', null=True, blank=True)
    file_result = models.FileField(upload_to='spectra/results/', null=True, blank=True)