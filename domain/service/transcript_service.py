from data_access.parser.transcript_parser import parse_transcript
from domain.model.transcript import Transcript
from domain.model.course_attempt import CourseAttempt
from exceptions.invalid_argument import InvalidArgumentException

def get_transcript(path: str) -> Transcript:
    if not path.endswith(".pdf"):
        raise InvalidArgumentException("File type must be a PDF")
    return parse_transcript(path)
    