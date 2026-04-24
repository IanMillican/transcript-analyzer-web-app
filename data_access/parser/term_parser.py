import re
from domain.model.course_attempt import CourseAttempt
from domain.model.term import Term
from data_access.parser.course_parser import parse_courses
from exceptions.parsing_exception import ParsingException

def _skip_line(line: str) -> bool:
    return (_credit_hour_line(line) or _end_of_year(line) or 
            _start_or_end_of_page(line) or _end_of_term(line) or 
            _header(line) or _end_of_record(line) or 
            _graduation(line) or _deans_list(line) or _coop(line))

def _term_separator(line: str) -> bool:
    return bool(re.fullmatch(r"^_+\s*$", line))

def _deans_list(line: str) -> bool:
    return line.startswith("Dean's")

def _coop(line: str) -> bool:
    return line.startswith("4-months") or line.startswith("with")

def _graduation(line: str) -> bool:
    return (line.startswith("Degree conferred") or line.startswith("Bachelor") or
            line.startswith("Minor") or 
            (line.startswith("(") and not line.startswith("(Continued")))

def _end_of_record(line: str) -> bool:
    return bool(re.fullmatch(r"^Awards\s+Granted:$", line) or
                re.fullmatch(r"^\d{4}-\d{2}\s+.*$", line) or
                re.fullmatch(r"^End\s+of\s+record$", line))

def _header(line: str) -> bool:
    return bool(re.fullmatch(r"GRADE\s+HRS\s+POINTS\s+TRANSFERS", line))

def _credit_hour_line(line: str) -> bool:
    return bool(re.fullmatch(r"^Program\s+Credit\s+Hours:\s+Attempted\s+\d{1,3}.\d{2}\s+Passed\s+\d{1,3}\d{2}\s+Cumulative\s+GPA\.\.\.\s+\d.\d$", line))

def _end_of_year(line: str) -> bool:
    return bool(re.fullmatch(r"^\d{4}/\d{2}\s+Assessment\s+Year\s+GPA\.*\s+\d.\d$", line) or
                re.fullmatch(r"^In\s+good\s+academic\s+standing$", line))

def _start_or_end_of_page(line: str) -> bool:
    return bool(re.fullmatch(r"(?iu)^UNOFFICIAL\s+TRANSCRIPT\s*\(Continued\s+on\s+page\s+\d{1,3}\)\s*$", line) or
                re.fullmatch(r"^UNOFFICIAL\s+TRANSCRIPT\s*$", line) or
                re.fullmatch(r"^\(Continued\s+from\s+page\s+\d{1,3}\)\s*$", line) or
                re.fullmatch(r"^\d{6,}\s+.+$", line))

def _end_of_term(line: str) -> bool:
    return bool(re.fullmatch(r"^Program\s+Credit\s+Hours:\s+Attempted\s+\d{1,3}\.\d{2}\s+Passed\s+\d{1,3}\.\d{2}\s+Cumulative\s+GPA\.\.\.\s+\d{1}\.\d{1}\s*$", line))

def parse_terms(transcript: list[str]) -> list[Term]:

    if len(transcript) == 0:
        raise ParsingException("This transcript is empty")
    terms = []
    pattern = re.compile(r"^(\d{4})/([A-Z]{2})\s+([A-Z]{2,6}(?:\s+[A-Z]{2,10})?)\s+(\S(?:.*\S)?)\s*$")
    while len(transcript) > 0:
        index = 0
        line = transcript[index]
        while index < len(transcript) and _skip_line(line):
            line = transcript[index]
            index += 1

        if index >= len(transcript):
            break

        m = pattern.fullmatch(line)
        if m:
            year = int(m.group(1))
            term = m.group(2)
            degree = m.group(3)
            location = m.group(4)
            index += 1
            if index >= len(transcript):
                break

            raw_courses = []
            line = transcript[index]
            while index < len(transcript) and not _term_separator(line):
                if not _skip_line(line):
                    raw_courses.append(line)
                index += 1
                if index < len(transcript):
                    line = transcript[index]

            index += 1
            parsed_courses = parse_courses(raw_courses)
            terms.append(Term(term, year, degree, parsed_courses, location))
            transcript = transcript[index:]
        else:
            raise ParsingException("Error parsing terms and degree info")

    return terms