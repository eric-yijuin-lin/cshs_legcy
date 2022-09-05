import datetime
<<<<<<< HEAD
from modules.student import StudentInfo
from modules.schoolclass import ClassInfo
from modules.seat import SeatInfo
=======
from student import StudentInfo
from schoolclass import ClassInfo
from seat import SeatInfo
>>>>>>> 8d7bb190c233267b00c056e0a81e93fb22d94929

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