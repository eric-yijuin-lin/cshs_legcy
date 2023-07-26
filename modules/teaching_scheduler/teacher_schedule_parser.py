import json
from os import listdir
from bs4 import BeautifulSoup

PERIOD_MAP = {
    "第一節" : ("08:00", "08:50"),
    "第二節" : ("09:10", "10:00"),
    "第三節" : ("10:10", "11:00"),
    "第四節" : ("11:10", "12:00"),
    "第五節" : ("13:10", "14:00"),
    "第六節" : ("14:10", "15:00"),
    "第七節" : ("15:15", "16:05"),
    "第八節" : ("16:10", "17:00"),
}

DEFAUT_SCHEDULE_FOLDER = "C:/Users/funny/Desktop/112暑輔網頁"

class ClassCell:
    def __init__(self) -> None:
        self.subject = ''
        self.teacher_name = ''
        self.teacher_code = ''
        self.class_unit = ''
        self.room = ''

class TeacherSchedule:
    def __init__(self, teacher_info: dict, schedule: dict) -> None:
        self.name = teacher_info['name']
        self.code = teacher_info['code']
        self.schedule = schedule
    def get_as_json(self) -> dict:
        result = {
            "name": self.name,
            "code": self.code,
            "schedule": {}
        }
        for day in ["一", "二", "三", "四", "五"]:
            result[day] = []
            for period in ["第一節", "第二節", "第三節", "第四節", "第五節", "第六節", "第七節", "第八節"]:
                key = (day, period)
                if key in self.schedule:
                    result[day].append(self.schedule[key])
                else:
                    result[day].append(None)
        return result


class TeacherScheduleParser:
    def __init__(self, folder_path) -> None:
        self.folder_path = folder_path
        self.teacher_schedules = []

    def parse(self):
        self.teacher_schedules = self.get_teacher_schedules(self.folder_path)

    def get_teacher_schedules(self, folder_path: list) -> list:
        schedules = []
        file_names = listdir(folder_path)
        for file_name in file_names:
            if file_name[0] != 't':
                continue
            schedule = self.get_teacher_schedule_from_html(file_name)
            # self.save_json_single(schedule)
            schedules.append(schedule)
        return schedules
    
    def get_teacher_schedule_from_html(self, file_name: str) -> TeacherSchedule:
        file_name = f'{self.folder_path}/{file_name}'
        with open(file_name, "r", encoding="big5") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            teacher = self.get_teacher_info_from_bs4_object(soup)
            schedule = self.get_schedule_from_bs4_object(soup)
            return TeacherSchedule(teacher, schedule)

    def get_teacher_info_from_bs4_object(self, soup: BeautifulSoup) -> dict:
        title_set = soup.find_all("center")[0].text.split('    ')
        self.fix_title_set(title_set)
        teacher_code = title_set[0]
        teacher_name = title_set[1]
        return {
            'code': teacher_code,
            'name': teacher_name
        }

    def fix_title_set(self, title_set: list):
        if title_set[0] == "0317":
            title_set[1] = "吳亘霖"
    
    def get_schedule_from_bs4_object(self, soup: BeautifulSoup) -> dict:
        schedule = {}
        rows = ["第一節", "第二節", "第三節", "第四節", "第五節", "第六節", "第七節", "第八節"]
        columns = ['節次', '時間', '一', '二', '三', '四', '五']
        table_rows = soup.find_all("tr")
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
                    raise Exception("undefined structure detected.")
                if i >= 2 and subject:
                    day = columns[i]
                    schedule[(day, period)] = {
                        "subject": subject,
                        "class_unit": class_unit,
                        "class_room": class_room
                    }
            print('---')
        return schedule

    def get_period(self, td_contents: list):
        return td_contents[0] + td_contents[2] + td_contents[4]
     
    def save_json_single(self, schedule: TeacherSchedule, folder) -> None:
        schedule_json = schedule.get_as_json()
        file_name = f"{folder}/{schedule.code}-{schedule.name}.json"
        with open(file_name, "w", encoding="utf8") as fp:
            json.dump(schedule_json, fp, indent=4)
    def save_json_all(self, folder = DEFAUT_SCHEDULE_FOLDER) -> None:
        folder = folder + "/json"
        for schedule in self.teacher_schedules:
            self.save_json_single(schedule, folder)


parser = TeacherScheduleParser(DEFAUT_SCHEDULE_FOLDER)
parser.parse()
parser.save_json_all()
