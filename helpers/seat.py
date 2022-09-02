import hashlib
from datetime import datetime
from schoolclass import ClassHelper

class SeatHelper:
    def __init__(self) -> None:
        self.hasher = hashlib.md5()
        self.class_helper = ClassHelper()
        self.seat_dict = {}

    def init_seat_dict(self) -> None:
        classrooms = ["R302", "R401", "電腦B", "TEAL"]
        seat_dict = {}
        for room in classrooms:
            for i in range(1, 30 + 1):
                hash_value = self.get_seat_hash(room, i)
                seat_dict[hash_value] = (room, i)

    def register_seat(self, seat_hash: str) -> None:
        time_now = datetime.now()
        day_of_week = time_now.weekday()
        hour = time_now.hour

        seat_info = self.seat_dict.get(seat_hash)
        self.write_seat_record(seat_info)

    def validate_seat(self, seat_hasg: str) -> bool:
        pass

    def write_seat_record(self, seat_info: tuple) -> None:
        pass
    
    def get_seat_hash(self, classroom: str, seat_no: int) -> str:
        seat_str = classroom + str(seat_no).zfill(2)
        return self.get_hash(seat_str)

    def get_classroom_info(self, day_of_week: int, hour: int) -> tuple:
        return self.class_info_dict.get((day_of_week, hour), None)

    def get_hash(self, content: str) -> str:
        self.hasher.update(content)
        hash_bytes = self.hasher.digest()
        return hash_bytes.decode('utf-8')