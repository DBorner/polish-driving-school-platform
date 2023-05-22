from .models import TheoryCourse
import datetime


def get_course_dates(theory_id):
    course = TheoryCourse.objects.get(pk=theory_id)
    if course == None:
        return None
    dates = []
    if course.type == "T":
        if course.start_date.weekday() != 0:
            print("Wrong start date")
            return None
        dates.append((course.start_date, ('8:00', '14:00')))
        dates.append((course.start_date + datetime.timedelta(days=1), ('8:00', '14:00')))
        dates.append((course.start_date + datetime.timedelta(days=2), ('8:00', '14:00')))
        dates.append((course.start_date + datetime.timedelta(days=3), ('8:00', '14:00')))
        dates.append((course.start_date + datetime.timedelta(days=4), ('8:00', '14:00')))
        return dates
    else:
        if course.start_date.weekday() != 5:
            print("Wrong start date")
            return None
        dates.append((course.start_date, ('8:00', '16:00')))
        dates.append((course.start_date + datetime.timedelta(days=1), ('9:00', '16:00')))
        dates.append((course.start_date + datetime.timedelta(days=7), ('8:00', '16:00')))
        dates.append((course.start_date + datetime.timedelta(days=8), ('9:00', '16:00')))
        return dates