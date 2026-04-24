from pypdf import PdfReader
import re
from datetime import date
from domain.model.transcript import Transcript
from domain.model.student import Student
from domain.model.month_day import MonthDay
from data_access.parser.term_parser import parse_terms
from exceptions.parsing_exception import ParsingException
from utils.constants import month_int_converter

def parse_transcript(file_path: str) -> Transcript:
    
    try:
        reader = PdfReader(file_path)
        full_text = "\n".join(page.extract_text() for page in reader.pages)
        lines = [line.strip() for line in full_text.split("\n")]
        index = 0

        if len(lines) <= 0 or not lines[index].strip() == "UNOFFICIAL TRANSCRIPT":
            raise ParsingException("This does not appear to be an unofficial transcript")
        index += 1

        name_id_line = lines[index]
        m = re.fullmatch(r"^(\d{6,})\s+(.+)$", name_id_line)
        if not m:
            raise ParsingException("Could not parse student ID and name")
        
        student_id = int(m.group(1))
        name = m.group(2).strip()
        index += 2  # Skip header line for DOB and DOI

        dob_doi_line = lines[index]
        m = re.fullmatch(
            r"^(\d{1,2})/(\d{1,2})\s+(\d{1,2})\s([A-Za-z]{3,4})\s(\d{4})$",
            dob_doi_line
        )
        if not m:
            raise ParsingException("Could not parse DOB/DOI")

        dob_month = int(m.group(1))
        dob_day = int(m.group(2))
        day = int(m.group(3))
        month_str = m.group(4)
        try:
            month_int = month_int_converter(month_str)
        except ValueError as e:
            raise ParsingException("Issue parsing month for DOI") from e
        year = int(m.group(5))
        index += 1

        if student_id == 0 or name is None:
            raise ParsingException("Issue parsing Student information")
        
        s = Student(name=name, student_id=student_id, dob=MonthDay(dob_month, dob_day))

        terms = parse_terms(lines[index:])

        # date uses 1900 as placeholder year since DOI only requires month and day, and 1900 is a particular year allowing for Feb29 birthdays
        transcript = Transcript(terms, s, date(1900, month_int, day))

    except IOError as e:
        raise ParsingException("IOError, failed to load the document") from e
    
    return transcript