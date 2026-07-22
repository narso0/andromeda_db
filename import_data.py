import os
import django
import pandas as pd


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromeda.settings')
django.setup()

from core.models import Laboratory, User, Sample, PrimaryBeam, Equipment, SpectrometerParameters, AcquisitionTOFSIMS
def run_import():
    file_name = 'Andromeda_Data.xlsx'
    print(f"Loading {file_name}...")
    df_labs = pd.read_excel(file_name, sheet_name='Laboratory')
    df_users = pd.read_excel(file_name, sheet_name='User')
    df_samples = pd.read_excel(file_name, sheet_name='Sample')
    #new imports
    df_beams = pd.read_excel(file_name, sheet_name='Primary Ion')
    df_equipments = pd.read_excel(file_name, sheet_name='Equipment')
    df_params = pd.read_excel(file_name, sheet_name='Spectrometer Parameter')
    df_acquisitions = pd.read_excel(file_name, sheet_name='Acquisition TOF-SIMS')
    print("Importing Laboratories...")
    for index, row in df_labs.iterrows():
        lab, created = Laboratory.objects.update_or_create(
            laboratory_id=int(row['laboratory_id']),
            defaults={
                'name_laboratory': str(row['name_laboratory']).strip(),
                'organization': str(row['organization']).strip() if pd.notna(row['organization']) else None,
                'organization_type': str(row['organization_type']).strip(),
                'country': str(row['country']).strip(),
            }
        )
        if created:
            print(f"  + Created new Lab: {lab.name_laboratory}")

    print("Importing Users...")
    for index, row in df_users.iterrows():
        lab_id = row['laboratory_id']
        try:
            parent_lab = Laboratory.objects.get(laboratory_id=lab_id)
        except Laboratory.DoesNotExist:
            print(f"Error: Lab ID {lab_id} not found for User {row['last_name']}")
            continue
        is_confidential = True if str(row['confidentiality']).strip().upper() == 'O' else False
        raw_date = row['submission_date']
        submission_date = pd.to_datetime(raw_date, errors='coerce')
        final_date = submission_date.date() if pd.notna(submission_date) else None

        user, created = User.objects.update_or_create(
            user_id=int(row['user_id']),
            defaults={
                'last_name': str(row['last_name']).strip(),
                'email': str(row['email']).strip() if pd.notna(row['email']) else None,
                'laboratory': parent_lab,
                'first_name': str(row['first_name']).strip() if pd.notna(row['first_name']) else None,
                'project_title': str(row['project_title']).strip(),
                'submission_date': final_date,
                'project_origin': str(row['project_origin']).strip(),
                'confidentiality': is_confidential,
                'file_proposal': None,
                'file_retex': None,
            }
        )
        if created:
            print(f"  + Created User: {user.first_name} {user.last_name}")

    print("Importing Samples...")
    for index, row in df_samples.iterrows():
        user_id = row['user_id']
        try:
            parent_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            print(f"Error: User ID {user_id} not found for sample {row['sample_code(user)']}")
            continue
        raw_prep_date = row['preparation_date']
        preparation_date = pd.to_datetime(raw_prep_date, errors='coerce')
        final_prep_date = preparation_date.date() if pd.notna(preparation_date) else None
        raw_reception_date = row['reception_date']
        reception_date = pd.to_datetime(raw_reception_date, errors='coerce')
        final_reception_date = reception_date.date() if pd.notna(reception_date) else None

        sample, created = Sample.objects.update_or_create(
            sample_id = int(row['sample_id']),
            defaults={
                'user': parent_user,
                'name_sample': str(row['name_sample']).strip() if pd.notna(row['name_sample']) else None,
                'sample_code': str(row['sample_code(user)']).strip() if pd.notna(row['sample_code(user)']) else None,
                'batch_id': str(row['batch_id(user)']).strip() if pd.notna(row['batch_id(user)']) else None,
                'type_sample': str(row['type_sample']).strip() if pd.notna(row['type_sample']) else None,
                'type_substrate': str(row['sample_substrate']).strip() if pd.notna(row['sample_substrate']) else None,
                'material_classification': str(row['material_classification']).strip() if pd.notna(row['material_classification']) else None,
                'description': str(row['description']).strip() if pd.notna(row['description']) else None,
                'preparation_date': final_prep_date,
                'reception_date': final_reception_date,
                'storage_conditions': str(row['storage_conditions']).strip() if pd.notna(row['storage_conditions']) else None,
                'file_sample': None,
            }
        )
        if created:
            print(f"  + Created Sample: {sample.name_sample}")


