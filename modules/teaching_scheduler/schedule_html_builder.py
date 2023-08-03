import dominate
from schedule_parser import *
from dominate.tags import *

day_texts = ["一","二","三","四","五"]
period_texts = ["第一節", "第二節", "第三節", "第四節", "第五節", "第六節", "第七節", "第八節"]
period_times = [("08:00", "08:50"),
    ("09:10", "10:00"),
    ("10:10", "11:00"),
    ("11:10", "12:00"),
    ("13:10", "14:00"),
    ("14:10", "15:00"),
    ("15:15", "16:05"),
    ("16:10", "17:00")
]

day_index_map = {
    "一": 0,
    "二": 1,
    "三": 2,
    "四": 3,
    "五": 4,
}

period_index_map = {
    "第一節": 0,
    "第二節": 1,
    "第三節": 2,
    "第四節": 3,
    "第五節": 4,
    "第六節": 5,
    "第七節": 6,
    "第八節": 7,
}

class TimetableHtmlBuilder:
    def __init__(self) -> None:
        self.parser = ScheduleParser(DEFAUT_SCHEDULE_FOLDER)
        self.schedules = []
        # time table: ordered, row=period, column=day
        self.teacher_timetables = []
        self.class_timetables = []
        self.room_timetables = []

    def load_schedule(self) -> None:
        self.parser.parse()
        self.schedules = self.parser.schedules
        # schedule: not ordered, key-map structure
        teacher_schedules = [x for x in self.schedules if x.type == ScheduleType.Teacher]
        class_schedules = [x for x in self.schedules if x.type == ScheduleType.ClassUnit]
        room_schedules = [x for x in self.schedules if x.type == ScheduleType.Classroom]
        for schedule in teacher_schedules:
            teacher_table = {
                "name": schedule.name,
                "code": schedule.code,
                "timetable": []
            }
            teacher_table["timetable"] = self.get_timetable(schedule)
            self.teacher_timetables.append(teacher_table)
        for schedule in class_schedules:
            class_table = {
                "name": schedule.name,
                "code": schedule.code,
                "timetable": []
            }
            class_table["timetable"] = self.get_timetable(schedule)
            self.class_timetables.append(class_table)
        for schedule in room_schedules:
            room_table = {
                "name": schedule.name,
                "code": schedule.code,
                "timetable": []
            }
            room_table["timetable"] = self.get_timetable(schedule)
            self.room_timetables.append(room_table)
    
    # time table: ordered, row=period, column=day
    def get_timetable(self, schedule_set: dict) -> list:
        time_table = []
        for _ in range(8):
            time_table.append([None] * 5)
        for period_index in range(8):
            for day_index in range(5):
                period_key = period_texts[period_index]
                day_key = day_texts[day_index]
                cell_key = (day_key, period_key)
                if cell_key in schedule_set.schedule:
                    time_table[period_index][day_index] = schedule_set.schedule[cell_key]
        return time_table

    def save_timetables_as_json(self, folder = DEFAUT_SCHEDULE_FOLDER + "/json"):
        file_name = folder + "/timetable_html.json"
        unified_json = {
            "teacher": self.get_timetable_json_array(self.teacher_timetables),
            "class_unit": self.get_timetable_json_array(self.class_timetables),
            "classroom": self.get_timetable_json_array(self.room_timetables),
        }
        with open(file_name, "w", encoding="utf8") as fp:
            json.dump(unified_json, fp, indent=4)

    def get_timetable_json_array(self, timetables: list) -> list:
        result = []
        for table_obj in timetables:
            table_html = self.timetable_to_html_table(table_obj["timetable"])
            timetable_json = {
                "name": table_obj["name"],
                "code": table_obj["code"],
                "table_html": table_html
            }
            result.append(timetable_json)
        return result

    def timetable_to_html_table(self, timetable: list) -> str:
        html = "<table border=\"2\" width=\"90%\" align=\"center\" cellpadding=\"1\" cellspacing=\"1\">"
        for period in range(8):
            html += self.timetable_row_to_html_tr(period, timetable[period])
        html += "</table>"
        return html

    def timetable_row_to_html_tr(self, period, timetale_row):
        tr_html = "<tr>"
        tr_html += self.create_chinese_period_td(period)
        tr_html += self.create_period_time_td(period)
        for i in range(5):
            tr_html += self.create_timetable_cell_td(timetale_row[i])
        tr_html += "</tr>"
        return tr_html

    def create_chinese_period_td(self, period_index) -> str:
        period_text = period_texts[period_index]
        return f"<td align=\"center\">{period_text}</td>"

    def create_period_time_td(self, period_index) -> str:
        time_start = period_times[period_index][0]
        time_end = period_times[period_index][1]
        return f"<td align=\"center\">{time_start}<br> | <br>{time_end}</td>"

    def create_timetable_cell_td(self, cell_dict) -> str:
        if cell_dict is None:
            return "<td align=\"center\">&nbsp;</td>"
        td_html = "<td align=\"center\">" + cell_dict["subject"]
        if "class_unit" in cell_dict and cell_dict["class_unit"]:
            class_unit = cell_dict["class_unit"]["text"]
            td_html += f"<br><a href=\"#\">{class_unit}</a>"
        if "teacher" in cell_dict and cell_dict["teacher"]:
            teacher = cell_dict["teacher"]["text"]
            td_html += f"<br><a href=\"#\">{teacher}</a>"
        if "class_room" in cell_dict and cell_dict["class_room"]:
            class_room = cell_dict["class_room"]["text"]
            td_html += f"<br><a href=\"#\">{class_room}</a>"
        td_html += "</td>"
        return td_html

builder = TimetableHtmlBuilder()
builder.load_schedule()
builder.save_timetables_as_json()
