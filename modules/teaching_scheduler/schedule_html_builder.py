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
        timetable_json = {}
        timetable_json["timetables"] = {
            "teacher": self.get_timetable_json_array(self.teacher_timetables),
            "class_unit": self.get_timetable_json_array(self.class_timetables),
            "classroom": self.get_timetable_json_array(self.room_timetables),
        }
        timetable_json["teacher_options"] = self.get_select_options(timetable_json, ScheduleType.Teacher)
        timetable_json["class_options"] = self.get_select_options(timetable_json, ScheduleType.ClassUnit)
        timetable_json["room_options"] = self.get_select_options(timetable_json, ScheduleType.Classroom)
        with open(file_name, "w", encoding="utf8") as fp:
            json.dump(timetable_json, fp, indent=4)

    def get_timetable_json_array(self, timetables: list) -> list:
        result = []
        for table_obj in timetables:
            table_html = self.timetable_to_html_table(False, table_obj["timetable"])
            timetable_json = {
                "name": table_obj["name"],
                "code": table_obj["code"],
                "table_html": table_html
            }
            result.append(timetable_json)
        return result

    def timetable_to_html_table(self, with_table_root: bool, timetable: list) -> str:
        tr_list_html = "<tr><td colspan=\"2\" align=\"center\">&nbsp;</td><td align=\"center\" width=\"15%\"><b>一</b></td><td align=\"center\" width=\"15%\"><b>二</b></td><td align=\"center\" width=\"15%\"><b>三</b></td><td align=\"center\" width=\"15%\"><b>四</b></td><td align=\"center\" width=\"15%\"><b>五</b></td></tr>"
        for period in range(8):
            tr_list_html += self.timetable_row_to_html_tr(period, timetable[period])

        if with_table_root:
            table_start = "<table border=\"2\" width=\"90%\" align=\"center\" cellpadding=\"1\" cellspacing=\"1\">"
            table_end = "</table>"
            return table_start + tr_list_html + table_end
        return tr_list_html

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
        table_types = ["class_unit", "teacher", "class_room"]
        for type_key in table_types:
            if type_key in cell_dict and cell_dict[type_key]: 
                link_text = cell_dict[type_key]["text"]
                link_href =  cell_dict[type_key]["href"]
                td_html += f"<br><a href=\"{link_href}\">{link_text}</a>"
        td_html += "</td>"
        return td_html

    def get_select_options(self, timetable_json: dict, schedule_type: ScheduleType):
        key_dict = {
            ScheduleType.Teacher: "teacher",
            ScheduleType.ClassUnit: "class_unit",
            ScheduleType.Classroom: "classroom",
        }
        key = key_dict[schedule_type]
        timetables: list = timetable_json["timetables"][key]
        return [
            {
                "name": timetable["name"],
                "code": timetable["code"]
            }
            for timetable in timetables
        ]
builder = TimetableHtmlBuilder()
builder.load_schedule()
builder.save_timetables_as_json()
