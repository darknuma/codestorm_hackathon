# # from django.db import models
# from django.contrib.gis.db import models
# from helper.models import DateModel
# from django.core.validators import FileExtensionValidator
# from django.utils.translation import gettext_lazy as _
# from functools import partial
# from uuid import uuid4
# from django.utils import timezone


# def upload_directory_path(instance, filename, extra_arg1):
#     project = instance.project
#     now = timezone.now()
#     return '{0}/user_{1}/{2}/{3}'.format(extra_arg1,project,now, filename)

# #project defination.
# class Project(DateModel):
#     class TaskChoices(models.TextChoices):
#         Ongoing =  'Ongoing'
#         Completed = 'Completed'
#         Notstarted = 'Notstarted'
#     project_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     location = models.PolygonField()
#     name = models.TextField()
#     hectares = models.FloatField()
#     description = models.TextField(blank=True, null = True)
#     status = models.CharField(choices = TaskChoices.choices, max_length = 12)
#     user = models.ForeignKey('account.UserAccount', models.DO_NOTHING)
#     type = models.CharField( max_length = 12)
#     State = models.CharField(max_length=100,blank=True, null=True)
#     country = models.CharField(max_length=100,blank=True, null=True)
#     start_date = models.DateField()
#     end_date = models.DateField()

# class Trainning(DateModel):
#     training_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     location = models.PointField()
#     # class_type = models.CharField(choices = ClassChoices.get_choices(), max_length = 12,)
#     class_type=models.ForeignKey('Crop',on_delete=models.CASCADE)
#     class_value = models.IntegerField()
#     status = models.BooleanField(default = False)
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     training_date = models.DateTimeField()
#     user = models.ForeignKey('account.UserAccount', models.DO_NOTHING)

# class Carbon(DateModel):
#     carbon_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     # location = models.PolygonField()
#     year = models.IntegerField()
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     # class_type = models.CharField(choices = ClassChoices.get_choices(), max_length = 12)
#     class_type=models.ForeignKey('Crop',on_delete=models.CASCADE)
#     area = models.FloatField()

# class CarbonStats(DateModel):
#     stat_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     # location = models.PolygonField()
#     year1 = models.IntegerField()
#     year2 = models.IntegerField()
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     # class_type = models.CharField(choices = ClassChoices.get_choices(), max_length = 12)
#     class_type=models.ForeignKey('Crop',on_delete=models.CASCADE)
#     carbon = models.FloatField()

# class ClassificationMap(DateModel):
#     classification_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     image_url = models.URLField(max_length = 200)
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     season = models.OneToOneField('Season', on_delete=models.CASCADE)

# class ProjectMember(DateModel):
#     ROLES = (
#         ('Buyers', 'Buyers'),
#         ('Administrator', 'Administrator'),
#         ('Sample', 'Sample'),
#         ('Farmer', 'Farmer'),
#         ('Creater','Creater' )
#     )
#     member_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     user = models.ForeignKey('account.UserAccount', on_delete=models.CASCADE)
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLES)
#     telephone_number = models.CharField(
#         max_length=20,
#         blank=True,
#         null=True,
#         # validators=[
#         #     RegexValidator(
#         #         regex=r'^\+?1?\d{9,15}$',
#         #         message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
#         #     )
#         # ],
#         # help_text="Enter a valid telephone number with up to 15 digits."
#     )
#     _id = models.CharField(max_length=255, blank=True, null = True)

#     class Meta:
#         unique_together = ('user', 'project', 'role', '_id')  # Ensure a user can only be a member of a project once

#     def __str__(self):
#         return f"{self.user.username} - {self.project.name} - {self.get_role_display()}"

# # class FarmerProfile(DateModel):
# #     PROFILE_PICTURE = 'profile_pics/'
# #     IDENTIFICATION_PICTURE = 'identifications/'
# #     BVN_SLIP_PICTURE = 'bvn_slips/'

# #     GENDER_CHOICES = [
# #         ('M', 'Male'),
# #         ('F', 'Female'),
# #         ('O', 'Other'),
# #     ]

# #     MARITAL_STATUS_CHOICES = [
# #         ('S', 'Single'),
# #         ('M', 'Married'),
# #         ('D', 'Divorced'),
# #         ('W', 'Widowed'),
# #     ]

# #     IDENTIFICATION_TYPE_CHOICES = [
# #         ('passport', 'Passport'),
# #         ('national_id', 'National ID'),
# #         ('driver_license', 'Driver License'),
# #         ('other', 'Other'),
# #     ]

# #     FARMING_TYPE_CHOICES = [
# #         ('crop', 'Crop Farming'),
# #         ('livestock', 'Livestock Farming'),
# #         ('mixed', 'Mixed Farming'),
# #         ('other', 'Other'),
# #     ]
# #     farmerprofile_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
# #     project = models.ForeignKey('Project', on_delete=models.CASCADE)
# #     profile_pic = models.ImageField(upload_to=PROFILE_PICTURE, blank=True, null=True)
# #     first_name = models.CharField(max_length=100,blank=True, null=True)
# #     middle_name = models.CharField(max_length=100, blank=True, null=True)
# #     surname = models.CharField(max_length=100,blank=True, null=True)
# #     telephone = models.CharField(max_length=20,blank=True, null=True)
# #     email_address = models.EmailField(unique=True,blank=True, null=True)
# #     date_of_birth = models.DateField(blank=True, null=True)
# #     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
# #     marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES,blank=True, null=True)
# #     country = models.CharField(max_length=100,blank=True, null=True)
# #     state = models.CharField(max_length=100,blank=True, null=True)
# #     address = models.TextField(blank=True, null=True)
# #     amenity = models.CharField(max_length=255, blank=True, null=True)
# #     spoken_language = models.CharField(max_length=100,blank=True, null=True)

# #     kin_first_name = models.CharField(max_length=100,blank=True, null=True)
# #     kin_middle_name = models.CharField(max_length=100, blank=True, null=True)
# #     kin_surname = models.CharField(max_length=100,blank=True, null=True)
# #     kin_telephone = models.CharField(max_length=20,blank=True, null=True)
# #     kin_occupation = models.CharField(max_length=100,blank=True, null=True)
# #     kin_relationship = models.CharField(max_length=50,blank=True, null=True)

# #     level_of_education = models.CharField(max_length=100,blank=True, null=True)
# #     professional_experience = models.TextField(blank=True, null=True)
# #     years_experience = models.PositiveIntegerField(blank=True, null=True)
# #     type = models.CharField(max_length=100,blank=True, null=True)
# #     corporative_name = models.CharField(max_length=255,blank=True, null=True)
# #     bvn_slip = models.ImageField(upload_to=BVN_SLIP_PICTURE, blank=True, null=True)
# #     identification = models.ImageField(upload_to=IDENTIFICATION_PICTURE, blank=True, null=True)
# #     identification_type = models.CharField(max_length=50, choices=IDENTIFICATION_TYPE_CHOICES,blank=True, null=True)
# #     expiry_date = models.DateField(blank=True, null=True)
# #     issuance_date = models.DateField(blank=True, null=True)
# #     id_number = models.CharField(max_length=50,blank=True, null=True)

# #     bank_name = models.CharField(max_length=100,blank=True, null=True)
# #     account_number = models.CharField(max_length=50,blank=True, null=True)
# #     account_name = models.CharField(max_length=100,blank=True, null=True)

# #     farming_type = models.CharField(max_length=50, choices=FARMING_TYPE_CHOICES,blank=True, null=True)
# #     farm_location = models.CharField(max_length=255,blank=True, null=True)
# #     farm_size = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
# #     farm_owner = models.CharField(blank=True, null=True)
# #     owners_name = models.CharField(max_length=100, blank=True, null=True)
# #     owners_number = models.CharField(max_length=20, blank=True, null=True)
# #     crop_types = models.TextField(blank=True, null=True)
# #     lease_duration = models.PositiveIntegerField(blank=True, null=True)
# #     estimated_income = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)

# #     type_machine = models.CharField(max_length=100,blank=True, null=True)
# #     number_machines = models.PositiveIntegerField(blank=True, null=True)
# #     number_active_unit_machines = models.PositiveIntegerField(blank=True, null=True)
# #     number_inactive_unit_machines = models.PositiveIntegerField(blank=True, null=True)
# #     average_number_years_machines_use = models.PositiveIntegerField(blank=True, null=True)
# #     average_number_years_machines = models.PositiveIntegerField(blank=True, null=True)

# #     def __str__(self):
# #         return f"{self.first_name} {self.surname}"

# # class BusinessProfile(DateModel):
# #     BUSINESS_TYPE_CHOICES = [
# #         ('crop', 'Crop Farming'),
# #         ('livestock', 'Livestock Farming'),
# #         ('mixed', 'Mixed Farming'),
# #         ('other', 'Other'),
# #     ]

# #     MEANS_IDENTIFICATION_CHOICES = [
# #         ('passport', 'Passport'),
# #         ('national_id', 'National ID'),
# #         ('driver_license', 'Driver License'),
# #         ('other', 'Other'),
# #     ]

# #     TENOR_CHOICES = [
# #         ('short', 'Short Term'),
# #         ('medium', 'Medium Term'),
# #         ('long', 'Long Term'),
# #     ]

# #     businessprofile_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
# #     project = models.ForeignKey('Project', on_delete=models.CASCADE)
# #     business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES,blank=True, null=True)
# #     business_name = models.CharField(max_length=255,blank=True, null=True)
# #     means_identification = models.CharField(max_length=50, choices=MEANS_IDENTIFICATION_CHOICES,blank=True, null=True)
# #     phone_number = models.CharField(max_length=20,blank=True, null=True)
# #     email_address = models.EmailField(blank=True, null=True)
# #     age = models.PositiveIntegerField(blank=True, null=True)
# #     years_agric_experience = models.PositiveIntegerField(blank=True, null=True)
# #     agribusiness_location = models.CharField(max_length=255,blank=True, null=True)
# #     farm_size = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
# #     personal_guarantee = models.FileField(upload_to='personal_guarantee', blank=True, null=True)
# #     six_bank_statement = models.FileField(upload_to='bank_statements/', blank=True, null=True)
# #     # farm_location = models.CharField(max_length=255)

