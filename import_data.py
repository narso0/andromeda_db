import os
import django
import pandas as pd

# Set up the environment to run as a Django script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromeda.settings')
django.setup()

from core.models import Laboratory, User

def run_import():
    file_name = 'Andromeda_Data.xlsx'
    print(f"Loading {file_name}...")
    df_labs = pd.read_excel(file_name, sheet_name='Laboratory')
    df_users = pd.read_excel(file_name, sheet_name='User')
    print("Importing Laboratories...")
    for index, row in df_labs.iterrows():
        lab, created = Laboratory.objects.update_or_create(
            laboratory_id=int(row['Laboratory_Id']),
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
            print(f"  [!] Error: Lab ID {lab_id} not found for User {row['last_name']}")
            continue
        is_confidential = True if str(row['confidentiality']).strip().upper() == 'O' else False
        raw_date = row['submission_date']
        # 'coerce' turns invalid dates (like 20222) into NaT (Not a Time) instead of crashing
        submission_date = pd.to_datetime(raw_date, errors='coerce')
        
        # If the result is NaT, set it to None, otherwise convert to datetime.date object
        final_date = submission_date.date() if pd.notna(submission_date) else None

        user, created = User.objects.update_or_create(
            last_name=str(row['last_name']).strip(),
            email=str(row['email']).strip() if pd.notna(row['email']) else None,
            defaults={
                'laboratory': parent_lab,
                'first_name': str(row['first_name']).strip() if pd.notna(row['first_name']) else None,
                'project_title': str(row['project_title']).strip(),
                'submission_date': final_date, # Use the clean 'final_date' here
                'project_origin': str(row['project_origin']).strip(),
                'confidentiality': is_confidential,
                'file_proposal': None,
            }
        )
        if created:
            print(f"  + Created User: {user.first_name} {user.last_name}")

    print("Import Complete!")

if __name__ == '__main__':
    run_import()