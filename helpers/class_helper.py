class ClassHelper:
    def __init__(self) -> None:
        self.timetable: dict = {}
        self.class_info_dict: dict = {}

    def init_timetable(self) -> dict:
        self.timetable = {
            # hour: "room"
            8: "第一節",
            9: "第二節",
            10: "第三節",
            11: "第四節",
            13: "第五節",
            14: "第六節",
            15: "第七節",
            16: "第八節",
        }

    def init_class_info(self) -> dict:
        self.class_info_dict = {
            # (Day, Hour-Start): ("Room", "Class")
            (1, 8): ("R302", "高二3"),
            (1, 13): ("R401", "高二5"),
            (2, 8): ("R401", "高二4"),
            (2, 13): ("電腦B", "美二1"),
            (4, 10): ("TEAL", "跑班"),
            (4, 13): ("R401", "高二1"),
            (5, 13): ("R401", "高二2"),
        }

    def is_valid_class(self, day_of_week, hour, class_unit, classroom):
        class_info = self.get_class_info(day_of_week, hour)
        if class_unit != class_info[0] or classroom != class_info[1]:
            raise ValueError("錯誤的課堂或教室")

    def get_class_info(self, day_of_week, hour) -> tuple:
        return self.class_info_dict.get(day_of_week, hour)