# #     director_name_1 = models.CharField(max_length=255,blank=True, null=True)
# #     director_number_1 = models.CharField(max_length=20,blank=True, null=True)
# #     valid_identification_1 = models.CharField(max_length=255,blank=True, null=True)
# #     director_name_2 = models.CharField(max_length=255, blank=True, null=True)
# #     director_number_2 = models.CharField(max_length=20, blank=True, null=True)
# #     valid_identification_2 = models.CharField(max_length=255,blank=True, null=True)
# #     government_identification = models.FileField(upload_to='government_ids/', blank=True, null=True)
# #     cac_02 = models.FileField(upload_to='cac_documents/', blank=True, null=True)
# #     cac_07 = models.FileField(upload_to='cac_documents/', blank=True, null=True)
# #     certificate_incorporation = models.FileField(upload_to='certificates/', blank=True, null=True)
# #     twelve_bank_statement_1 = models.FileField(upload_to='bank_statements/', blank=True, null=True)
# #     twelve_bank_statement_2 = models.FileField(upload_to='bank_statements/', blank=True, null=True)
# #     passport_photograph = models.ImageField(upload_to='passports/', blank=True, null=True)
# #     corporate_guarantee = models.FileField(upload_to='corporate_guarantee', blank=True, null=True)

# #     loan_amount = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
# #     tenor = models.CharField(max_length=50, choices=TENOR_CHOICES,blank=True, null=True)
# #     purpose_loan = models.TextField(blank=True, null=True)

# #     type = models.CharField(max_length=50,blank=True, null=True)
# #     firs_identification_number = models.CharField(max_length=100,blank=True, null=True)
# #     purchase_order = models.FileField(upload_to='purchase_orders/', blank=True, null=True)
# #     company_profile = models.FileField(upload_to='company_profiles/', blank=True, null=True)
# #     utility_bill = models.FileField(upload_to='utility_bills/', blank=True, null=True)
# #     equity_contribution = models.FileField(upload_to='equity_contribution/', blank=True, null=True)
# #     zowasel_domcmiciation_letter = models.FileField(upload_to='letters/', blank=True, null=True)
# #     board_resolution = models.FileField(upload_to='resolutions/', blank=True, null=True)
# #     cac_search_fee = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)

# #     def __str__(self):
# #         return self.business_name4

# class CropBaseline(DateModel):
#     cropbaseline_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     crop_name = models.CharField(max_length=255)
#     labour = models.IntegerField(default=0)
#     input = models.FloatField(default=0.0)
#     others = models.FloatField(blank=True, null = True)
#     crop_yield = models.FloatField(default=0.0)
#     price_crop_kg = models.FloatField(default=0.0)
#     crop_income = models.FloatField(default=0.0)
#     crop_area = models.FloatField(default=0.0)
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)

#     season = models.ForeignKey('Season', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.crop_name

# class Landrights(DateModel):
#     rights_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     allowed_extensions=['png','jpg','jpeg','pdf']
#     ownership = models.CharField( max_length = 100)
#     certificate = models.FileField( upload_to=partial(upload_directory_path,extra_arg1='certificate'),
#                                     validators=[FileExtensionValidator(allowed_extensions)],max_length=255,
#                                     verbose_name=_('certificate File'))
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)

# class FarmManagement(DateModel):
#     farm_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     weeding = models.BooleanField(default=False)
#     chemical_fertilizer_name = models.CharField(max_length=255,blank=True, null=True)
#     chemical_fertilizer_use = models.BooleanField(default=False)
#     chemical_fertilizer_composition = models.CharField(max_length=255,blank=True, null=True)
#     fungicide_name = models.CharField(max_length=255,blank=True, null=True)
#     insecticide_name = models.CharField(max_length=255,blank=True, null=True)
#     tillage = models.CharField(max_length=255,blank=True, null=True)
#     residual_matter = models.CharField(max_length=255,blank=True, null=True)
#     fertilisation = models.CharField(max_length=255,blank=True, null=True)
#     chemical_fertilizer_name = models.CharField(max_length=255,blank=True, null=True)
#     pesticide_name = models.CharField(max_length=255,blank=True, null=True)
#     herbicide_name = models.CharField(max_length=255,blank=True, null=True)
#     organic_matter_fertilisation = models.CharField(max_length=255, help_text='e.g., manure',blank=True, null=True)
#     residual_matter_management = models.CharField(max_length=255,blank=True, null=True)
#     use_of_irrigation_system = models.BooleanField(default=False)
#     how_often_irrigate = models.CharField(max_length=255,blank=True, null=True)
#     how_do_get_water = models.CharField(max_length=255,blank=True, null=True)
#     # year = models.IntegerField()
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     season = models.OneToOneField('Season', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Farm Management {self.farm_id}"

# class SoilSample(DateModel):
#     soil_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     soil_texture = models.CharField(max_length=255,blank=True, null=True)
#     soil_carbon = models.FloatField(default=0.0)
#     soil_organic_matter = models.FloatField(default=0.0)
#     soil_ph = models.FloatField(default=0.0)
#     ph_water = models.FloatField(default=0.0)
#     phosphorus_m3 = models.FloatField(default=0.0)
#     calcium = models.FloatField(default=0.0)
#     aluminum = models.FloatField(default=0.0)
#     moisture = models.FloatField(default=0.0)
#     nitrogen = models.FloatField(default=0.0)
#     potassium = models.FloatField(default=0.0)
#     magnesium = models.FloatField(default=0.0)
#     cation_exchange_capacity = models.FloatField(default=0.0)
#     total_iron = models.FloatField(default=0.0)
#     density = models.FloatField(default=0.0)
#     # year = models.IntegerField()
#     trainning = models.ForeignKey('Trainning', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Soil Sample {self.soil_id}"

# class Tree(DateModel):
#     trees_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     # tree_species_name = models.CharField(max_length=255)
#     number_of_trees = models.IntegerField()
#     average_height = models.FloatField(default=0.0)
#     average_dbh = models.FloatField(help_text="Diameter at Breast Height (DBH)")
#     average_age = models.IntegerField(default=0)
#     plant_type=models.ForeignKey('Plant',on_delete=models.CASCADE)
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     location = models.PointField()


#     def __str__(self):
#         return self.plant_type.common_name

# class EnergyUsage(DateModel):
#     energy_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     energy_source = models.CharField(max_length=255,blank=True, null=True)
#     volume_used = models.FloatField(default=0.0)
#     unit = models.CharField(max_length=255,blank=True, null=True)
#     # year = models.IntegerField()
#     # date = models.DateField()
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)
#     season = models.OneToOneField('Season', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.energy_source} on {self.updated_at}"

# class Season(DateModel):
#     season_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     year_from = models.DateField()
#     year_to = models.DateField()
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('year_from', 'year_to', 'project')

# class Crop(DateModel):
#     crop_id = models.BigAutoField(primary_key=True, editable=False)
#     crop_name = models.CharField(max_length=25, unique=True)
#     lue = models.FloatField()

# class Plant(DateModel):
#     plant_id = models.BigAutoField(primary_key=True, editable=False)
#     genus = models.CharField(max_length=100)
#     species = models.CharField(max_length=100, unique=True)
#     family = models.CharField(max_length=100)
#     common_name = models.CharField(max_length=100, null=True, blank=True)
#     local_name = models.CharField(max_length=100, null=True, blank=True)
#     a = models.DecimalField(max_digits=10, decimal_places=4)
#     b = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.genus} {self.species}"

#     class Meta:
#         unique_together = ('genus', 'species', 'family', 'common_name')

# class CropCarbon(models.Model):
#     season = models.ForeignKey('Season', on_delete=models.CASCADE)
#     fpar = models.FloatField()
#     ndvi = models.FloatField()
#     apar = models.FloatField()
#     gpp = models.FloatField()
#     class_type=models.ForeignKey('Crop',on_delete=models.CASCADE)
#     npp = models.FloatField()
#     area_sum = models.FloatField()
#     carbon_sequestration = models.FloatField()
#     carbon_sequestration_area = models.FloatField()

#     def __str__(self):
#         return f"Carbon {self.class_type.crop_name}"

#     class Meta:
#         unique_together = ('season', 'class_type')


"""
Consolidated Generator script to generate synthetic data for Nigerian farmers,
combining principles and features from helper_ds.py, helper_cl.py, and helper_gm.py.
This script aims to produce a comprehensive dataset for alternative credit scoring models
and general agricultural finance analysis.
Version 2: Incorporates statistical context from LSMS-ISA survey data.
MODIFIED: Added functions to generate Farmer_Profile, Farm_Enterprise, and Loan_Record CSVs.
"""

# import os
# import random
# import pandas as pd
# import numpy as np
# from faker import Faker
# from datetime import datetime # Added for date calculations
# from dateutil.relativedelta import relativedelta # Added for precise month calculations

# # --- Configuration & Constants ---
# NUM_FARMERS = 10000 # Reduced for faster testing, user can set back to 10000
# OUTPUT_DIR = 'data'
# OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'master_nigerian_farmer_data.csv')
# FARMER_PROFILE_FILENAME = os.path.join(OUTPUT_DIR, 'farmer_profile.csv')
# FARM_ENTERPRISE_FILENAME = os.path.join(OUTPUT_DIR, 'farm_enterprise.csv')
# LOAN_RECORD_FILENAME = os.path.join(OUTPUT_DIR, 'loan_record.csv')


# os.makedirs(OUTPUT_DIR, exist_ok=True)

# fake = Faker()
# Faker.seed(42)


# np.random.seed(42)
# random.seed(42)

