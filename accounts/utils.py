# import os
# import pandas as pd
# from django.core.management.base import BaseCommand
# from django.conf import settings
# from accounts.models import Supervisor
# from django.db import transaction


# class Command(BaseCommand):
#     help = "Imports supervisor data from a predefined Excel sheet"

#     def handle(self, *args, **kwargs):
#         file_path = os.path.join(
#             settings.BASE_DIR, "data", "supervisors.xlsx"
#         )  # Adjust the path
#         sheet_name = "LI (Oct24-Feb25)"  # Adjust sheet name if needed

#         if not os.path.exists(file_path):
#             self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
#             return

#         try:
#             df = pd.read_excel(
#                 file_path,
#                 sheet_name=sheet_name,
#                 header=None,
#                 skiprows=1,
#                 engine="openpyxl",
#             )
#             self.stdout.write(
#                 self.style.SUCCESS(f"Loaded sheet '{sheet_name}' from {file_path}")
#             )

#             lecturers = []
#             with transaction.atomic():
#                 for _, row in df.iterrows():
#                     name, phone, email, campus = (
#                         row[1],
#                         row[2],
#                         row[3],
#                         row[4],
#                     )  # Adjust indexes as needed
#                     lecturers.append(
#                         Supervisor(name=name, phone=phone, email=email, campus=campus)
#                     )

#                 Supervisor.objects.bulk_create(Supervisors)

#             self.stdout.write(
#                 self.style.SUCCESS(
#                     f"Successfully imported {len(lecturers)} supervisors."
#                 )
#             )

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Error importing sheet: {e}"))
