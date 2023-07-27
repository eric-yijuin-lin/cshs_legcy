import json
import os
from enum import Enum
from bs4 import BeautifulSoup

DEFAUT_SCHEDULE_FOLDER = "C:/Users/funny/Desktop/112暑輔網頁"
SUPPORTED_PREFIX = ['t', 'c', 'r']

class ScheduleType(Enum):
    Undefineded = 0
    Teacher = 1
    ClassUnit = 2
    Classroom = 3

class Schedule:
    def __init__(self, type_code: str, teacher_info: dict, schedule: dict) -> None:
        self.type = self.get_schedule_type(type_code)
        self.name = teacher_info['name']
        self.code = teacher_info['code']
        self.schedule = schedule

    def get_schedule_type(self, type_code: str) -> ScheduleType:
        if type_code.lower() == 't':
            return ScheduleType.Teacher
        elif type_code.lower() == 'c':
            return ScheduleType.ClassUnit
        elif type_code.lower() == 'r':
            return ScheduleType.Classroom
        else:
            raise ValueError("無效的類別碼")

    def get_as_json(self) -> dict:
        result = {
            "name": self.name,
            "code": self.code,
            "schedule": {}
        }
        for day in ["一", "二", "三", "四", "五"]:
            result["schedule"][day] = []
            for period in ["第一節", "第二節", "第三節", "第四節", "第五節", "第六節", "第七節", "第八節"]:
                key = (day, period)
                if key in self.schedule:
                    result["schedule"][day].append(self.schedule[key])
        return result


