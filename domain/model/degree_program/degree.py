from domain.model.degree_program.section import Section

class Degree:
    def __init__(self, sections: list[Section], program: str, excluded_subjects: list[str], excluded_courses: list[str]):
        self.sections = list(sections)
        self.program = program
        self.excluded_subjects = list(excluded_subjects)
        self.excluded_courses = list(excluded_courses)