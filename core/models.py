from django.db import models

class Laboratory(models.Model):
    ORGANIZATION_CHOICES = [
        ('Internal Academic', 'Internal Academic'),
        ('External Academic', 'External Academic'),
        ('Industrial', 'Industrial'),
    ]
    laboratory_id = models.AutoField(primary_key=True)
    name_laboratory = models.CharField(max_length=150)
    organization = models.CharField(max_length=50, null=True, blank=True)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_CHOICES)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name_laboratory
    class Meta:
        verbose_name_plural = "Laboratories"
class User(models.Model):
    PROJECT_ORIGIN_CHOICES = [
        ('EMIR&A Call', 'EMIR&A Call'),
        ('Mosaic Proposal', 'Mosaic Proposal'),
        ('User Feasibility Study', 'User Feasibility Study'),
        ('Internal Research', 'Internal Research'),
    ]

    laboratory = models.ForeignKey(Laboratory, on_delete=models.RESTRICT, related_name='users')

    user_id = models.AutoField(primary_key=True)

    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    project_title = models.CharField(max_length=200)
    submission_date = models.DateField(null=True, blank=True)
    project_origin = models.CharField(max_length=50, choices=PROJECT_ORIGIN_CHOICES)
    confidentiality = models.BooleanField(default=False)

    file_proposal = models.FileField(upload_to='users/proposals/', null=True, blank=True)
    file_retex = models.FileField(upload_to='users/retex/', null=True, blank=True)


    def __str__(self):
        return f"{self.last_name} ({self.project_title})"

class Sample(models.Model):
    MATERIAL_CHOICES = [
        ('Ceramic', 'Ceramic'), ('Lipids', 'Lipids'), ('Metals', 'Metals'),
        ('Micrometeorite', 'Micrometeorite'), ('Minerals', 'Minerals'), 
        ('Organic', 'Organic'), ('Oxides', 'Oxides'), ('Polymers', 'Polymers'),
        ('Substrate', 'Substrate'), ('Thin organic films', 'Thin organic films'),
    ]

    TYPE_SAMPLE_CHOICES = [
        ('Sample', 'Sample'), ('Substrate', 'Substrate'), ('Standard', 'Standard'),
        ('Analogue', 'Analogue'),
    ]
    TYPE_SUBSTRATE_CHOICES = [
        ('Cuivre', 'Cuivre'), ('Aluminium', 'Aluminium'), ('Silicium', 'Silicium'),
        ('Gold', 'Gold'), ('ITO', 'ITO'), ('Carbon', 'Carbon'), ('Mylar', 'Mylar'),
        ('MgF2', 'MgF2'),
    ]
    sample_id = models.AutoField(primary_key=True)
    name_sample = models.CharField(max_length=200, null=True, blank=True)
    sample_code = models.CharField(max_length=100, null=True, blank=True)
    batch_id = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='samples')

    type_sample = models.CharField(max_length=100, choices=TYPE_SAMPLE_CHOICES, null=True, blank=True)
    type_substrate = models.CharField(max_length=100, choices=TYPE_SUBSTRATE_CHOICES, null=True, blank=True)

    material_classification = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
   
    description = models.TextField(null=True, blank=True)
    preparation_date = models.DateField(null=True, blank=True)

    reception_date = models.DateField()
    storage_conditions = models.CharField(max_length=200, null=True, blank=True)

    file_sample = models.FileField(upload_to='samples/pdfs/', null=True, blank=True)


    def __str__(self):
        if self.name_sample:
            return self.name_sample
        elif self.sample_code:
            return self.sample_code
        return f"Sample {self.sample_id}"

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
    #required fields
    irradiation_date = models.DateField()
    primary_ion_species = models.CharField(max_length=50, choices=PRIMARY_ION_CHOICES)
    energy_MeV = models.FloatField()
    spot_size_um = models.FloatField(choices=SPOT_SIZE_CHOICES)
    pulse_beam_kV = models.FloatField()
    repetition_rate_kHz = models.FloatField()
    
    #optional fields
    accelerator_name = models.CharField(max_length=100, null=True, blank=True)
    ion_source_type = models.CharField(max_length=100, choices=ION_SOURCE_CHOICES, null=True, blank=True)
    fluence_ions_cm2 = models.FloatField(null=True, blank=True)
    current_nA = models.FloatField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    file_accelerator_log = models.FileField(upload_to='beams/logs/', null=True, blank=True)
    def __str__(self):
        return f"Beam {self.primary_ion_species} on Sample {self.sample.sample_code} at ({self.irradiation_date})"

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

    #new optional fields
    make_spectrometer = models.CharField(max_length=100, null=True, blank=True)
    beam_incidence_angle = models.FloatField(null=True, blank=True)
    detector_type = models.CharField(max_length=100, null=True, blank=True)
    detector_dead_time = models.CharField(max_length=100, null=True, blank=True)
    supplementary_information = models.TextField(null=True, blank=True)

    file_slowcontrol_log_txt = models.FileField(upload_to='spectrometers/logs/', null=True, blank=True)
    spectrometer_metadata = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"Spectrometer {self.spectrometer_id} on {self.spectrometer_date}"


class AcquisitionTOFSIMS(models.Model):
    run_id = models.AutoField(primary_key=True)

    spectrometer = models.ForeignKey(Spectrometer, on_delete=models.CASCADE, related_name='acquisitions')
    SOFTWARE_CHOICES = [
        ('Slow Control EVE', 'Slow Control EVE'),
        ('Narval', 'Narval'),
        ('C-Visu', 'C-Visu'),
        ('Mmass', 'Mmass'),
        ('Origin', 'Origin'),
    ]
    ACQUISITION_CHOICES = [('Local', 'Local'), ('Scan', 'Scan')]

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
    class Meta:
        verbose_name = "Acquisition TOF-SIMS"
        verbose_name_plural = "Acquisitions TOF-SIMS"


class PreProcessingSpectra(models.Model):
    raw_spectrum_id = models.AutoField(primary_key=True)
    
    acquisition = models.ForeignKey(AcquisitionTOFSIMS, on_delete=models.CASCADE, related_name='pre_processings')

    DATA_TYPE_CHOICES = [('1D', '1D'), ('Map 2D', 'Map 2D')]
    FILTER_CHOICES = [
        ('Ion_Correlated', 'Ion_Correlated'),
        ('Multiplicity_Correlated', 'Multiplicity_Correlated'),
        ('Position_Detector_Correlated', 'Position_Detector_Correlated'),
    ]
    
    SOFTWARE_CHOICES = [
        ('Slow Control EVE', 'Slow Control EVE'),
        ('Narval', 'Narval'), ('C-Visu', 'C-Visu'),
        ('Mmass', 'Mmass'), ('Origin', 'Origin'),
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
    def __str__(self):
        return f"PreProcessing {self.raw_spectrum_id} ({self.data_type})"

class Spectra(models.Model):
    mz_spectra_id = models.AutoField(primary_key=True)

    pre_processing = models.OneToOneField(PreProcessingSpectra, on_delete=models.CASCADE, related_name='spectra')
    SOFTWARE_CHOICES = [
        ('Slow Control EVE', 'Slow Control EVE'),
        ('Narval', 'Narval'), ('C-Visu', 'C-Visu'),
        ('Mmass', 'Mmass'), ('Origin', 'Origin'),
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
    def __str__(self):
        return f"Spectra {self.mz_spectra_id} derived from PreProcess {self.pre_processing_id}"
    class Meta:
        verbose_name_plural = "Spectra"