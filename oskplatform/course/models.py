from django.db import models
from datetime import date, datetime
from django.db.models.constraints import CheckConstraint
from django.db.models import Q

vehicle_type_choices = [
    ('SO', 'Samochód osobowy'),
    ('MO', 'Motocykl'),
    ('SC', 'Samochód ciężarowy'),
    ('BU', 'Autobus'),
    ('PL', 'Przyczepa lekka'),
    ('PC', 'Przyczepa ciężka')
]

gearbox_type_choices = [
    ('M', 'Manualna'),
    ('A', 'Automatyczna'),
    ('N', 'Nie dotyczy')
]

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    registration_number = models.CharField(max_length=15, null=False)
    type = models.CharField(max_length=2, choices=vehicle_type_choices, default='SO', null=False)
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    year_of_production = models.IntegerField(null=True, blank=True)
    gearbox_type = models.CharField(max_length=1, choices=gearbox_type_choices, default='M', null=False)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.registration_number} - {self.type}'
    

class Category(models.Model):
    symbol = models.CharField(max_length=4, primary_key=True, unique=True, null=False)
    description = models.TextField(null=False)
    required_practical_hours = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(default='default_category.jpg', upload_to='category_photos')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.symbol

course_status_choices = [
    ('R', 'Rozpoczęty'),
    ('Z', 'Zakończony'),
    ('A', 'Anulowany'),
]

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    pkk_number = models.CharField(max_length=20, null=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    start_date = models.DateField(null=False)
    course_status = models.CharField(max_length=1, choices=course_status_choices, default='R', null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey('users.student', on_delete=models.CASCADE, null=False)
    instructor = models.ForeignKey('users.instructor', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.student.full_name} ({self.category.symbol})'
    
    @property
    def is_instructor_assigned(self):
        return self.instructor is not None
    
theory_type_choices = [
    ('T', 'Tygodniowy'),
    ('W', 'Weekendowy'),
]
    
class TheoryCourse(models.Model):
    class Meta:
        unique_together = (('type', 'start_date'))
        constraints = [CheckConstraint(check=Q(start_date__gte=date.today()), name='start_date_gte_today')]
    
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1, choices=theory_type_choices, default='T', null=False)
    start_date = models.DateField()
    instructor = models.ForeignKey('users.instructor', on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f'{self.id} - {self.start_date} ({self.type})'
    
class PracticalLesson(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    num_of_hours = models.IntegerField(null=False)
    num_of_km = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    instructor = models.ForeignKey('users.instructor', on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id} - {self.course.pkk_number} {self.date} ({self.start_time})'

    @property
    def has_already_happened(self):
        return self.date < date.today() 
    
    @property
    def is_paid(self):
        return self.cost is not None
    
    @property
    def get_end_time(self):
        hour = (self.start_time.hour + self.num_of_hours) % 24
        return datetime(year=self.date.year, month=self.date.month, day=self.date.day, hour=hour, minute=self.start_time.minute)
    
    @property
    def is_number_of_km_filled(self):
        return self.num_of_km is not None
    
    @property
    def is_vehicle_filled(self):
        return self.vehicle is not None