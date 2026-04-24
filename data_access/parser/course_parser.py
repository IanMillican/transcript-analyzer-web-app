import re
from domain.model.course_attempt import CourseAttempt

def parse_courses(term: list[str]) -> list[CourseAttempt]:
    pattern = re.compile(
        r"^([A-Z]{2,10})\*([A-Z0-9]{2,5})\s+(.+?)\s+(?:(WF|INC|NCR|CR|[A-D][+-]?|F|W)\s+)?"
        r"(\d{1,3}\.\d{2})(?:\s+\d{1,3}\.\d{2})?(?:\s+([A-Z]{2,4}(?:\s+[A-Z]{2,4})*))?\s*$"
    )
    courses = []
    for line in term:
        m = pattern.fullmatch(line)
        if m:
            subject = m.group(1)
            code = m.group(2)
            title = m.group(3)
            grade = m.group(4)
            if grade is None:
                grade = ""
            credit_hour = int(m.group(5).split(".")[0])
            transfers = m.group(6)
            transfer_list = [] if transfers is None else [t.strip() for t in transfers.split(" ")]
            if code.isdigit() and len(code) == 4:
                num = int(code)
                new_course = CourseAttempt(subject, num, title, credit_hour, grade, transfer_list)
                courses.append(new_course)
            else:
                new_course = CourseAttempt(subject, 0, title, credit_hour, grade, transfer_list)
                courses.append(new_course)
    
    return courses