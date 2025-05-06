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
