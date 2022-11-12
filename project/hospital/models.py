# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Doctor(models.Model):
    doctor_id = models.CharField(db_column='doctorID', primary_key=True, max_length=10)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1)
    age = models.IntegerField()
    phone_number = models.CharField(db_column='phoneNumber', max_length=255)
    address = models.CharField(max_length=255)
    office = models.CharField(max_length=255)
    photo = models.TextField()

    class Meta:
        db_table = 'doctor'


class InspectionItem(models.Model):
    inspection_id = models.CharField(db_column='inspectionID', primary_key=True, max_length=12)
    inspection_name = models.CharField(db_column='InspectionName', max_length=255)
    medical_records_id = models.ForeignKey('MedicalRecord', models.CASCADE, db_column='medicalRecordsID')
    payment_id = models.ForeignKey('PaymentSlip', models.CASCADE, db_column='paymentID')
    result = models.TextField()
    analysis = models.TextField(blank=True, null=True)
    picture = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inspection_item'


class MedicalRecord(models.Model):
    medical_records_id = models.CharField(db_column='medicalRecordsID', primary_key=True, max_length=10)
    patient_id = models.ForeignKey('Patient', models.CASCADE, db_column='patientID')
    doctor_id = models.ForeignKey(Doctor, models.CASCADE, db_column='doctorID')
    description = models.TextField(blank=True, null=True)
    office = models.ForeignKey('Office', models.CASCADE, db_column='office')
    treatment_programme = models.TextField(db_column='treatmentProgramme')
    diagnoses = models.TextField(db_column='Diagnoses')

    class Meta:
        db_table = 'medical_records'


class Office(models.Model):
    office_name = models.CharField(db_column='officeName', primary_key=True, max_length=255)
    head_id = models.CharField(db_column='headID', max_length=10, blank=True, null=True)
    number = models.IntegerField()

    class Meta:
        db_table = 'office'


class Patient(models.Model):
    patient_id = models.CharField(db_column='patientID', primary_key=True, max_length=10)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1)
    age = models.IntegerField()
    phone_number = models.CharField(db_column='phoneNumber', max_length=13)
    history = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    photo = models.TextField()

    class Meta:
        db_table = 'patient'


class PaymentSlip(models.Model):
    payment_id = models.CharField(db_column='paymentID', primary_key=True, max_length=10)
    patient_id = models.ForeignKey(Patient, models.CASCADE, db_column='patientID')
    payment_items = models.CharField(db_column='paymentItems', max_length=2)
    amount = models.FloatField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'payment_slip'


class PrescriptionList(models.Model):
    prescription_id = models.CharField(db_column='prescriptionID', primary_key=True, max_length=10)
    patient_id = models.ForeignKey(Patient, models.CASCADE, db_column='patientID')
    doctor_id = models.ForeignKey(Doctor, models.CASCADE, db_column='doctorID')
    payment_id = models.ForeignKey(PaymentSlip, models.CASCADE, db_column='paymentID')
    content = models.TextField()

    class Meta:
        db_table = 'prescription_list'


class RegistrationSlip(models.Model):
    registration_id = models.CharField(db_column='registrationID', primary_key=True, max_length=10)
    patient_id = models.ForeignKey(Patient, models.CASCADE, db_column='patientID')
    doctor_id = models.ForeignKey(Doctor, models.CASCADE, db_column='doctorID')
    office = models.ForeignKey(Office, models.CASCADE, db_column='office')
    payment_id = models.ForeignKey(PaymentSlip, models.CASCADE, db_column='paymentID')
    time = models.DateTimeField()
    type = models.CharField(max_length=4)

    class Meta:
        db_table = 'registration_slip'
