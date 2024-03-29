from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date
from django.db.models import Q


class Student(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(birth_date__lte=date.today()), name="student_birth_date_lte_today"
            )
        ]
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.surname} {self.name}"

    @property
    def full_name(self):
        return f"{self.surname} {self.name}"


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    date_of_employment = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False)
    instructor_id = models.CharField(max_length=15, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.surname} {self.name}"

    @property
    def full_name(self):
        return f"{self.surname} {self.name}"


class Employee(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(birth_date__lte=date.today()), name="employee_birth_date_lte_today"
            ),
            models.CheckConstraint(
                check=Q(date_of_employment__lte=date.today()), name="employee_date_of_employment_gte_birth_date"
            )
        ]
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    date_of_employment = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.surname} {self.name}"

    @property
    def full_name(self):
        return f"{self.surname} {self.name}"


class Qualification(models.Model):
    class Meta:
        unique_together = (("instructor", "category"),)
        constraints = [
            models.CheckConstraint(
                check=Q(date_of_achievement__lte=date.today()),
                name="date_of_achievement_lte_today",
            )
        ]

    id = models.AutoField(primary_key=True)
    date_of_achievement = models.DateField(null=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(
        "course.Category", on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f"({self.instructor}) - ({self.category})"


permissions_choices = [
    ("A", "Administrator"),
    ("I", "Instruktor"),
    ("E", "Pracownik"),
    ("S", "Kursant"),
]


class CustomUserMenager(BaseUserManager):
    def create_user(
        self, username, password=None, permissions_type="S", **extra_fields
    ):
        if not username:
            raise ValueError("Użytkownik musi mieć nazwę użytkownika")
        user = self.model(
            username=username, permissions_type=permissions_type, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractUser):
    permissions_type = models.CharField(
        max_length=1, choices=permissions_choices, default="S", null=False
    )
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, null=True, blank=True
    )
    instructor = models.OneToOneField(
        Instructor, on_delete=models.CASCADE, null=True, blank=True
    )
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, null=True, blank=True
    )