# NIGERIAN_STATES = [
# 	'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno',
# 	'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo', 'Jigawa',
# 	'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger',
# 	'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe',
# 	'Zamfara', 'FCT',
# ]

# NIGERIAN_REGIONS = {
# 	'North Central': ['Benue', 'FCT', 'Kogi', 'Kwara', 'Nasarawa', 'Niger', 'Plateau'],
# 	'North East': ['Adamawa', 'Bauchi', 'Borno', 'Gombe', 'Taraba', 'Yobe'],
# 	'North West': ['Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Sokoto', 'Zamfara'],
# 	'South East': ['Abia', 'Anambra', 'Ebonyi', 'Enugu', 'Imo'],
# 	'South South': ['Akwa Ibom', 'Bayelsa', 'Cross River', 'Delta', 'Edo', 'Rivers'],
# 	'South West': ['Ekiti', 'Lagos', 'Ogun', 'Ondo', 'Osun', 'Oyo'],
# }

# STATE_TO_REGION = {state: region for region, states in NIGERIAN_REGIONS.items() for state in states}

# MAJOR_NATIONAL_CROPS = ['Maize', 'Cassava', 'Sorghum', 'Yam', 'Cowpea']

# CROPS_BY_REGION = {
# 	'North Central': ['Maize', 'Rice', 'Yam', 'Cassava', 'Sorghum', 'Millet', 'Cowpea', 'Soybean', 'Sesame', 'Beans'],
# 	'North East': ['Millet', 'Sorghum', 'Groundnut', 'Cowpea', 'Maize', 'Rice', 'Sesame', 'Beans'],
# 	'North West': ['Millet', 'Sorghum', 'Maize', 'Rice', 'Groundnut', 'Cotton', 'Cowpea', 'Tomato', 'Beans'],
# 	'South East': ['Cassava', 'Yam', 'Rice', 'Maize', 'Vegetables', 'Oil Palm', 'Cocoa', 'Beans'],
# 	'South South': ['Cassava', 'Yam', 'Plantain', 'Oil Palm', 'Cocoa', 'Rubber', 'Rice', 'Vegetables', 'Beans'],
# 	'South West': ['Cocoa', 'Cassava', 'Maize', 'Yam', 'Oil Palm', 'Vegetables', 'Cowpea', 'Plantain', 'Beans'],
# }
# for region, crops in CROPS_BY_REGION.items():
# 	if 'Sorghum' in crops and 'Guinea Corn' not in crops: # Ensure Guinea Corn is added if Sorghum exists
# 		crops.append('Guinea Corn')
# ALL_CROPS = sorted(list(set(crop for crops_list in CROPS_BY_REGION.values() for crop in crops_list)))

# FARM_SIZE_RANGES_HA = {
# 	'North Central': (0.3, 4), 'North East': (0.4, 5), 'North West': (0.4, 6),
# 	'South East': (0.1, 2.5), 'South South': (0.2, 3), 'South West': (0.2, 3.5),
# }

# EDUCATION_LEVELS_MAPPING = {
# 	'No Formal Education': 0, 'Primary Incomplete': 3, 'Primary Complete': 6,
# 	'Secondary Incomplete': 9, 'Secondary Complete': 12, 'OND/NCE': 14,
# 	'HND/BSc': 16, 'Masters/PhD': 18,
# }
# EDUCATION_CATEGORIES = list(EDUCATION_LEVELS_MAPPING.keys())
# MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']
# LIVESTOCK_TYPES = ['Poultry', 'Goats', 'Sheep', 'Cattle', 'Pigs', 'Fish Farming', 'Ducks', 'Guinea Fowl', 'None']

# LIVESTOCK_WEIGHTS_BY_REGION = {
#     'North Central': {'Poultry': 0.71, 'Goats': 0.69, 'Sheep': 0.18, 'Cattle': 0.41, 'Pigs': 0.1, 'Fish Farming': 0.02, 'Ducks': 0.07, 'Guinea Fowl': 0.01, 'None': 0.3},
#     'North East': {'Poultry': 0.44, 'Goats': 0.68, 'Sheep': 0.39, 'Cattle': 0.36, 'Pigs': 0.01, 'Fish Farming': 0.01, 'Ducks': 0.05, 'Guinea Fowl': 0.02, 'None': 0.3},
#     'North West': {'Poultry': 0.42, 'Goats': 0.72, 'Sheep': 0.56, 'Cattle': 0.48, 'Pigs': 0.01, 'Fish Farming': 0.01, 'Ducks': 0.03, 'Guinea Fowl': 0.05, 'None': 0.2},
#     'South East': {'Poultry': 0.65, 'Goats': 0.52, 'Sheep': 0.07, 'Cattle': 0.01, 'Pigs': 0.15, 'Fish Farming': 0.003, 'Ducks': 0.01, 'Guinea Fowl': 0.0, 'None': 0.4},
#     'South South': {'Poultry': 0.53, 'Goats': 0.55, 'Sheep': 0.02, 'Cattle': 0.0, 'Pigs': 0.1, 'Fish Farming': 0.073, 'Ducks': 0.01, 'Guinea Fowl': 0.01, 'None': 0.4},
#     'South West': {'Poultry': 0.58, 'Goats': 0.53, 'Sheep': 0.07, 'Cattle': 0.06, 'Pigs': 0.05, 'Fish Farming': 0.003, 'Ducks': 0.0, 'Guinea Fowl': 0.01, 'None': 0.4},
# }
# NATIONAL_LIVESTOCK_WEIGHTS = {
#     'Poultry': 0.54, 'Goats': 0.65, 'Sheep': 0.31, 'Cattle': 0.25, 'Pigs': 0.05,
#     'Fish Farming': 0.02, 'Ducks': 0.03, 'Guinea Fowl': 0.02, 'None': 0.53,
# }
# PRIMARY_LIVESTOCK_USES = ['Sold Alive', 'Savings/Insurance', 'Food for the Family', 'Crop Agriculture', 'Sale of Livestock Products', 'Social Status/Prestige', 'Transport']
# LIVESTOCK_USE_WEIGHTS = [0.621, 0.207, 0.164, 0.098, 0.091, 0.010, 0.014]

# LAND_OWNERSHIP_STATUSES = ['Inherited', 'Family Owned', 'Purchased', 'Leased', 'Community Land', 'Rented', 'Gift']
# LAND_ACQUISITION_METHODS = ['Inheritance', 'Purchase', 'Lease', 'Gift', 'Community Grant', 'Family Allocation', 'Rental']
# PEST_DISEASE_CONTROL_METHODS = ['Modern Chemical', 'Organic', 'Traditional', 'Integrated Pest Management', 'None']
# UTILITY_PAYMENT_TIMELINESS_CATS = ['Excellent', 'Good', 'Fair', 'Poor']
# MOBILE_MONEY_USAGE_CATS = ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
# SOCIAL_MEDIA_USAGE_CATS = ['None', 'Low', 'Medium', 'High']
# YIELD_CONSISTENCY_CATS = ['High', 'Medium', 'Low', 'Very Low']
# LOAN_PRODUCTS_PLATFORM = ['Input Loan', 'Mechanization Loan', 'Bundled Services Loan']
# LOAN_PURPOSES_GENERAL = ['Working Capital', 'Asset Acquisition', 'Land Expansion', 'Processing Equipment', 'Storage Construction']
# PRIOR_LOAN_REPAYMENT_HISTORY_CATS = ['None', 'Poor', 'Fair', 'Good', 'Excellent']

# BASE_YIELDS_TONS_PER_HA = {
#     'Maize': 2.5, 'Rice': 2.8, 'Yam': 10.0, 'Cassava': 15.0, 'Sorghum': 2.0, 'Millet': 1.8,
#     'Cowpea': 1.0, 'Beans': 1.0, 'Groundnut': 1.2, 'Cotton': 1.5, 'Vegetables': 18.0,
#     'Oil Palm': 5.0, 'Plantain': 12.0, 'Cocoa': 0.7, 'Rubber': 1.5, 'Soybean': 1.5,
#     'Sesame': 0.8, 'Tomato': 20.0, 'Guinea Corn': 2.0,
# }
# CROP_PRICES_NAIRA_PER_TON = {
#     'Maize': 200000, 'Rice': 350000, 'Yam': 280000, 'Cassava': 120000, 'Sorghum': 190000,
#     'Millet': 180000, 'Cowpea': 400000, 'Beans': 400000, 'Groundnut': 450000, 'Cotton': 550000,
#     'Vegetables': 320000, 'Oil Palm': 500000, 'Plantain': 220000, 'Cocoa': 1500000,
#     'Rubber': 700000, 'Soybean': 380000, 'Sesame': 600000, 'Tomato': 250000, 'Guinea Corn': 190000,
# }
# BASE_COST_PER_HA = {crop: price * 0.50 for crop, price in CROP_PRICES_NAIRA_PER_TON.items()}

# # --- Helper Functions ---
# def weighted_choice(choices_weights):
#     choices, weights = zip(*choices_weights)
#     total_weight = sum(weights)
#     if not np.isclose(total_weight, 1.0) and total_weight > 0: # Added total_weight > 0 check
#         weights = [w / total_weight for w in weights]
#     elif total_weight == 0: # Handle case where all weights are zero
#         return random.choice(choices)
#     return random.choices(choices, weights=weights, k=1)[0]


# # --- Data Generation Functions (Adapted & Updated) ---
# def calculate_yield_tons_per_ha(row):
# 	base = BASE_YIELDS_TONS_PER_HA.get(row['primary_crop'], 1.0)
# 	education_factor = {
# 		'No Formal Education': 0.8, 'Primary Incomplete': 0.85, 'Primary Complete': 0.9,
# 		'Secondary Incomplete': 0.95, 'Secondary Complete': 1.0, 'OND/NCE': 1.1,
# 		'HND/BSc': 1.15, 'Masters/PhD': 1.2,
# 	}.get(row['education_category'], 1.0)