class ScheduleParser:
    def __init__(self, folder_path) -> None:
        self.folder_path = folder_path
        self.schedules = []

    def parse(self):
        self.schedules = self.get_schedules(self.folder_path)

    def get_schedules(self, folder_path: list) -> list:
        schedules = []
        file_names = os.listdir(folder_path)
        for file_name in file_names:
            type_code = file_name[0]
            if type_code in SUPPORTED_PREFIX:
                schedule = self.get_schedule_from_html(type_code, file_name)
            else:
                continue
            # self.save_json_single(schedule)
            schedules.append(schedule)
        return schedules
    
    def get_schedule_from_html(self, type_code: str, file_name: str) -> Schedule:
        file_name = f'{self.folder_path}/{file_name}'
        with open(file_name, "r", encoding="big5") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            title = self.get_title_from_bs4_object(soup)
            schedule = self.get_schedule_from_bs4_object(type_code, soup)
            return Schedule(type_code, title, schedule)

    def get_title_from_bs4_object(self, soup: BeautifulSoup) -> dict:
        title_set = soup.find_all("center")[0].text.split('    ')
        self.fix_title_set(title_set)
        code = title_set[0]
        name = title_set[1]
        return {
            'code': code,
            'name': name
        }

    def fix_title_set(self, title_set: list):
        if title_set[0] == "0317":
            title_set[1] = "吳亘霖"

    def get_schedule_from_bs4_object(self, type_code: str, soup: BeautifulSoup) -> dict:
        schedule = {}
        if type_code == 't':
            schedule = self.get_teacher_schedule(soup)
        elif type_code == 'c':
            schedule = self.get_classunit_schedule(soup)
        return schedule

    def get_teacher_schedule(self, bs4_obj: BeautifulSoup) -> dict:
        schedule = {}
        columns = ['節次', '時間', '一', '二', '三', '四', '五']
        table_rows = bs4_obj.find_all("tr")
        for tr in table_rows:
            if tr.text == "回教師課表索引頁" or tr.text == "午休" or tr.text == "\n\xa0\n一\n二\n三\n四\n五\n":
                continue
            row_data = tr.find_all("td")
            period = ''
 
            lc = len(columns)
            for i in range(lc):
                day = ''
                subject = ''
                class_unit = {}
                class_room = {}
                td = row_data[i]
                if len(td.contents) < 2:
                    print("正在忽略 ", td.contents)
                elif td.contents[0] == "第":
                    period = self.get_period(td.contents)
                    print(period)
                elif td.contents[2] == "｜":
                    print("正在忽略時間")
                elif td.find("a"):
                    subject = td.contents[0]
                    a_tags = td.find_all("a")
                    class_unit["text"] = a_tags[0].text
                    class_unit["href"] = a_tags[0]["href"]
                    if len(a_tags) == 2:
                        class_room["text"] = a_tags[1].text
                        class_room["href"] = a_tags[1]["href"]
                else:
                    print(td.contents)
                    raise ValueError("undefined structure detected.")
                if i >= 2 and subject:
                    day = columns[i]
                    schedule[(day, period)] = {
                        "subject": subject,
                        "class_unit": class_unit,
                        "class_room": class_room
                    }
        return schedule

    def get_classunit_schedule(self, bs4_obj: BeautifulSoup) -> dict:
        schedule = {}
        columns = ['節次', '時間', '一', '二', '三', '四', '五']
        table_rows = bs4_obj.find_all("tr")
        for tr in table_rows:
            if tr.text == "回班級課表索引頁" or tr.text == "午休" or tr.text == "\n\xa0\n一\n二\n三\n四\n五\n":
                continue
            row_data = tr.find_all("td")
            period = ''

            lc = len(columns)
            for i in range(lc):
                day = ''
                subject = ''
                teacher = {}
                class_room = {}
                td = row_data[i]
                if len(td.contents) < 2:
                    print("正在忽略 ", td.contents)
                elif td.contents[0] == "第":
                    period = self.get_period(td.contents)
                    print(period)
                elif td.contents[2] == "｜":
                    print("正在忽略時間")
                elif td.find("a"):
                    subject = td.contents[0]
                    a_tags = td.find_all("a")
                    teacher["text"] = a_tags[0].text
                    teacher["href"] = a_tags[0]["href"]
                    if len(a_tags) == 2:
                        class_room["text"] = a_tags[1].text
                        class_room["href"] = a_tags[1]["href"]
                else:
                    print(td.contents)
                    raise ValueError("undefined structure detected.")
                if i >= 2 and subject:
                    day = columns[i]
                    schedule[(day, period)] = {
                        "subject": subject,
                        "teacher": teacher,
                        "class_room": class_room
                    }
        return schedule

    def get_period(self, td_contents: list):
        return td_contents[0] + td_contents[2] + td_contents[4]

    def save_schedule_as_json(self, schedule: Schedule, folder) -> None:
        schedule_json = schedule.get_as_json()
        file_name = self.get_saving_file_name(schedule, folder)
        with open(file_name, "w", encoding="utf8") as fp:
            json.dump(schedule_json, fp, indent=4)

    def save_all_schedule_as_json(self, source_folder = DEFAUT_SCHEDULE_FOLDER) -> None:
        target_folder = source_folder + "/json"
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)
        for schedule in self.schedules:
            self.save_schedule_as_json(schedule, target_folder)

    def get_saving_file_name(self, schedule: Schedule, folder: str) -> str:
        file_name = f"{schedule.code}-{schedule.name}.json"
        if schedule.type == ScheduleType.Teacher:
            file_name = 't' + file_name
        elif schedule.type == ScheduleType.ClassUnit:
            file_name = 'c' + file_name
        elif schedule.type == ScheduleType.Classroom:
            file_name = 'r' + file_name
        else:
            raise ValueError("未定義的 schedule type")
        return f"{folder}/{file_name}"
    
    def unify_schedule_json(self, source_folder = DEFAUT_SCHEDULE_FOLDER + "/json") -> None:
        unified_json = {
            "teacher": [],
            "class_unit": [],
            "class_room": [],
        }
        file_list = os.listdir(source_folder)
        for file_name in file_list:
            if file_name[0] not in SUPPORTED_PREFIX or file_name[0] == '_':
                continue
            with open(f"{source_folder}/{file_name}", "r", encoding="utf8") as fp:
                schedule = json.load(fp)
            if file_name[0] == 't':
                unified_json["teacher"].append(schedule)
            elif file_name[0] == 'c':
                unified_json["class_unit"].append(schedule)
            elif file_name[0] == 'r':
                unified_json["class_room"].append(schedule)
            else:
                raise ValueError("未定義的 type prefix")
        output_file = source_folder + "/_unified.json"
        with open(output_file, "w", encoding="utf8") as fp:
            json.dump(unified_json, fp, indent=4)

parser = ScheduleParser(DEFAUT_SCHEDULE_FOLDER)
parser.parse()
parser.save_all_schedule_as_json()
parser.unify_schedule_json()
