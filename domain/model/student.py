from domain.model.month_day import MonthDay

class Student:
    def __init__(self, dob: MonthDay, name: str, student_id: int):
        self.dob = dob
        self.name = name
        self.student_id = student_id
    
    def __str__(self):
        return f"Name: {self.name}\nStudent ID: {self.student_id}\nDate of Birth: {self.dob.month:02d}/{self.dob.day:02d}"