# 	modern_practices_factor = 1.0
# 	if row['uses_improved_seeds']: modern_practices_factor += 0.15
# 	if row['uses_fertilizer']: modern_practices_factor += 0.20
# 	if row['uses_irrigation']: modern_practices_factor += 0.35
# 	if row['pest_disease_control_method'] in ['Modern Chemical', 'Integrated Pest Management']: modern_practices_factor += 0.10
# 	if row['uses_extension_services']: modern_practices_factor += 0.05

# 	experience_factor = min(1.0 + (row['farming_experience_years'] * 0.015), 1.25)
# 	random_factor = random.uniform(0.70, 1.30)
# 	return round(base * education_factor * modern_practices_factor * experience_factor * random_factor, 2)

# def calculate_annual_farm_expenses_ngn(row):
# 	base_cost = BASE_COST_PER_HA.get(row['primary_crop'], 100000) * row['farm_size_ha']
# 	if row['uses_improved_seeds']: base_cost *= 1.15
# 	if row['uses_fertilizer']: base_cost *= 1.20
# 	if row['uses_irrigation']: base_cost *= 1.30
# 	labor_factor = 1.0
# 	if row['farm_size_ha'] > 2.0: labor_factor += 0.1
# 	if row['gender'] == 'Female' and row['farm_size_ha'] > 1.0: labor_factor += 0.05
# 	base_cost *= labor_factor
# 	return round(base_cost * random.uniform(0.80, 1.20), -3)

# def generate_off_farm_income_ngn(row):
# 	if row['has_off_farm_income']:
# 		education_base = {
# 			'No Formal Education': 80000, 'Primary Incomplete': 100000, 'Primary Complete': 150000,
# 			'Secondary Incomplete': 200000, 'Secondary Complete': 300000, 'OND/NCE': 400000,
# 			'HND/BSc': 500000, 'Masters/PhD': 700000,
# 		}.get(row['education_category'], 100000)
# 		return round(education_base * random.uniform(0.6, 1.4), -3)
# 	return 0

# def generate_prior_loan_details(row):
# 	if row['has_prior_loan']:
# 		potential_revenue = row['annual_farm_revenue_ngn']
# 		loan_amount = min(potential_revenue * random.uniform(0.10, 0.35), 200000 + (row['farm_size_ha'] * 60000))
# 		loan_amount = round(max(20000, loan_amount), -3)
# 		base_repayment_prob = 0.60
# 		if row['education_category'] in ['Secondary Complete', 'OND/NCE', 'HND/BSc', 'Masters/PhD']: base_repayment_prob += 0.1
# 		if row['cooperative_member']: base_repayment_prob += 0.07
# 		if row['has_off_farm_income']: base_repayment_prob += 0.08
# 		if row['farm_profit_ngn'] > loan_amount * 0.5: base_repayment_prob += 0.1
# 		repayment_prob = min(base_repayment_prob, 0.90)
# 		actual_repayment_rate = random.uniform(max(0.20, repayment_prob - 0.30), min(1.0, repayment_prob + 0.1))
# 		repayment_history = 'Poor'
# 		if actual_repayment_rate >= 0.95: repayment_history = 'Excellent'
# 		elif actual_repayment_rate >= 0.80: repayment_history = 'Good'
# 		elif actual_repayment_rate >= 0.55: repayment_history = 'Fair'
# 		return pd.Series({
# 			'prior_loan_amount_ngn': loan_amount,
# 			'prior_loan_repayment_rate': round(actual_repayment_rate, 2),
# 			'prior_loan_repayment_history': repayment_history,
# 			'prior_loan_purpose': random.choice(LOAN_PURPOSES_GENERAL + LOAN_PRODUCTS_PLATFORM),
# 		})
# 	return pd.Series({
# 		'prior_loan_amount_ngn': 0, 'prior_loan_repayment_rate': 0,
# 		'prior_loan_repayment_history': 'None', 'prior_loan_purpose': 'N/A',
# 	})

# def calculate_credit_score(row):
#     score = 350
#     edu_points = {'No Formal Education': 0, 'Primary Incomplete': 10, 'Primary Complete': 20, 'Secondary Incomplete': 30, 'Secondary Complete': 50, 'OND/NCE': 60, 'HND/BSc': 70, 'Masters/PhD': 80}
#     score += edu_points.get(row['education_category'], 0)
#     if row['has_bank_account']: score += 35
#     if row['has_formal_id']: score += 25
#     if row['mobile_money_usage_frequency'] not in ['Never', 'Rarely']: score += 20
#     score += min(row['farming_experience_years'] * 3, 30)
#     if row['has_off_farm_income']: score += 50
#     if row['yield_consistency_rating'] == 'High': score += 20
#     elif row['yield_consistency_rating'] == 'Medium': score += 10
#     elif row['yield_consistency_rating'] == 'Low': score -= 10
#     score += (row['utility_bill_payment_score_1_10'] - 1) * 4
#     score += (row['mobile_money_activity_score_1_10'] - 1) * 3
#     if row['phone_bill_timeliness'] == 'Excellent': score += 15
#     elif row['phone_bill_timeliness'] == 'Good': score += 8
#     land_pts = {'Inherited': 25, 'Family Owned': 30, 'Purchased': 40, 'Leased': 15, 'Community Land': 10, 'Rented': 5, 'Gift': 20}
#     score += land_pts.get(row['land_acquisition_method'], 10)
#     if row['has_land_title']: score += 25
#     if row['has_prior_loan']:
#         history_pts = {'Excellent': 70, 'Good': 40, 'Fair': -10, 'Poor': -70, 'None': 0}
#         score += history_pts.get(row['prior_loan_repayment_history'], 0)
#         score += int((row['prior_loan_repayment_rate'] - 0.6) * 100)
#     if row['cooperative_member']: score += 40
#     if row['uses_extension_services']: score += 15
#     if row['uses_improved_seeds']: score += 10
#     if row['uses_fertilizer']: score += 10
#     if row['uses_irrigation']: score += 15
#     if row['has_weather_insurance']: score += 35
#     if row['has_storage_facility']: score += 15
#     if row['smartphone_owner']: score += 20
#     score += (row['digital_footprint_score_1_10'] - 1) * 2
#     if row['value_chain_platform_registered'] and row['years_on_platform'] > 0: score += 30
#     profit_margin = row['farm_profit_ngn'] / max(row['annual_farm_revenue_ngn'], 1)
#     if profit_margin > 0.30: score += 35
#     elif profit_margin > 0.15: score += 20
#     elif profit_margin > 0.0: score += 5
#     else: score -= 30
#     if row['owns_tractor']: score += 25
#     if row['owns_plow']: score += 15
#     if row['owns_sprayer']: score += 10
#     return max(300, min(850, int(score)))

# def determine_creditworthiness_category(score):
#     if score >= 700: return 'Excellent'
#     elif score >= 660: return 'Very Good'
#     elif score >= 620: return 'Good'
#     elif score >= 560: return 'Fair'
#     elif score >= 480: return 'Poor'
#     else: return 'Very Poor'

# def calculate_max_recommended_loan_ngn(row):
#     multiplier = 0.05
#     if row['credit_score'] >= 700: multiplier = 0.7
#     elif row['credit_score'] >= 660: multiplier = 0.55
#     elif row['credit_score'] >= 620: multiplier = 0.4
#     elif row['credit_score'] >= 560: multiplier = 0.25
#     elif row['credit_score'] >= 480: multiplier = 0.15
#     base_amount = row['total_annual_income_ngn'] * multiplier
#     profit_factor = (min(1.0 + (row['farm_profit_ngn'] / max(row['total_annual_income_ngn'], 1)) * 0.5, 1.5) if row['farm_profit_ngn'] > 0 else 0.5)
#     max_loan = base_amount * profit_factor * random.uniform(0.80, 1.20)
#     return round(max(10000, max_loan), -3)

# def determine_suitable_loan_products(row):
#     products = []
#     if row['credit_score'] >= 480: products.append('Microfinance Starter')
#     if row['credit_score'] >= 560: products.append('Input Finance')
#     if row['credit_score'] >= 620 and row['farm_size_ha'] >= 0.5: products.append('Equipment Loan (Small)')
#     if row['credit_score'] >= 620: products.append('Working Capital')
#     if row['credit_score'] >= 660 and row['farming_experience_years'] >= 4: products.append('Land Expansion Loan')
#     if row['credit_score'] >= 660 and row['total_annual_income_ngn'] >= 600000: products.append('Processing Equipment Loan')
#     if row['farm_size_ha'] >= 0.8 and row['credit_score'] >= 560: products.append('Crop Insurance Partnership')
#     if row['smartphone_owner'] and row['digital_footprint_score_1_10'] >= 3: products.append('Digital Finance Solutions')
#     return ', '.join(sorted(list(set(products)))) if products else 'Not Currently Eligible'

# def calculate_predicted_default_probability(row):
#     base_risk = 0.40
#     credit_factor = 1.0 - ((row['credit_score'] - 300) / 550)
#     income_stability_factor = 0.75 if row['has_off_farm_income'] else 1.0
#     experience_factor = max(0.70, 1.0 - (row['farming_experience_years'] * 0.02))
#     modern_practices_factor = 1.0
#     if row['uses_improved_seeds']: modern_practices_factor -= 0.05
#     if row['uses_fertilizer']: modern_practices_factor -= 0.05
#     if row['uses_irrigation']: modern_practices_factor -= 0.10
#     if row['has_weather_insurance']: modern_practices_factor -= 0.15
#     social_factor = 0.80 if row['cooperative_member'] else 1.0
#     social_factor = social_factor * 0.95 if row['uses_extension_services'] else social_factor
#     prior_history_factor = 1.0
#     if row['has_prior_loan']:
#         history_map = {'Excellent': 0.65, 'Good': 0.80, 'Fair': 1.05, 'Poor': 1.35, 'None': 1.0}
#         prior_history_factor = history_map.get(row['prior_loan_repayment_history'], 1.0)
#     loan_to_income_ratio = row['loan_amount_requested_ngn'] / max(row['total_annual_income_ngn'], 1)
#     capacity_factor = 1.0 + min(max(0, loan_to_income_ratio - 0.25) * 2.5, 0.6)
#     default_prob = (base_risk * credit_factor * income_stability_factor * experience_factor * modern_practices_factor * social_factor * prior_history_factor * capacity_factor)
#     default_prob = default_prob * random.uniform(0.75, 1.25)
#     return round(max(0.02, min(0.98, default_prob)), 4)
# # --- End of Placeholder for original data generation functions ---


