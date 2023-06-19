import os 
from tqdm import trange
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oskplatform.settings")

import django 
django.setup() 

from faker import Faker 
import random
from course.models import Category, Course, PracticalLesson 
from users.models import Instructor, Student, Qualification
from model_bakery import baker

def bake_data(how_many=10):
    fake = Faker(['pl_PL']) 
    print("Creating fake data...")
    for k in trange(0, how_many, desc ="Progress: "):
        name = fake.name()
        student = baker.make(Student,
                        name=name[0:name.find(' ')],
                        surname=name[name.find(' ')+1:],
                        birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80),
                        phone_number=fake.phone_number(),
                        email=fake.email()
        )
        categories = Category.objects.all()
        random_categories = random.sample(list(categories), random.randint(1, 3))
        for category in random_categories:
            instructor = pick_instructor(category)
            course = baker.make(Course,
                            pkk_number=fake.random_int(min=10000000000000000000, max=99999999999999999999),
                            cost=category.price,
                            start_date=fake.date_between(start_date='-3y', end_date='-1m'),
                            course_status='R',
                            category=category,
                            student=student,
                            instructor=instructor
            )
            num_of_hours = 0
            while num_of_hours < category.required_practical_hours:
                practical_lesson = baker.make(PracticalLesson,
                                        date=fake.date_between(start_date='-3y', end_date='-1m'),
                                        start_time=fake.time(),
                                        num_of_hours=random.randint(1, 2),
                                        num_of_km=random.randint(10, 50),
                                        cost=None,
                                        instructor=instructor,
                                        course=course
                )
                num_of_hours += practical_lesson.num_of_hours
            course.course_status = 'Z'
            course.save()
    print("Done!")


def pick_instructor(category):
    qualifications = Qualification.objects.filter(category=category)
    qualification = random.choice(qualifications)
    return qualification.instructor

def start_script():
    input("This script will create fake data. Press ENTER to continue...")
    input("It will only work if you have already created instructors, categories and qualifications. Press ENTER to continue...")
    x = input("Are you sure you want to continue? (y/n): ")
    if x == 'y':
        try:
            how_many = int(input("How many students do you want to create? (default: 10): "))
        except ValueError:
            print("Wrong input. Default value will be used.")
            bake_data()
        if how_many <= 0:
            bake_data()
        bake_data(how_many)
        
if __name__ == "__main__":
    start_script()