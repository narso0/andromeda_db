import os
import django
import pandas as pd


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromeda.settings')
django.setup()

from core.models import Laboratory, User, Sample

def run_import():
    file_name = 'Andromeda_Data.xlsx'
    print(f"Loading {file_name}...")
    df_labs = pd.read_excel(file_name, sheet_name='Laboratory')
    df_users = pd.read_excel(file_name, sheet_name='User')
    df_samples = pd.read_excel(file_name, sheet_name='Sample')
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
        is_confidential = "O" if str(row['confidentiality']).strip().upper() == 'O' else "N"
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

    print("Import Complete!")



if __name__ == '__main__':
    run_import()