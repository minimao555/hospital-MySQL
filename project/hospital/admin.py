from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(InspectionItem)
admin.site.register(MedicalRecord)
admin.site.register(Office)
admin.site.register(Patient)
admin.site.register(PaymentSlip)
admin.site.register(PrescriptionList)
admin.site.register(RegistrationSlip)