# # --- Main Data Generation Loop (from original script) ---
# all_farmer_data = []
# for i in range(NUM_FARMERS):
#     farmer_id = f'NGF{i + 1:06d}'
#     age = random.randint(16, 65)

#     possible_education_levels = []
#     if age < 18:
#         possible_education_levels = [('No Formal Education', 0.4), ('Primary Incomplete', 0.3), ('Primary Complete', 0.2), ('Secondary Incomplete', 0.1)]
#     elif age < 22:
#         possible_education_levels = [('No Formal Education', 0.20), ('Primary Incomplete', 0.10), ('Primary Complete', 0.20), ('Secondary Incomplete', 0.20), ('Secondary Complete', 0.25), ('OND/NCE', 0.05)]
#     elif age < 25:
#         possible_education_levels = [('No Formal Education', 0.15), ('Primary Incomplete', 0.10), ('Primary Complete', 0.15), ('Secondary Incomplete', 0.15), ('Secondary Complete', 0.25), ('OND/NCE', 0.15), ('HND/BSc', 0.05)]
#     else:
#         possible_education_levels = [('No Formal Education', 0.25), ('Primary Incomplete', 0.15), ('Primary Complete', 0.25), ('Secondary Incomplete', 0.10), ('Secondary Complete', 0.18), ('OND/NCE', 0.04), ('HND/BSc', 0.02), ('Masters/PhD', 0.01)]

#     max_possible_edu_years = age - 6
#     filtered_education_choices = []
#     for edu_cat, weight in possible_education_levels:
#         if EDUCATION_LEVELS_MAPPING[edu_cat] <= max_possible_edu_years:
#             filtered_education_choices.append((edu_cat, weight))

#     if not filtered_education_choices:
#         education_category = 'No Formal Education'
#     else:
#         education_category = weighted_choice(filtered_education_choices)
#     education_level_years = EDUCATION_LEVELS_MAPPING[education_category]
#     gender = random.choices(['Male', 'Female'], weights=[0.75, 0.25])[0]

#     if age < 18: marital_status_weights = [('Single', 0.95), ('Married', 0.05), ('Divorced', 0.00), ('Widowed', 0.00)]
#     elif age < 22: marital_status_weights = [('Single', 0.60), ('Married', 0.38), ('Divorced', 0.01), ('Widowed', 0.01)]
#     elif age < 30: marital_status_weights = [('Single', 0.25), ('Married', 0.70), ('Divorced', 0.02), ('Widowed', 0.03)]
#     else: marital_status_weights = [('Single', 0.05), ('Married', 0.75), ('Divorced', 0.05), ('Widowed', 0.15)]
#     marital_status = weighted_choice(marital_status_weights)

#     household_size = 1
#     if marital_status == 'Single':
#         if age < 22: household_size = random.randint(1, 3)
#         elif age < 30: household_size = random.randint(1, 5)
#         else: household_size = random.randint(1, 4)
#     elif marital_status == 'Married':
#         min_hh_size = 2
#         if age < 22: household_size = random.randint(min_hh_size, min_hh_size + 2)
#         elif age < 30: household_size = random.randint(min_hh_size, min_hh_size + 4)
#         else: household_size = random.randint(min_hh_size, 14)
#     elif marital_status == 'Widowed':
#         if age < 30: household_size = random.randint(1, 3)
#         else: household_size = random.randint(1, 10)
#     elif marital_status == 'Divorced':
#         if age < 30: household_size = random.randint(1, 4)
#         else: household_size = random.randint(1, 8)
#     household_size = max(1, household_size)

#     state = random.choice(NIGERIAN_STATES)
#     region = STATE_TO_REGION[state]
#     has_off_farm_income = random.choices([True, False], weights=[0.45, 0.55])[0]
#     farming_experience_years = max(1, min(age - 16, random.randint(1, 45)))
#     farm_size_min, farm_size_max = FARM_SIZE_RANGES_HA[region]
#     farm_size_ha = round(farm_size_min + (farm_size_max - farm_size_min) * (random.random() ** 2.5), 2)
#     farm_size_ha = round(max(0.05, farm_size_ha), 2)

#     regional_crops = CROPS_BY_REGION.get(region, ALL_CROPS)
#     crop_weights = [3 if crop in MAJOR_NATIONAL_CROPS else 1 for crop in regional_crops]
#     primary_crop = random.choices(regional_crops, weights=crop_weights, k=1)[0] if regional_crops else 'Unknown' # Handle empty regional_crops

#     secondary_crop_options = [c for c in regional_crops if c != primary_crop] + ['None'] if regional_crops else ['None']
#     secondary_crop = random.choice(secondary_crop_options) if secondary_crop_options else 'None'

#     owns_livestock = random.choices([True, False], weights=[0.47, 0.53])[0]
#     livestock_type = 'None'
#     primary_livestock_use = 'N/A'
#     if owns_livestock:
#         region_weights = LIVESTOCK_WEIGHTS_BY_REGION.get(region, NATIONAL_LIVESTOCK_WEIGHTS)
#         livestock_type = weighted_choice(list(region_weights.items()))
#         if livestock_type != 'None':
#             primary_livestock_use = weighted_choice(list(zip(PRIMARY_LIVESTOCK_USES, LIVESTOCK_USE_WEIGHTS)))
#         else: owns_livestock = False

#     # Farm practices reflecting national averages
#     uses_fertilizer = random.choices([True, False], weights=[0.354, 1 - 0.354])[0]
#     uses_improved_seeds = random.choices([True, False], weights=[0.101, 1 - 0.101])[0]
#     uses_irrigation = random.choices([True, False], weights=[0.022, 1 - 0.022])[0]

#     # Adjusted input use slightly based on gender context
#     if gender == 'Female': uses_fertilizer = uses_fertilizer if random.random() < 0.9 else False
#     else: uses_fertilizer = uses_fertilizer if random.random() < 1.1 else True

#     pest_disease_control_method = random.choice(PEST_DISEASE_CONTROL_METHODS)
#     soil_type_known = random.choices([True, False], weights=[0.5, 0.5])[0]
#     yield_consistency_rating = random.choice(YIELD_CONSISTENCY_CATS)
#     post_harvest_loss_perc = round(random.uniform(5, 45), 2)
#     has_storage_facility = random.choices([True, False], weights=[0.35, 0.65])[0]
#     has_weather_insurance = random.choices([True, False], weights=[0.05, 0.95])[0]

#     # Land Tenure
#     land_acquisition_method = weighted_choice([('Inheritance', 0.65), ('Family Allocation', 0.15), ('Purchase', 0.08), ('Lease', 0.05), ('Rental', 0.03), ('Community Grant', 0.02), ('Gift', 0.02)])

#     has_land_title = False
#     if land_acquisition_method == 'Purchase': has_land_title = random.choices([True, False], weights=[0.20, 0.80])[0]
#     else: has_land_title = random.choices([True, False], weights=[0.05, 0.95])[0]

# 	# Agricultural Assets Ownership (Based on Table 6.21)
#     owns_tractor = random.choices([True, False], weights=[0.001, 0.999])[0]
#     owns_plow = random.choices([True, False], weights=[0.051, 1 - 0.051])[0]
#     owns_sprayer = random.choices([True, False], weights=[0.142, 1 - 0.142])[0]
#     owns_wheelbarrow = random.choices([True, False], weights=[0.233, 1 - 0.233])[0]
#     owns_cutlass = random.choices([True, False], weights=[0.904, 1 - 0.904])[0]
#     owns_sickle = random.choices([True, False], weights=[0.325, 1 - 0.325])[0]

#     # Extension Services
#     uses_extension_services = random.choices([True, False], weights=[0.207, 1 - 0.207])[0]

#     # Financial Inclustion & Digital Footprint
#     has_bank_account = random.choices([True, False], weights=[0.55, 0.45])[0]
#     has_formal_id = random.choices([True, False], weights=[0.65, 0.35])[0]
#     smartphone_owner = random.choices([True, False], weights=[0.60, 0.40])[0]
#     mobile_money_usage_frequency = 'Never'
#     if smartphone_owner: mobile_money_usage_frequency = weighted_choice([('Daily', 0.10), ('Weekly', 0.30), ('Monthly', 0.35), ('Rarely', 0.20), ('Never', 0.05)])
#     monthly_mobile_spend_naira = random.randint(300, 6000) if smartphone_owner else random.randint(100, 1200)
#     social_media_usage = random.choice(SOCIAL_MEDIA_USAGE_CATS) if smartphone_owner else 'None'
#     ecommerce_activity = random.choices([True, False], weights=[0.15, 0.85])[0] if smartphone_owner else False
#     active_on_agri_forums = random.choices([True, False], weights=[0.15, 0.85])[0] if smartphone_owner else False
#     digital_footprint_score_1_10 = random.randint(1, 10)

