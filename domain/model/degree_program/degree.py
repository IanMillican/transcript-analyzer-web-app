from domain.model.degree_program.section import Section

class Degree:
    def __init__(self, sections: list[Section], program: str, excluded_subjects: list[str], excluded_courses: list[str], pw_requirements: dict[str, int] | None = None):
        self.sections = list(sections)
        self.program = program
        self.excluded_subjects = list(excluded_subjects)
        self.excluded_courses = list(excluded_courses)
        self.pw_requirements = pw_requirements or {"min_p": 0, "min_w": 0}