#normalization for liquid metals and tofsims
    ION_SOURCE_MODEL_TO_CATEGORY = {
        'LMIS AuGe': 'Liquid metal',
    }
    ANALYSER_TYPE_NORMALIZATION = {
        'TOF SIMS': 'TOF',
        'TOF': 'TOF',
    }
    print("Importing Primary Beams...")
    for index, row in df_beams.iterrows():
        if pd.isna(row['irradiation_id']): continue
        raw_source = str(row['ion_source_type']).strip() if pd.notna(row['ion_source_type']) else None
        source_category = ION_SOURCE_MODEL_TO_CATEGORY.get(raw_source)
        if raw_source and source_category is None:
            print(f"Unknown ion source '{raw_source}' on irradiation_id={row['irradiation_id']} -> leaving category blank, have to check with others later")
        PrimaryBeam.objects.update_or_create(
            irradiation_id=int(row['irradiation_id']),
            defaults={
                'irradiation_date': pd.to_datetime(row['irradiation_date']).date() if pd.notna(row['irradiation_date']) else None,
                'accelerator_name': str(row['accelerator_name']).strip() if pd.notna(row['accelerator_name']) else None,
                'ion_source_type': source_category,
                'source_model': raw_source,
                'primary_ion_species': str(row['primary_ion_species']).strip(),
                'energy_MeV': float(row['energy_MeV']) if pd.notna(row['energy_MeV']) else 0.0,
                'spot_size_um': float(row['spot_size_µm']) if pd.notna(row['spot_size_µm']) else 0.0,
                'pulse_beam_kV': float(row['pulse_beam_kv']) if pd.notna(row['pulse_beam_kv']) else 0.0,
                'repetition_rate_kHz': float(row['repetition_rate_kHz']) if pd.notna(row['repetition_rate_kHz']) else 0.0,
                'fluence_ions_cm2': float(row['fluence_ions_cm2']) if pd.notna(row['fluence_ions_cm2']) else None,
                'current_nA': float(row['current_nA']) if pd.notna(row['current_nA']) else None,
                'comments': str(row['comments']).strip() if pd.notna(row['comments']) else None,
            }
        )
    print("Importing Equipment...")
    for index, row in df_equipments.iterrows():
        raw_analyser = str(row['analyser_type']).strip()
        normalized_analyser = ANALYSER_TYPE_NORMALIZATION.get(raw_analyser)
        if normalized_analyser is None:
            print(f"Unknown analyser_type '{raw_analyser}' on equipment_id={row['equipment_id']} -> leaving blank, have to check with others")
        Equipment.objects.update_or_create(
            equipment_id=int(row['equipment_id']),
            defaults={
                'instrument_name': str(row['instrument_name']).strip() if pd.notna(row['instrument_name']) else None,
                'make': str(row['make']).strip() if pd.notna(row['make']) else None,
                'beam_incidence_angle': float(str(row['beam_incidence_angle']).replace('°', '').strip()) if pd.notna(row['beam_incidence_angle']) else None,
                'detector_type': str(row['detector_type']).strip() if pd.notna(row['detector_type']) else None,
                'detector_dead_time': str(row['detector_dead_time']).strip() if pd.notna(row['detector_dead_time']) else None,
                'supplementary_information': str(row['supplementary information']).strip() if pd.notna(row['supplementary information']) else None,
                'analyser_type': normalized_analyser,
                'reflectron_state': None,
            }
        )

    print("Importing Spectrometer Parameters...")
    for index, row in df_params.iterrows():
        if pd.isna(row['param_id']): continue
        SpectrometerParameters.objects.update_or_create(
            param_id=int(row['param_id']),
            defaults={
                'equipment_id': int(row['equipment_id']),
                'spectrometer_date': pd.to_datetime(row['spectrometer_date']).date() if pd.notna(row['spectrometer_date']) else None,
                'polarity': str(row['polarity']).strip(),
                'sample_bias_kV': float(row['sample_bias_kv']) if pd.notna(row['sample_bias_kv']) else 0.0,
                'detector_bias': float(row['detector_bias']) if pd.notna(row['detector_bias']) else 0.0,
                'lens_ext': float(row['lens_ext']) if pd.notna(row['lens_ext']) else 0.0,
                'lens_SI': float(row['lens_si']) if pd.notna(row['lens_si']) else 0.0,
                'name_position': str(row['name_position']).strip() if pd.notna(row['name_position']) else None,
                'analysis_area_um2': float(row['analysis_area_µm2']) if pd.notna(row['analysis_area_µm2']) else None,
                'comments': str(row['comments']).strip() if pd.notna(row['comments']) else None,
            }
        )

    print("Importing Acquisitions...")
    for index, row in df_acquisitions.iterrows():
        if pd.isna(row['run_id']): continue
        AcquisitionTOFSIMS.objects.update_or_create(
            run_id=str(row['run_id']).strip(),
            defaults={
                'sample_id': int(row['sample_id']),
                'primary_beam_id': int(row['irradiation_id']),
                'spectro_params_id': int(row['param_id']),
                'run_date': pd.to_datetime(row['run_date']).date() if pd.notna(row['run_date']) else None,
                'software_version': str(row['software_version']).strip() if pd.notna(row['software_version']) else None,
                'type_acquisition': str(row['type_acquisition']).strip() if pd.notna(row['type_acquisition']) else None,
                'event_number': int(row['event_number']) if pd.notna(row['event_number']) else None,
                'tof_bin_width_ns': float(row['tof_bin_width_ns']) if pd.notna(row['tof_bin_width_ns']) else None,
                'number_of_tof_bins': int(row['number_of_tof_bins']) if pd.notna(row['number_of_tof_bins']) else None,
            }
        )
    print("Full Database Import Complete!")




if __name__ == '__main__':
    run_import()