#     # Alternate payment data
#     utility_bill_payment_score_1_10 = random.randint(1, 10)
#     mobile_money_activity_score_1_10 = random.randint(1, 10) if mobile_money_usage_frequency != 'Never' else 1
#     utility_payment_timeliness = random.choice(UTILITY_PAYMENT_TIMELINESS_CATS)
#     rent_payment_timeliness = random.choice(UTILITY_PAYMENT_TIMELINESS_CATS + ['N/A']) if land_acquisition_method in ['Lease', 'Rental'] else 'N/A'
#     phone_bill_timeliness = random.choice(UTILITY_PAYMENT_TIMELINESS_CATS)
#     last_utility_payment_date = fake.date_between(start_date='-100d', end_date='today')
#     last_rent_payment_date = fake.date_between(start_date='-70d', end_date='today') if rent_payment_timeliness != 'N/A' else None

#     # Value Chain Platform
#     value_chain_platform_registered = random.choices([True, False], weights=[0.25, 0.75])[0]
#     years_on_platform = 0
#     marketplace_sales_ngn_last_year = 0
#     if value_chain_platform_registered:
#         years_on_platform = random.randint(0, 4)
#         if years_on_platform > 0: marketplace_sales_ngn_last_year = random.uniform(0.1, 0.6)

#     # Cooperative
#     cooperative_member = random.choices([True, False], weights=[0.40, 0.60])[0]
#     cooperative_repayment_rate_percent = random.randint(60, 100) if cooperative_member else 0

#     # Distances
#     distance_to_market_km = round(random.uniform(0.5, 70), 1)
#     distance_to_bank_km = round(random.uniform(1, 100), 1) if has_bank_account else round(random.uniform(10, 150), 1)

#     # --- Calculations requiring generated data ---
#     temp_row_for_calc = {
#         'primary_crop': primary_crop, 'education_category': education_category,
#         'uses_improved_seeds': uses_improved_seeds, 'uses_fertilizer': uses_fertilizer,
#         'uses_irrigation': uses_irrigation, 'farming_experience_years': farming_experience_years,
#         'farm_size_ha': farm_size_ha, 'pest_disease_control_method': pest_disease_control_method,
#         'has_off_farm_income': has_off_farm_income, 'cooperative_member': cooperative_member,
#         'gender': gender, 'uses_extension_services': uses_extension_services,
#     }
#     annual_farm_yield_tons_per_ha = calculate_yield_tons_per_ha(temp_row_for_calc)
#     total_production_tons = round(farm_size_ha * annual_farm_yield_tons_per_ha, 2)
#     crop_price_per_ton = CROP_PRICES_NAIRA_PER_TON.get(primary_crop, 150000)
#     annual_farm_revenue_ngn = round(total_production_tons * crop_price_per_ton, -3)
#     annual_farm_expenses_ngn = calculate_annual_farm_expenses_ngn(temp_row_for_calc)
#     farm_profit_ngn = annual_farm_revenue_ngn - annual_farm_expenses_ngn
#     annual_off_farm_income_ngn = generate_off_farm_income_ngn(temp_row_for_calc)
#     total_annual_income_ngn = annual_farm_revenue_ngn + annual_off_farm_income_ngn # Corrected: farm revenue + off-farm income
#     income_per_capita_ngn = round(total_annual_income_ngn / max(1, household_size), 0)

#     if value_chain_platform_registered and years_on_platform > 0:
#         marketplace_sales_ngn_last_year = round(marketplace_sales_ngn_last_year * annual_farm_revenue_ngn, -3)
#     else: marketplace_sales_ngn_last_year = 0

#     # Crop Disposition Estimation (Simplified based on Table 6.12 averages)
#     crop_disposition = {'Stored': 0.40, 'Sold Unprocessed': 0.25, 'Sold Processed': 0.05, 'Consumed': 0.25, 'Given Out': 0.04, 'Lost': 0.01}
#     if primary_crop == 'Cassava':
#         crop_disposition = {
# 			'Stored': 0.10,
# 			'Sold Unprocessed': 0.28,
# 			'Sold Processed': 0.17,
# 			'Consumed': 0.36,
# 			'Given Out': 0.06,
# 			'Lost': 0.005,
# 		}
#     elif primary_crop == 'Yam':
#         crop_disposition = {
# 			'Stored': 0.41,
# 			'Sold Unprocessed': 0.20,
# 			'Sold Processed': 0.01,
# 			'Consumed': 0.31,
# 			'Given Out': 0.05,
# 			'Lost': 0.01,
# 		}
#     elif primary_crop == 'Maize':
#         crop_disposition = {
# 			'Stored': 0.41,
# 			'Sold Unprocessed': 0.25,
# 			'Sold Processed': 0.00,
# 			'Consumed': 0.24,
# 			'Given Out': 0.05,
# 			'Lost': 0.003,
# 		}
#     elif primary_crop in ['Sorghum', 'Millet', 'Guinea Corn']:
#         crop_disposition = {
# 			'Stored': 0.66,
# 			'Sold Unprocessed': 0.07,
# 			'Sold Processed': 0.00,
# 			'Consumed': 0.19,
# 			'Given Out': 0.04,
# 			'Lost': 0.001,
# 		}
#     elif primary_crop == 'Rice':
#         crop_disposition = {
# 			'Stored': 0.56,
# 			'Sold Unprocessed': 0.27,
# 			'Sold Processed': 0.01,
# 			'Consumed': 0.10,
# 			'Given Out': 0.03,
# 			'Lost': 0.001,
# 		}
#     elif primary_crop == 'Groundnut':
#         crop_disposition = {
# 			'Stored': 0.54,
# 			'Sold Unprocessed': 0.32,
# 			'Sold Processed': 0.01,
# 			'Consumed': 0.09,
# 			'Given Out': 0.03,
# 			'Lost': 0.001,
# 		}
#     elif primary_crop in ['Cowpea', 'Beans']:
#         crop_disposition = {
# 			'Stored': 0.47,
# 			'Sold Unprocessed': 0.22,
# 			'Sold Processed': 0.01,
# 			'Consumed': 0.24,
# 			'Given Out': 0.03,
# 			'Lost': 0.001,
# 		}

#     percentage_sold_unprocessed = round(crop_disposition['Sold Unprocessed'] * 100 * random.uniform(0.8, 1.2), 1)
#     percentage_consumed = round(crop_disposition['Consumed'] * 100 * random.uniform(0.8, 1.2), 1)

#     # Prior Loan (using calculated revenues)
#     has_prior_loan = random.choices([True, False], weights=[0.25, 0.75])[0]
#     prior_loan_data = generate_prior_loan_details({
#         **temp_row_for_calc, 'has_prior_loan': has_prior_loan,
#         'annual_farm_revenue_ngn': annual_farm_revenue_ngn, 'farm_profit_ngn': farm_profit_ngn,
#     })

#     # Current Loan request
#     requests_loan_now = random.choices([True, False], weights=[0.5, 0.5])[0]
#     # Request amount based on need/capacity, maybe related to expenses or desired investment
#     loan_amount_requested_ngn = 0
#     current_loan_purpose = 'N/A'
#     current_loan_tenure_months = 0
#     if requests_loan_now:
#         max_sensible_request = max(annual_farm_expenses_ngn * 0.8, total_annual_income_ngn * 0.5)
#         loan_amount_requested_ngn = round(random.uniform(20000, max(50000, max_sensible_request * 1.5)) / 5000, 0) * 5000
#         if value_chain_platform_registered and random.random() < 0.7: current_loan_purpose = random.choice(LOAN_PRODUCTS_PLATFORM)
#         else: current_loan_purpose = random.choice(LOAN_PRODUCTS_PLATFORM + LOAN_PURPOSES_GENERAL)
#         current_loan_tenure_months = random.choice([3, 6, 9, 12, 18, 24])

#     # Full row for credit score and other final calculations
#     full_row_for_scoring = {
#         'education_category': education_category, 'has_bank_account': has_bank_account, 'has_formal_id': has_formal_id,
#         'mobile_money_usage_frequency': mobile_money_usage_frequency, 'farming_experience_years': farming_experience_years,
#         'has_off_farm_income': has_off_farm_income, 'yield_consistency_rating': yield_consistency_rating,
#         'utility_bill_payment_score_1_10': utility_bill_payment_score_1_10,
#         'mobile_money_activity_score_1_10': mobile_money_activity_score_1_10,
#         'phone_bill_timeliness': phone_bill_timeliness, 'land_acquisition_method': land_acquisition_method,
#         'has_land_title': has_land_title, 'has_prior_loan': has_prior_loan,
#         'prior_loan_repayment_history': prior_loan_data['prior_loan_repayment_history'],
#         'prior_loan_repayment_rate': prior_loan_data['prior_loan_repayment_rate'],
#         'cooperative_member': cooperative_member, 'uses_improved_seeds': uses_improved_seeds,
#         'uses_fertilizer': uses_fertilizer, 'uses_irrigation': uses_irrigation,
#         'has_weather_insurance': has_weather_insurance, 'has_storage_facility': has_storage_facility,
#         'smartphone_owner': smartphone_owner, 'digital_footprint_score_1_10': digital_footprint_score_1_10,
#         'value_chain_platform_registered': value_chain_platform_registered, 'years_on_platform': years_on_platform,
#         'farm_profit_ngn': farm_profit_ngn, 'annual_farm_revenue_ngn': annual_farm_revenue_ngn,
#         'total_annual_income_ngn': total_annual_income_ngn, 'loan_amount_requested_ngn': loan_amount_requested_ngn,
#         'uses_extension_services': uses_extension_services, 'owns_tractor': owns_tractor,
#         'owns_plow': owns_plow, 'owns_sprayer': owns_sprayer,
#     }
#     credit_score = calculate_credit_score(full_row_for_scoring)
#     full_row_for_scoring['credit_score'] = credit_score
#     creditworthiness_category = determine_creditworthiness_category(credit_score)
#     max_recommended_loan_ngn = calculate_max_recommended_loan_ngn(full_row_for_scoring)
#     suitable_loan_products = determine_suitable_loan_products({**full_row_for_scoring, 'farm_size_ha': farm_size_ha})
#     predicted_default_prob = 0.0
#     predicted_loan_repayment_outcome = 'N/A'

