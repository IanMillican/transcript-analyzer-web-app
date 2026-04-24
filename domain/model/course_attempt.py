from domain.model.course import Course
from exceptions.invalid_argument import InvalidArgumentException

class CourseAttempt(Course):
    GRADE_POINT_MAP = {
        "A+": 4.3,
        "A":  4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B":  3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C":  2.0,
        "D":  1.0,
        "F":  0.0,
        "WF": 0.0
    }
    GRADE_PRECEDENCE = [
        "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F", "W", "WF", "INC", "CR", "NCR", "N/A"
    ]
    def __init__(self, subject: str, num: int, name: str, credit_hours: int, grade: str, transfers: list[str]):
        super().__init__(subject, num, name, credit_hours, num == 0)
        self.grade = grade
        self.transfers = list(transfers)

    def __eq__(self, other) -> bool:
        if isinstance(other, (CourseAttempt, Course)):
            return self.course_code == other.course_code
        else:
            return False
    
    def __lt__(self, other) -> bool:
        if isinstance(other, Course):
            return self.course_code < other.course_code
        return NotImplemented
        
    def __hash__(self) -> int:
        return hash(self.course_code)
    
    def __str__(self) -> str:
        points = self.credit_hours * CourseAttempt.GRADE_POINT_MAP.get(self.grade, 0.0)
        transfers_str = ", ".join(self.transfers) if self.transfers else ""
        return f"{self.course_code}\t{self.name}\tgrade: {self.grade}\t{self.credit_hours:.2f}ch\tpoints: {points:.2f}\t{transfers_str}"

    @staticmethod
    def grade_comparator(g1: str, g2: str) -> int:
        """Compares two grades to determine which is higher

        Args:
            g1 (str): First grade to be compared
            g2 (str): Second grade to be compared

        Raises:
            InvalidArgumentException: Raised if either grade is invalid.

        Returns:
            int: 1 if g2 is higher than g1, -1 if g1 is higher than g2, and 0 if they are equal.
        """

        if g1 not in CourseAttempt.GRADE_PRECEDENCE:
            raise InvalidArgumentException(f"{g1} is not a valid grade")
        elif g2 not in CourseAttempt.GRADE_PRECEDENCE:
            raise InvalidArgumentException(f"{g2} is not a valid grade")

        ind1 = CourseAttempt.GRADE_PRECEDENCE.index(g1)
        ind2 = CourseAttempt.GRADE_PRECEDENCE.index(g2)

        return (ind1 > ind2) - (ind1 < ind2)
    