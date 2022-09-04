from calendar import weekday
from datetime import datetime
import seat
class ClassInfo:
    def __init__(self) -> None:
        self.unit = ""
        self.room = ""
        self.segment = 0

class ClassHelper:
    # hour: "節次"
    class_timetable = {
        8: "第一、二節",
        9: "第一、二節",
        10: "第三、四節",
        11: "第三、四節",
        13: "第五、六節",
        14: "第五、六節",
        15: "第七、八節",
        16: "第七、八節",
    }

    # (weekday, hour): ("room", "unit")
    class_info_dict = {
        (1, 8): ("R302", "高二3"),
        (1, 9): ("R302", "高二3"),
        (1, 13): ("R401", "高二5"),
        (1, 14): ("R401", "高二5"),
        (2, 8): ("R401", "高二4"),
        (2, 9): ("R401", "高二4"),
        (2, 13): ("電腦B", "美二1"),
        (2, 14): ("電腦B", "美二1"),
        (4, 10): ("TEAL", "跑班"),
        (4, 11): ("TEAL", "跑班"),
        (4, 13): ("R401", "高二1"),
        (4, 14): ("R401", "高二1"),
        (5, 13): ("R401", "高二2"),
        (5, 14): ("R401", "高二2"),
    }

    def __init__(self) -> None:
        self.seat_helper = seat.SeatHelper()

    def get_class_by_datetime(self, dt: datetime = None):
        if dt is None:
            dt = datetime.now()
        weekday = dt.weekday()
        hour = dt.hour
        return self.get_class_info(weekday, hour)

    def get_class_info(self, weekday, hour) -> ClassInfo:
        time_segment = ClassHelper.class_timetable.get(hour)
        class_item = ClassHelper.class_info_dict.get(weekday, hour)

        class_info = ClassInfo()
        class_info.segment = time_segment
        class_info.room = class_item[0]
        class_info.unit = class_item[1]
        return class_info