#     # Assign outcome based on probability bands
#     if requests_loan_now:
#         predicted_default_prob = calculate_predicted_default_probability(full_row_for_scoring)
#         if predicted_default_prob < 0.12: predicted_loan_repayment_outcome = 'Likely Full Repayment'
#         elif predicted_default_prob < 0.30: predicted_loan_repayment_outcome = 'Likely Partial Repayment'
#         elif predicted_default_prob < 0.55: predicted_loan_repayment_outcome = 'High Risk of Default'
#         else: predicted_loan_repayment_outcome = 'Very High Risk of Default'

#     farm_size_category = pd.cut([farm_size_ha], bins=[0, 1, 5, 10, float('inf')], labels=['Subsistence (<1ha)', 'Small (1-5ha)', 'Medium (5-10ha)', 'Large (>10ha)'], right=False)[0]

#     all_farmer_data.append({
#         'farmer_id': farmer_id, 'age': age, 'gender': gender, 'education_category': education_category,
#         'education_level_years': education_level_years, 'marital_status': marital_status,
#         'household_size': household_size, 'state': state, 'region': region,
#         'has_off_farm_income': has_off_farm_income, 'annual_off_farm_income_ngn': annual_off_farm_income_ngn,
#         'farming_experience_years': farming_experience_years, 'farm_size_ha': farm_size_ha,
#         'farm_size_category': farm_size_category, 'land_acquisition_method': land_acquisition_method,
#         'has_land_title': has_land_title, 'primary_crop': primary_crop, 'secondary_crop': secondary_crop,
#         'owns_livestock': owns_livestock, 'livestock_type': livestock_type,
#         'primary_livestock_use': primary_livestock_use, 'uses_improved_seeds': uses_improved_seeds,
#         'uses_fertilizer': uses_fertilizer, 'uses_irrigation': uses_irrigation,
#         'pest_disease_control_method': pest_disease_control_method, 'soil_type_known': soil_type_known,
#         'uses_extension_services': uses_extension_services,
#         'annual_farm_yield_tons_per_ha': annual_farm_yield_tons_per_ha,
#         'total_production_tons': total_production_tons, 'crop_price_per_ton_ngn': crop_price_per_ton,
#         'annual_farm_revenue_ngn': annual_farm_revenue_ngn, 'annual_farm_expenses_ngn': annual_farm_expenses_ngn,
#         'farm_profit_ngn': farm_profit_ngn, 'total_annual_income_ngn': total_annual_income_ngn,
#         'income_per_capita_ngn': income_per_capita_ngn, 'yield_consistency_rating': yield_consistency_rating,
#         'post_harvest_loss_perc': post_harvest_loss_perc,
#         'percentage_sold_unprocessed': percentage_sold_unprocessed,
#         'percentage_consumed': percentage_consumed, 'has_storage_facility': has_storage_facility,
#         'has_weather_insurance': has_weather_insurance, 'owns_tractor': owns_tractor,
#         'owns_plow': owns_plow, 'owns_sprayer': owns_sprayer, 'owns_wheelbarrow': owns_wheelbarrow,
#         'owns_cutlass': owns_cutlass, 'owns_sickle': owns_sickle, 'has_bank_account': has_bank_account,
#         'has_formal_id': has_formal_id, 'smartphone_owner': smartphone_owner,
#         'mobile_money_usage_frequency': mobile_money_usage_frequency,
#         'monthly_mobile_spend_naira': monthly_mobile_spend_naira, 'social_media_usage': social_media_usage,
#         'ecommerce_activity': ecommerce_activity, 'active_on_agri_forums': active_on_agri_forums,
#         'digital_footprint_score_1_10': digital_footprint_score_1_10,
#         'utility_bill_payment_score_1_10': utility_bill_payment_score_1_10,
#         'mobile_money_activity_score_1_10': mobile_money_activity_score_1_10,
#         'utility_payment_timeliness': utility_payment_timeliness,
#         'rent_payment_timeliness': rent_payment_timeliness, 'phone_bill_timeliness': phone_bill_timeliness,
#         'last_utility_payment_date': last_utility_payment_date,
#         'last_rent_payment_date': last_rent_payment_date, 'cooperative_member': cooperative_member,
#         'cooperative_repayment_rate_percent': cooperative_repayment_rate_percent,
#         'value_chain_platform_registered': value_chain_platform_registered,
#         'years_on_platform': years_on_platform,
#         'marketplace_sales_ngn_last_year': marketplace_sales_ngn_last_year,
#         'distance_to_market_km': distance_to_market_km, 'distance_to_bank_km': distance_to_bank_km,
#         'has_prior_loan': has_prior_loan,
#         'prior_loan_amount_ngn': prior_loan_data['prior_loan_amount_ngn'],
#         'prior_loan_repayment_rate': prior_loan_data['prior_loan_repayment_rate'],
#         'prior_loan_repayment_history': prior_loan_data['prior_loan_repayment_history'],
#         'prior_loan_purpose': prior_loan_data['prior_loan_purpose'],
#         'requests_loan_now': requests_loan_now,
#         'loan_amount_requested_ngn': loan_amount_requested_ngn,
#         'current_loan_purpose': current_loan_purpose,
#         'current_loan_tenure_months': current_loan_tenure_months, 'credit_score': credit_score,
#         'creditworthiness_category': creditworthiness_category,
#         'max_recommended_loan_ngn': max_recommended_loan_ngn,
#         'suitable_loan_products': suitable_loan_products,
#         'predicted_default_probability_current_loan': predicted_default_prob if requests_loan_now else 0.0,
#         'predicted_loan_repayment_outcome': predicted_loan_repayment_outcome if requests_loan_now else 'N/A',
#     })

# df_master = pd.DataFrame(all_farmer_data)

# # --- Post-Generation Analysis & Output ---
# print(f'Generated master dataset with {len(df_master)} farmers.')
# df_master.to_csv(OUTPUT_FILENAME, index=False)
# print(f'Master data saved to {OUTPUT_FILENAME}')


# # --- NEW FUNCTIONS TO CREATE STAR SCHEMA TABLES ---

# def create_farmer_profile_table(df_master_data):
#     """Creates the Farmer_Profile dimension table."""
#     df_farmer_profile = pd.DataFrame()
#     df_farmer_profile['Farmer_ID'] = df_master_data['farmer_id']
#     df_farmer_profile['Age'] = df_master_data['age']
#     df_farmer_profile['Gender'] = df_master_data['gender']
#     df_farmer_profile['Education_Category'] = df_master_data['education_category']
#     df_farmer_profile['Education_Level_Years'] = df_master_data['education_level_years']
#     df_farmer_profile['Marital_Status'] = df_master_data['marital_status']
#     df_farmer_profile['Household_Size'] = df_master_data['household_size']
#     df_farmer_profile['Off_Farm_Income_NGN'] = df_master_data['annual_off_farm_income_ngn']
#     df_farmer_profile['Region'] = df_master_data['region']
#     df_farmer_profile['State'] = df_master_data['state']
#     df_farmer_profile['Has_Bank_Account'] = df_master_data['has_bank_account']
#     df_farmer_profile['Has_Formal_ID'] = df_master_data['has_formal_id']
#     df_farmer_profile['Smartphone_Owner'] = df_master_data['smartphone_owner']
#     return df_farmer_profile

# def create_farm_enterprise_table(df_master_data):
#     """Creates the Farm_Enterprise dimension table."""
#     farm_enterprises = []
#     enterprise_id_counter = 1
#     for _, row in df_master_data.iterrows():
#         farmer_id = row['farmer_id']
#         # Enterprise 1: Primary Crop
#         enterprise_1_id = f"E{enterprise_id_counter:07d}"
#         enterprise_id_counter += 1

#         equipment_type = 'Unknown'
#         if row['owns_tractor']: equipment_type = 'Modern'
#         elif row['owns_plow'] or row['owns_sprayer']: equipment_type = 'Integrated'
#         elif row['owns_cutlass'] or row['owns_sickle']: equipment_type = 'Traditional'

#         value_of_farm_assets = (row['farm_size_ha'] * 300000) + \
#                                (5000000 if row['owns_tractor'] else 0) + \
#                                (200000 if row['owns_plow'] else 0) + \
#                                (50000 if row['owns_sprayer'] else 0)

#         farm_enterprises.append({
#             'Enterprise_ID': enterprise_1_id,
#             'Farmer_ID': farmer_id,
#             'Enterprise_Type': 'Crop',
#             'Primary_Crop': row['primary_crop'],
#             'Secondary_Crop': row['secondary_crop'] if row['secondary_crop'] != 'None' else None,
#             'Farm_Size_Ha': row['farm_size_ha'],
#             'Farm_Size_Category': row['farm_size_category'],
#             'Farming_Experience_Years': row['farming_experience_years'],
#             'Farming_Equipment_Type': equipment_type,
#             'Uses_Irrigation': row['uses_irrigation'],
#             'Depends_on_Rain': not row['uses_irrigation'],
#             'Uses_Fertilizer': row['uses_fertilizer'],
#             'Uses_Improved_Seeds': row['uses_improved_seeds'],
#             'Yield_per_Hectare_Tons': row['annual_farm_yield_tons_per_ha'],
#             'Profit_NGN': row['farm_profit_ngn'], # Attributed to primary crop enterprise
#             'Monthly_Income_NGN': round(row['annual_farm_revenue_ngn'] / 12, 0) if row['annual_farm_revenue_ngn'] else 0,
#             'Monthly_Expense_NGN': round(row['annual_farm_expenses_ngn'] / 12, 0) if row['annual_farm_expenses_ngn'] else 0,
#             'Value_of_Farm_Assets_NGN': round(value_of_farm_assets, 0),
#             'Total_Operating_Expenditure_NGN': row['annual_farm_expenses_ngn'],
#             'Farm_Income_NGN': row['annual_farm_revenue_ngn']
#         })

