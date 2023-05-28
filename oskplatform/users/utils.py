
from .models import Instructor, Qualification

def get_inctructor_qualifications(instructor_id):
    instructor = Instructor.objects.get(pk=instructor_id)
    if instructor is None:
        return None
    qualifications = Qualification.objects.all().filter(instructor=instructor)
    return qualifications
