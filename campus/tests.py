from django.test import TestCase
import requests
from models import *

# Create your tests here.

data = student.objects.filter(email = "hrp2121228@sicsr.ac.in")

subjectNames = []
for info in data:
    div = info.div
    subject_aliases = info.subjectAlias.split(", ")
    for subject_alias in subject_aliases:
        try:
            subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
            subjectNames.append(subject.subjectName)
        except Subjects.DoesNotExist:
            pass


for subjectName in subjectNames:
    subjectName = subjectName.replace(" ", "+")
    baseUrl = f"http://time-table.sicsr.ac.in/report.php?from_day=16&from_month=3&from_year=2023&to_day=15&to_month=5&to_year=2023&areamatch=&roommatch=&namematch=%28Div+{div}%29%3A{subjectName}&descrmatch=&creatormatch=&match_confirmed=2&output=0&output_format=1&sortby=r&sumby=d&phase=2&datatable=1"
    response = requests.get(baseUrl)
    csv_path = "../static/keys/{subjectName} report.csv"
    with open(csv_path, "wb") as file:
        file.write(response.content)
    file.close()