#         # Enterprise 2: Livestock (if applicable)
#         if row['owns_livestock'] and row['livestock_type'] != 'None':
#             enterprise_2_id = f"E{enterprise_id_counter:07d}"
#             enterprise_id_counter += 1
#             farm_enterprises.append({
#                 'Enterprise_ID': enterprise_2_id,
#                 'Farmer_ID': farmer_id,
#                 'Enterprise_Type': row['livestock_type'], # More specific type
#                 'Primary_Crop': None,
#                 'Secondary_Crop': None,
#                 'Farm_Size_Ha': 0, # Number of livestock not available, setting size to 0 for this enterprise
#                 'Farm_Size_Category': None,
#                 'Farming_Experience_Years': row['farming_experience_years'], # General experience
#                 'Farming_Equipment_Type': 'N/A', # Assuming equipment is for crop
#                 'Uses_Irrigation': False, # Typically not for livestock in this context
#                 'Depends_on_Rain': True,
#                 'Uses_Fertilizer': False,
#                 'Uses_Improved_Seeds': False, # For livestock breeding, not seeds
#                 'Yield_per_Hectare_Tons': 0,
#                 'Profit_NGN': 0, # Simplified: livestock profit not separately calculated
#                 'Monthly_Income_NGN': 0,
#                 'Monthly_Expense_NGN': 0,
#                 'Value_of_Farm_Assets_NGN': round(value_of_farm_assets,0), # Farmer's total assets
#                 'Total_Operating_Expenditure_NGN': 0,
#                 'Farm_Income_NGN': 0
#             })
#     return pd.DataFrame(farm_enterprises)

# def create_loan_record_table(df_master_data, df_farm_enterprise, fake_instance):
#     """Creates the Loan_Record fact table."""
#     loan_records = []
#     loan_id_counter = 1

#     # Create a mapping for quick Farmer_ID -> first Enterprise_ID lookup
#     # This assumes loans are primarily for the first listed (crop) enterprise
#     farmer_to_first_enterprise = df_farm_enterprise.drop_duplicates(subset=['Farmer_ID'], keep='first')
#     farmer_to_first_enterprise = farmer_to_first_enterprise.set_index('Farmer_ID')['Enterprise_ID'].to_dict()
#     farmer_enterprise_details = df_farm_enterprise.set_index('Enterprise_ID')


#     for _, row in df_master_data.iterrows():
#         farmer_id = row['farmer_id']
#         enterprise_id = farmer_to_first_enterprise.get(farmer_id)

#         if not enterprise_id: # Should not happen if all farmers have at least one enterprise
#             continue

#         # Get details for the linked enterprise
#         current_enterprise_details = farmer_enterprise_details.loc[enterprise_id]
#         enterprise_value_assets = current_enterprise_details['Value_of_Farm_Assets_NGN']
#         enterprise_op_ex = current_enterprise_details['Total_Operating_Expenditure_NGN']
#         enterprise_income = current_enterprise_details['Farm_Income_NGN']


#         # Prior Loan
#         if row['has_prior_loan'] and row['prior_loan_amount_ngn'] > 0:
#             loan_id = f"L{loan_id_counter:08d}"
#             loan_id_counter += 1

#             duration_months = random.randint(6, 36)
#             loan_date_obj = fake_instance.date_between(start_date='-3y', end_date='-3m')
#             repayment_date_obj = loan_date_obj + relativedelta(months=duration_months)

#             credit_worthy_status = 'Non-creditworthy'
#             if row['prior_loan_repayment_history'] in ['Excellent', 'Good']:
#                 credit_worthy_status = 'Creditworthy'

#             loan_asset_ratio = (row['prior_loan_amount_ngn'] / enterprise_value_assets) if enterprise_value_assets > 0 else 0
#             op_ex_income_ratio = (enterprise_op_ex / enterprise_income) if enterprise_income > 0 else 0

#             has_defaulted = row['prior_loan_repayment_history'] == 'Poor'
#             default_reason = random.choice(['Market Loss', 'Low Yield', 'Illness', 'Diversion of Funds']) if has_defaulted else None

#             loan_source = random.choice(['Bank', 'Cooperative', 'BOA', 'Informal Lender', 'Microfinance'])
#             if row['cooperative_member'] and random.random() < 0.6: # Higher chance for cooperative
#                 loan_source = 'Cooperative'

#             loan_records.append({
#                 'Loan_ID': loan_id,
#                 'Farmer_ID': farmer_id,
#                 'Enterprise_ID': enterprise_id,
#                 'Loan_Amount_Naira': row['prior_loan_amount_ngn'],
#                 'Interest_Rate_Annual': round(random.uniform(0.12, 0.40), 2), # Annual interest rate
#                 'Loan_Date': loan_date_obj.strftime('%Y-%m-%d'),
#                 'Loan_Use_Status_As_Intended': random.choice([True, False]),
#                 'Loan_Repayment_Amount_Naira': round(row['prior_loan_amount_ngn'] * row['prior_loan_repayment_rate'],0),
#                 'Repayment_Date': repayment_date_obj.strftime('%Y-%m-%d'),
#                 'Duration_Months': duration_months,
#                 'Loan_Use_Duration_Months': round(duration_months * random.uniform(0.8, 1.0)),
#                 'Credit_Worthiness_Status': credit_worthy_status,
#                 'Loan_Asset_Ratio': round(loan_asset_ratio, 4),
#                 'OpEx_Income_Ratio': round(op_ex_income_ratio, 4),
#                 'Loan_Source': loan_source,
#                 'Loan_Supervision_Frequency_Visits': random.randint(0, 4),
#                 'Distance_to_Lender_km': row['distance_to_bank_km'], # Simplification
#                 'Disbursement_Lag_Months': random.randint(0, 3),
#                 'Has_Defaulted': has_defaulted,
#                 'Default_Reason': default_reason
#             })

#         # Current Loan Request
#         if row['requests_loan_now'] and row['loan_amount_requested_ngn'] > 0:
#             loan_id = f"L{loan_id_counter:08d}"
#             loan_id_counter += 1

#             loan_date_obj = fake_instance.date_this_year(before_today=True, after_today=False)
#             # Ensure loan_date_obj is a date object if it's not already (fake can sometimes return string)
#             if isinstance(loan_date_obj, str):
#                 loan_date_obj = datetime.strptime(loan_date_obj, '%Y-%m-%d').date()

#             repayment_date_obj = loan_date_obj + relativedelta(months=row['current_loan_tenure_months'])

#             loan_asset_ratio = (row['loan_amount_requested_ngn'] / enterprise_value_assets) if enterprise_value_assets > 0 else 0
#             op_ex_income_ratio = (enterprise_op_ex / enterprise_income) if enterprise_income > 0 else 0

#             # Predicted default for current loan
#             has_defaulted_predicted = row['predicted_default_probability_current_loan'] > 0.4 # Threshold for prediction
#             default_reason_predicted = random.choice(['Predicted Market Loss', 'Predicted Low Yield', 'Predicted Illness']) if has_defaulted_predicted else None

#             loan_source = random.choice(['Bank', 'Cooperative', 'BOA', 'Fintech Platform', 'Microfinance'])
#             if row['value_chain_platform_registered'] and random.random() < 0.5:
#                  loan_source = 'Fintech Platform' # Higher chance if on platform

#             loan_records.append({
#                 'Loan_ID': loan_id,
#                 'Farmer_ID': farmer_id,
#                 'Enterprise_ID': enterprise_id,
#                 'Loan_Amount_Naira': row['loan_amount_requested_ngn'],
#                 'Interest_Rate_Annual': round(random.uniform(0.10, 0.35), 2),
#                 'Loan_Date': loan_date_obj.strftime('%Y-%m-%d'),
#                 'Loan_Use_Status_As_Intended': None, # Not yet used
#                 'Loan_Repayment_Amount_Naira': 0, # Not yet repaid
#                 'Repayment_Date': repayment_date_obj.strftime('%Y-%m-%d'),
#                 'Duration_Months': row['current_loan_tenure_months'],
#                 'Loan_Use_Duration_Months': 0, # Not yet used
#                 'Credit_Worthiness_Status': row['creditworthiness_category'],
#                 'Loan_Asset_Ratio': round(loan_asset_ratio, 4),
#                 'OpEx_Income_Ratio': round(op_ex_income_ratio, 4),
#                 'Loan_Source': loan_source,
#                 'Loan_Supervision_Frequency_Visits': 0, # New loan
#                 'Distance_to_Lender_km': row['distance_to_bank_km'],
#                 'Disbursement_Lag_Months': random.randint(0, 2), # Typically shorter for new platforms
#                 'Has_Defaulted': has_defaulted_predicted, # This is a prediction for current loan
#                 'Default_Reason': default_reason_predicted
#             })
#     return pd.DataFrame(loan_records)


# # --- Generate and Save Tables ---
# if __name__ == '__main__':
#     # 1. Create Farmer Profile Table
#     df_farmer_profile = create_farmer_profile_table(df_master)
#     df_farmer_profile.to_csv(FARMER_PROFILE_FILENAME, index=False)
#     print(f'Farmer Profile data saved to {FARMER_PROFILE_FILENAME}')

#     # 2. Create Farm Enterprise Table
#     df_farm_enterprise = create_farm_enterprise_table(df_master)
#     df_farm_enterprise.to_csv(FARM_ENTERPRISE_FILENAME, index=False)
#     print(f'Farm Enterprise data saved to {FARM_ENTERPRISE_FILENAME}')

#     # 3. Create Loan Record Table
#     df_loan_record = create_loan_record_table(df_master, df_farm_enterprise, fake)
#     df_loan_record.to_csv(LOAN_RECORD_FILENAME, index=False)
#     print(f'Loan Record data saved to {LOAN_RECORD_FILENAME}')

#     print("\nAll CSV files generated successfully in the 'data' directory.")
