import datetime
from student import StudentInfo
from schoolclass import ClassInfo
from seat import SeatInfo

class RegisterationRow:
    def __init__(self, student_info: StudentInfo, class_info: ClassInfo, seat_info: SeatInfo) -> None:
        self.class_unit = student_info.class_unit
        self.student_no = student_info.no
        self.student_name = student_info.name
        self.room_seat_code = f"{class_info.classroom}-{str(seat_info.room_seat_code).zfill(2)}"
        self.time_segment = class_info.segment
        self.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:S')

    def to_list(self) -> list:
        return [
            self.class_unit,
            self.student_no,
            self.student_name,
            self.room_seat_code,
            self.time_segment,
            self.datetime
        ]