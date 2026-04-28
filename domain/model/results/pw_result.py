from domain.model.course_attempt import CourseAttempt

class PWResult:
    def __init__(self, min_p_ch: int, min_p_courses: int, 
                 min_w_ch: int, min_w_courses: int,
                 satisfied_p: list[CourseAttempt], 
                 satisfied_w: list[CourseAttempt]):
        self.min_p_ch = min_p_ch
        self.min_p_courses = min_p_courses
        self.min_w_ch = min_w_ch
        self.min_w_courses = min_w_courses
        self.satisfied_p = satisfied_p
        self.satisfied_w = satisfied_w
    
    @property
    def p_satisfied(self) -> bool:
        total_ch = sum(c.credit_hours for c in self.satisfied_p)
        return len(self.satisfied_p) >= self.min_p_courses and total_ch >= self.min_p_ch
    
    @property
    def w_satisfied(self) -> bool:
        total_ch = sum(c.credit_hours for c in self.satisfied_w)
        return len(self.satisfied_w) >= self.min_w_courses and total_ch >= self.min_w_ch