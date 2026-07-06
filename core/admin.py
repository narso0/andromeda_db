from django.contrib import admin
from .models import (
    Laboratory, User, Sample,
    Equipment, SpectrometerParameters,
    PrimaryBeam,
    AcquisitionTOFSIMS, PreProcessingSpectra, Spectra,
)

#inlines(shown nested inside their parent)
class SpectrometerParametersInline(admin.StackedInline):
    """All parameter sets that belong to one piece of Equipment."""
    model = SpectrometerParameters
    extra = 0
    show_change_link = True
    fields = (
        ('spectrometer_date', 'polarity'),
        ('lens_ext', 'lens_SI'),
        ('detector_bias', 'sample_bias_kV'),
        'name_position', 'analysis_area_um2',
        'comments', 'file_slowcontrol_log_txt',
    )

class PreProcessingInline(admin.TabularInline):
    """Pre-processing runs that came out of one Acquisition."""
    model = PreProcessingSpectra
    extra = 0
    show_change_link = True
    fields = ('data_type', 'nb_impact', 'software_name', 'filtered_spectrum', 'normalized_spectrum')

class SpectraInline(admin.StackedInline):
    """The one final Spectra record that came out of a PreProcessing."""
    model = Spectra
    extra = 0
    show_change_link = True
    fields = (
        ('date_mz_spectra', 'expert_validation'),
        ('software_name', 'software_version'),
        'comment',
        ('file_tag', 'file_peak_label', 'file_peak_list', 'file_result'),
    )

#admin classes
@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display  = ('laboratory_id', 'name_laboratory', 'organization_type', 'country')
    search_fields = ('name_laboratory', 'country')
    list_filter   = ('organization_type', 'country')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ('user_id', 'last_name', 'first_name', 'email', 'laboratory', 'project_origin', 'confidentiality')
    search_fields = ('last_name', 'first_name', 'email', 'project_title')
    list_filter   = ('project_origin', 'confidentiality', 'laboratory')
    raw_id_fields = ('laboratory',)

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display   = ('sample_id', 'name_sample', 'sample_code', 'material_classification', 'type_sample', 'reception_date', 'user')
    search_fields  = ('name_sample', 'sample_code', 'batch_id', 'description')
    list_filter    = ('material_classification', 'type_sample', 'type_substrate')
    date_hierarchy = 'reception_date'
    raw_id_fields  = ('user',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display  = ('equipment_id', 'instrument_name', 'make', 'analyser_type', 'detector_type')
    search_fields = ('instrument_name', 'make', 'detector_type')
    list_filter   = ('analyser_type',)
    inlines       = [SpectrometerParametersInline]

@admin.register(SpectrometerParameters)
class SpectrometerParametersAdmin(admin.ModelAdmin):
    list_display   = ('param_id', 'equipment', 'spectrometer_date', 'polarity', 'sample_bias_kV', 'detector_bias', 'lens_ext', 'lens_SI')
    search_fields  = ('equipment__instrument_name',)
    list_filter    = ('polarity', 'name_position', 'equipment')
    date_hierarchy = 'spectrometer_date'
    raw_id_fields  = ('equipment',)

@admin.register(PrimaryBeam)
class PrimaryBeamAdmin(admin.ModelAdmin):
    list_display   = ('irradiation_id', 'irradiation_date', 'primary_ion_species', 'energy_MeV', 'spot_size_um', 'pulse_beam_kV', 'repetition_rate_kHz')
    search_fields  = ('primary_ion_species', 'accelerator_name')
    list_filter    = ('primary_ion_species', 'ion_source_type', 'spot_size_um')
    date_hierarchy = 'irradiation_date'

@admin.register(AcquisitionTOFSIMS)
class AcquisitionTOFSIMSAdmin(admin.ModelAdmin):
    list_display   = ('run_id', 'run_date', 'sample', 'primary_beam', 'spectro_params', 'type_acquisition', 'software_name')
    search_fields  = ('sample__name_sample', 'sample__sample_code', 'primary_beam__primary_ion_species')
    list_filter    = ('type_acquisition', 'software_name')
    date_hierarchy = 'run_date'
    #raw_id_fields prevents huge dropdowns once you have hundreds of samples/beams
    raw_id_fields  = ('sample', 'primary_beam', 'spectro_params')
    inlines        = [PreProcessingInline]

@admin.register(PreProcessingSpectra)
class PreProcessingSpectraAdmin(admin.ModelAdmin):
    list_display  = ('raw_spectrum_id', 'acquisition', 'data_type', 'nb_impact', 'software_name', 'filtered_spectrum')
    search_fields = ('acquisition__sample__name_sample',)
    list_filter   = ('data_type', 'software_name', 'filtered_spectrum')
    raw_id_fields = ('acquisition',)
    inlines       = [SpectraInline]

@admin.register(Spectra)
class SpectraAdmin(admin.ModelAdmin):
    list_display   = ('mz_spectra_id', 'pre_processing', 'date_mz_spectra', 'expert_validation', 'software_name')
    search_fields  = ('pre_processing__acquisition__sample__name_sample',)
    list_filter    = ('expert_validation', 'software_name')
    date_hierarchy = 'date_mz_spectra'