from .models import Instructor, Qualification


def get_instructor_qualifications(instructor_id: int):
    if not Instructor.objects.filter(pk=instructor_id).exists():
        return None
    instructor = Instructor.objects.get(pk=instructor_id)
    qualifications = Qualification.objects.all().filter(instructor=instructor)
    return qualifications
