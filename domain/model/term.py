from domain.model.course_attempt import CourseAttempt
from exceptions.invalid_argument import InvalidArgumentException

class Term:
    def __init__(self, term: str, year: int, degree: str, courses: list[CourseAttempt], location: str):
        self.term = term
        self.year = year
        self.degree = degree
        self.courses = list(courses)
        self.location = location
    
    def add_course(self, course: CourseAttempt) -> None:
        if not isinstance(course, CourseAttempt):
            raise InvalidArgumentException(f"addCourse(course) requires parameter of type CourseAttempt, parameter of type {type(course)} was passed instead.")
        self.courses.append(course)
    
    def get_courses(self, degree: str | None = None) -> list[CourseAttempt]:
        if degree is None:
            return list(self.courses)
        else:
            return [c for c in self.courses if degree in c.transfers or self.degree.startswith(degree)]

    def print_courses(self):
        ret = ""
        for c in self.courses:
            ret+=f"{c}\n"
        return ret.rstrip("\n")

    def __str__(self):
        return f"{self.year}/{self.term}\t{self.degree}\t{self.location}"
    