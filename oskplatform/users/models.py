from django.db import models

class student(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id} - {self.surname} {self.name}'
    
class instructor(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    date_of_employment = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False)
    instructor_id = models.CharField(max_length=15, null=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.id} - {self.surname} {self.name}'
    
class employee(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    date_of_employment = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.surname} {self.name}'
    
class qualification(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_achievement = models.DateField(null=False)
    instructor = models.ForeignKey(instructor, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey('course.Category', on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f'({self.instructor}) - ({self.category})'