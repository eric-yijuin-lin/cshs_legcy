class StudentInfo:
    def __init__(self, form_data: dict) -> None:
        self.class_unit = form_data["class_unit"]
        self.no = int(form_data["no"])
        self.name = form_data["name"]
