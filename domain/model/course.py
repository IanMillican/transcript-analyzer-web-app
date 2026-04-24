class Course:
    def __init__(self, subject: str, num: int, name: str, credit_hours: int, coop: bool):
        self.subject = subject
        self.num = num
        self.name = name
        self.credit_hours = credit_hours
        self.coop = coop

    @property
    def course_code(self) -> str:
        return f"{self.subject}{self.num}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Course):
            return False
        return self.course_code == other.course_code

    def __hash__(self) -> int:
        return hash(self.course_code)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Course):
            return NotImplemented
        return self.course_code < other.course_code

    def __str__(self) -> str:
        return f"{self.course_code}: {self.name} Credit Hours: {self.credit_hours}"