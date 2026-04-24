from datetime import date
from domain.model.term import Term
from domain.model.course_attempt import CourseAttempt
from domain.model.student import Student

class Transcript():
    def __init__(self, terms: list[Term], student: Student, doi: date):
        self.terms = list(terms)
        self.student = student
        self.doi = doi

    def get_terms(self) -> list[Term]:
        return list(self.terms)
    
    def get_student_name(self) -> str:
        return self.student.name
    
    def get_student_id(self) -> int:
        return self.student.student_id
    
    def print_terms(self):
        ret = ""
        for t in self.terms:
            ret += f"{t}\n"
        return ret.rstrip("\n")

    def __str__(self):
        return f"{self.student}\n{self.print_terms()}"
    
    def get_courses(self, degree: str | None = None) -> list[CourseAttempt]:
        return [c for t in self.terms for c in t.get_courses(degree)]