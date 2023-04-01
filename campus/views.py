import json
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from .models import *
from datetime import datetime

import csv
from os import remove
import gspread

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE

base = str(settings.BASE_DIR)+"/static/"
current_datetime = datetime.today().date()
today = datetime.date
mail = {"clg_mail" : "hrp2121228@sicsr.ac.in", "clg_key" : "","1st_mail" : "", "1st_key" : "", "2nd_mail" : "hritikpatel2nd@gmail.com", "2nd_key": "wyrqybgvncedolxz", "Helper_mail" : "dropmailhelper@gamil.com", "Helper_key": "eugggsqhzudvjjry", "dhruvKhatri" : "dhk2121047@sicsr.ac.in", "service": "", "serviceKey": "frlgqyzzqylehkjr"}

# subjectDict -> name : url
path = settings.BASE_DIR/"static/keys/authKey.json"
gc = gspread.service_account(path)


# Create your functions here.
def getTimetable(url, For = None):
    import requests
    response = requests.get(url)
    csv_path = settings.BASE_DIR/"static/keys/report.csv"
    with open(csv_path, "wb") as file:
        file.write(response.content)
    file.close()
    # ====================================================
    if For is None:
        data = []
        with open(csv_path) as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                header = []
                for a in row:
                    if row.index(a) not in [1, 5, 6, 7, 8, 9, 10] and a not in header:
                        header.append(a)
                data.append(header)
    else:
        data = []
        with open(csv_path) as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                header = []
                for a in row:
                    if row.index(a) in [0,3,4] and a not in header:
                        header.append(a)
                data.append(header)
    remove(csv_path)
    return data

def send_mail(recipient, subject, body, file_path):
    
    # Setup port number and server name
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server


    sender = mail["2nd_mail"]
    password = mail["2nd_key"]
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Add the body text to the message
    body_text = MIMEText(body)
    msg.attach(body_text)

    # Add the file attachment to the message
    with open(file_path, "rb") as attachment:
        file_data = attachment.read()
        file_name = attachment.name
    file_attachment = MIMEApplication(file_data)
    file_attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(file_attachment)

    # Create context
    # simple_email_context = ssl.create_default_context()

    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    try:
        # Connect to the server
        print("Connecting to server...")
        TIE_server.starttls()
        TIE_server.login(sender, password)
        print("Connected to server :-)")
        
        # Send the actual email
        print()
        print(f"Sending email to - {recipient}")
        TIE_server.sendmail(sender, recipient, msg.as_string())
        print(f"Email successfully sent to - {recipient}")

    # If there's an error, print it out
    except Exception as e:
        print(e)

    # Close the port
    finally:
        TIE_server.quit()

# Utility functions

def informer(request):

    loggedUser = request.GET.get('loggedUser')
    calledFor = request.GET.get('calledFor')
    isStudent = request.GET.get("isStudent")
    
    if calledFor == "notes":
        import re
        data = loginCrad.objects.filter(email=loggedUser)
        uploaderData = teachers.objects.filter(email = loggedUser)
        subjectNames = []
        fileData = []

        for info in data:
            isStudent = info.isStudent

        if isStudent == "N":
            notesData = notesFile.objects.filter(uploadedBy=loggedUser)
            for info in uploaderData:
                uploader = info.fullname
                showTo = info.subjectAlias.split(", ")
                for subject_alias in showTo:
                    try:
                        subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                        subjectNames.append(subject.subjectName)
                    except Subjects.DoesNotExist:
                        pass
            for info in notesData:
                if len(info.originalName)> 7:
                    title = re.match(r'^.{7}', info.originalName).group()+"..."
                    fileData.append({ "title": info.title ,"fileName": title, "uploader": uploader, "date": str(info.uploadedOn).replace("00:00:00",""), "filePaths" : info.fileLocation.replace("./", "/"), "pk": info.pk})
                else:
                    fileData.append({ "title": info.title ,"fileName": info.originalName, "uploader": uploader, "date": str(info.uploadedOn).replace("00:00:00",""), "filePaths" : info.fileLocation.replace("./", "/"), "pk": info.pk})
            user_info = {
                "isStudent": isStudent,
                "fileData" : fileData,
                "subjectNames" : subjectNames,
                "showTo": showTo,
            }
        else:
            studentData = student.objects.filter(email = loggedUser)
            for info in studentData:
                subjects = info.subjectAlias.split(", ")
            for subject in subjects:
                notesData = notesFile.objects.all()
                for notes in notesData:
                    if subject in notes.uploadedFor:
                        uploaderData = teachers.objects.filter(email = notes.uploadedBy)
                        for name in uploaderData:
                            uploader = name.fullname
                        if len(notes.originalName)> 7:
                            title = re.match(r'^.{7}', notes.originalName).group()+"..."
                            fileData.append({ "title": notes.title ,"fileName": title, "uploader": uploader, "date": str(notes.uploadedOn).replace("00:00:00",""), "filePaths" : notes.fileLocation.replace("./", "/"), "pk" : notes.pk})
                        else:
                            fileData.append({ "title": notes.title ,"fileName": notes.originalName, "uploader": uploader, "date": str(notes.uploadedOn).replace("00:00:00",""), "filePaths" : notes.fileLocation.replace("./", "/"), "pk" : notes.pk})
            user_info = {
                    "isStudent": isStudent,
                    "fileData" : fileData,
                }
    elif calledFor == "login":
        username = request.GET.get("loggedUser")
        password = request.GET.get("password")

        try:
            data = loginCrad.objects.get(email=loggedUser)
            if data.email == username and data.password == password:
                user_info = {
                    "access" : "Granted",
                    "isStudent" : data.isStudent,
                }
            else:
                user_info = {
                    "access" : "notGranted"
                } 
        except Exception as e:
            user_info = {
                "access" : "notGranted"
            }
    elif calledFor == "timeline":
        info = {}
        if isStudent == "Y":
            record = student.objects.get(email=loggedUser)
            subject_aliases = record.subjectAlias.split(", ")
            subjectNames = []
            for subject_alias in subject_aliases:
                try:
                    subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                    subjectNames.append(subject.subjectName)
                except Subjects.DoesNotExist:
                    pass
            user_info = {
                "loggedUser" : loggedUser,
                "setID" : record.setID,
                "prn" : record.prn,
                "fullname" : record.fullname,
                "phone" : record.phone,
                "image" : record.photo.replace("./", "/"),
                "subjectNames" :subjectNames,
                "Div" : record.div,
                "course": record.course,
                "sem" : record.sem,
                "year" : record.year

            }
        else:
            records = teachers.objects.filter(email=loggedUser)
            for record in records:
                subject_aliases = record.subjectAlias.split(", ")
                subjectNames = []
                for subject_alias in subject_aliases:
                    try:
                        subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                        subjectNames.append(subject.subjectName)
                    except Subjects.DoesNotExist:
                        pass
                user_info = {
                    "fullname" : record.fullname,
                    "subjectNames" :subjectNames,
                }
    elif calledFor == "lecture":
        today = str(datetime.now()).split(" ")[0]
        user_info ={
        "lectures": lecture(loggedUser, today.split("-"),isStudent),
        "todo" : todoFinder(loggedUser, today)}
    elif calledFor == "attendance":
        if isStudent == "N":
            teacherData = teachers.objects.filter(email = loggedUser)
            subjectNames = []
            subjectTypes = []
            for info in teacherData:
                subject_aliases = info.subjectAlias.split(", ")
                for subject_alias in subject_aliases:
                    try:
                        subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                        subjectNames.append(subject.subjectName)
                        subjectTypes.append(subject.subjectType)
                    except Subjects.DoesNotExist:
                        pass
            user_info = {
                "subjectNames": subjectNames,
                "subjectTypes": subjectTypes,
            }
        else:
            studentData = student.objects.filter(email = loggedUser)
            subjectNames = []
            subjectDict = {}
            for info in studentData:
                prn = info.prn
                subject_aliases = info.subjectAlias.split(", ")
                for subject_alias in subject_aliases:
                    try:
                        subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                        subjectNames.append(subject.subjectName)
                    except Subjects.DoesNotExist:
                        pass
            for subject in subjectNames:
                data = attendanceSheets.objects.filter(subject = subject)
                for info in data:
                    if info.urlShared is not None:
                        subjectDict[subject] = info.urlShared
            user_info = {"data": getAttendence(prn, subjectDict,)} # TODO  sheetName
            
            # user_info = {'Software Project Practices': {'attendence': ['P', 'P', 'A', 'P', 'P', 'P', 'P'], 'head': ['1', '2', '3', '4', '5', '6', '7']}, 'Cloud Application Development (Group 1)': {'attendence': ['P', 'P', 'A', 'P', 'P', 'P', 'P'], 'head': ['1', '2', '3', '4', '5', '6', '7']}}
    elif calledFor == "verify":
        from gspread.exceptions import APIError
        urlVerifiable = request.GET.get('url')

        teacherData = teachers.objects.filter(email = loggedUser)
        subjectNames = []
        for info in teacherData:
            subject_aliases = info.subjectAlias.split(", ")
            for subject_alias in subject_aliases:
                try:
                    subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                    subjectNames.append(subject.subjectName)
                except Subjects.DoesNotExist:
                    pass

        try:
            path = settings.BASE_DIR/"static/keys/authKey.json"
            client = gspread.service_account(filename=path)
            sheet = client.open_by_url(urlVerifiable)
            
            sheet_names = [worksheet.title for worksheet in sheet.worksheets()]
            num_sheets = len(sheet_names)
            if num_sheets==1:
                user_info = {
                    "status" : "OK",
                    "sheet_names" : sheet_names,
                    "Subject": subjectNames,
                }
            elif num_sheets>1:
                user_info = {
                    "status" : "Multi",
                    "sheet_names" : sheet_names,
                    "Subject": subjectNames,
                }
        except APIError as error:
            user_info = {
                "status" : str(error)
            }
        except Exception as error:
            user_info = {
                "status" : str(error)
            }
    elif calledFor == "saveAttendance":
        subject = request.GET.get("subject")
        urlShared = request.GET.get("urlShared")
        sheet = request.GET.get("sheet")
        div = request.GET.get("Div")

        try:
            data = attendanceSheets.objects.get(subject = subject)
            data.urlShared = urlShared
            data.sheetName = sheet
            data.divList = div
            data.save()
        except attendanceSheets.DoesNotExist:
            data = attendanceSheets(subject = subject, urlShared = urlShared, sheetName = sheet, sharedBy = loggedUser, divList = div)
            data.save() 
    elif calledFor == "deleteNotes":
        pk = request.GET.get('id')
        fileToDelete = notesFile.objects.get(pk =int(pk))
        
        remove(base+fileToDelete.fileLocation.replace("./","/"))
        fileToDelete.delete()
    elif calledFor == "sendNotes":
        pk = request.GET.get('id')
        fileToDelete = notesFile.objects.get(pk =int(pk))
        filepath = base+fileToDelete.fileLocation.replace("./","/")

        body = f'''Title: {fileToDelete.title}\nDescription: {fileToDelete.desc}\nFilename: {fileToDelete.originalName}\nUploaded By: {fileToDelete.uploadedBy}\nUploaded On: {fileToDelete.uploadedOn}'''
        user_info = {
            "data" : send_mail(recipient= loggedUser, subject="File Delivery", body = body, file_path=filepath)
        }
        # remove(base+fileToDelete.fileLocation.replace("./","/"))
        # fileToDelete.delete()
    elif calledFor == "getLecture":
        year, month, date = request.GET.get("date").split("T")[0].split("-")
        subject = request.GET.get("subject")
        print(date, subject)
        url = f"http://time-table.sicsr.ac.in/report.php?from_day={date}&from_month={month}&from_year={year}&to_day={date}&to_month={month}&to_year={year}&areamatch=&roommatch=&namematch={subject}&descrmatch=&creatormatch=&match_confirmed=2&output=0&output_format=1&sortby=r&sumby=d&phase=2&datatable=1"
        data = getTimetable(url, For="data")
        
        user_info = {
            "data" : data
            }
    elif calledFor == "lectureCancelled":
        head, start, end, changedFor = json.loads(request.GET.get("data"))
        data = lectureMod(head = head, start = start, end = end, changedFor = changedFor)
        data.save()
        user_info = {
            "data" : "Lecture Cancelled"
        }
    elif calledFor == "getSheet":
        data = attendanceSheets.objects.filter(sharedBy = loggedUser)
        user_info = {
            "data": data
        }
    try:
        return JsonResponse(user_info)
    except Exception as error:
        print(error)
        user_info = {
            "error" : "internal server error. Please try again later..."
        }
        return JsonResponse(user_info)

def lecture(loggedUser, today, isStudent):  
    
    # Create your tests here.

    if isStudent == "Y":
        data = student.objects.filter(email = loggedUser)
        subjectNames = {}
        for info in data:
            div = info.div
            sem = info.sem
            course = info.course
            subject_aliases = info.subjectAlias.split(", ")
            for subject_alias in subject_aliases:
                try:
                    subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                    subjectNames[subject.subjectName] = subject.subjectType
                except Subjects.DoesNotExist:
                    pass
                
        
        lectures = {}
        for subjectName in subjectNames:
            # print(subjectName)
            lectureCancelled = lectureMod.objects.filter(changedFor = subjectName)
            print(lectureCancelled)
            if subjectNames[subjectName] == "Base":
                subjectType = f"(Div {div}):".replace("(", "%28").replace(")", "%29").replace(":", "%3A")
            elif subjectNames[subjectName] == "Elective":
                subjectType = f"{course} Sem {sem} (Elective) :".replace("(Hons.)", "").replace("(", "%28").replace(")", "%29").replace(":", "%3A")
            elif subjectNames[subjectName] == "Honours":
                subjectType = f"{course} Sem {sem} (Elective) :".replace("Hons.", "Honours").replace("(", "%28").replace(")", "%29").replace(":", "%3A")
            
            subjectName = subjectName.replace(" ", "+").replace("(", "%28").replace(")", "%29")
            subjectType = subjectType.replace(" ", "+")

            baseUrl = f"http://time-table.sicsr.ac.in/report.php?from_day={today[2]}&from_month={today[1]}&from_year={today[0]}&to_day={today[2]}&to_month={today[1]}&to_year={today[0]}&areamatch=&roommatch=&namematch={subjectType}{subjectName}&descrmatch=&creatormatch=&match_confirmed=2&output=0&output_format=1&sortby=r&sumby=d&phase=2&datatable=1"
            response = requests.get(baseUrl)

            csv_path = f"{subjectName} report.csv"
            
            with open(csv_path, "wb") as file:
                file.write(response.content)
            file.close()
            
            count = 0
            with open(csv_path) as file:
                csv_reader = csv.reader(file)
                next(csv_reader) # Skip the header row
                for row in csv_reader:
                    # print(row)
                    if lectureCancelled:
                        for info in lectureCancelled:
                            # print(info.head == row[0] and info.end == row[4] and info.start == row[3])
                            # print(info.head, info.end, info.start)
                            # print(row[0], row[4], row[3])

                            if info.head == row[0] and info.end == row[4] and info.start == row[3]:
                                pass
                            else:
                                header = [a for i,a in enumerate(row) if i not in [1, 5, 6, 7, 8, 9, 10]]
                                header[0] = subjectName.replace("+", " ").replace("%28", "(").replace("%29", ")")
                                if header[0] not in lectures:
                                    lectures[header[0]] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                                else:
                                    lectures[header[0]+str(count)] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                                    count+=1
                    else:
                        header = [a for i,a in enumerate(row) if i not in [1, 5, 6, 7, 8, 9, 10]]
                        header[0] = subjectName.replace("+", " ").replace("%28", "(").replace("%29", ")")
                        if header[0] not in lectures:
                            lectures[header[0]] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                        else:
                            lectures[header[0]+str(count)] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                            count+=1

            try:
                remove(csv_path)
            except Exception as e:
                print(e)
        
        sorted_lectures = sorted(lectures.items(), key=lambda x: x[1]['startTime'])
        lectures.clear()
        for key, value in sorted_lectures:
            lectures[key] = value
            
        
        return lectures
    else:
        data = teachers.objects.filter(email = loggedUser)
        subjectNames = {}
        for info in data:
            subject_aliases = info.subjectAlias.split(", ")
            for subject_alias in subject_aliases:
                try:
                    subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                    subjectNames[subject.subjectName] = subject.subjectType
                except Subjects.DoesNotExist:
                    pass
                
        
        lectures = {}
        for subjectName in subjectNames:
            lectureCancelled = lectureMod.objects.filter(changedFor = subjectName)

            subjectName = subjectName.replace(" ", "+").replace("(", "%28").replace(")", "%29")

            baseUrl = f"http://time-table.sicsr.ac.in/report.php?from_day={today[2]}&from_month={today[1]}&from_year={today[0]}&to_day={today[2]}&to_month={today[1]}&to_year={today[0]}&areamatch=&roommatch=&namematch={subjectName}&descrmatch=&creatormatch=&match_confirmed=2&output=0&output_format=1&sortby=r&sumby=d&phase=2&datatable=1"
            
            response = requests.get(baseUrl)

            csv_path = f"{subjectName} report.csv"
            
            with open(csv_path, "wb") as file:
                file.write(response.content)
            file.close()
            
            count = 0
            with open(csv_path) as file:
                csv_reader = csv.reader(file)
                next(csv_reader) # Skip the header row
                for row in csv_reader:
                    if lectureCancelled:
                        for info in lectureCancelled:
                            # print(info.head == row[0] and info.end == row[4] and info.start == row[3])
                            # print(info.head, info.end, info.start)
                            # print(row[0], row[4], row[3])

                            if info.head == row[0] and info.end == row[4] and info.start == row[3]:
                                pass
                            else:
                                header = [a for i,a in enumerate(row) if i not in [1, 5, 6, 7, 8, 9, 10]]
                                header[0] = subjectName.replace("+", " ").replace("%28", "(").replace("%29", ")")
                                if header[0] not in lectures:
                                    lectures[header[0]] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                                else:
                                    lectures[header[0]+str(count)] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                                    count+=1
                    else:
                        header = [a for i,a in enumerate(row) if i not in [1, 5, 6, 7, 8, 9, 10]]
                        header[0] = subjectName.replace("+", " ").replace("%28", "(").replace("%29", ")")
                        if header[0] not in lectures:
                            lectures[header[0]] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                        else:
                            lectures[header[0]+str(count)] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", "").replace("Flexi-Credit Course Introduction to ", ""), "roomNo": header[1], "startTime": header[2].split(":00 - ")[0], "endTime": header[3].split(":00 - ")[0]}
                            count+=1

            try:
                remove(csv_path)
            except Exception as e:
                print(e)
        
        sorted_lectures = sorted(lectures.items(), key=lambda x: x[1]['startTime'])
        lectures.clear()
        for key, value in sorted_lectures:
            lectures[key] = value
        
        return lectures


def todoFinder(loggedUser, today):
        
    todoDict = {}
    todoList = todo.objects.filter(email=loggedUser)
    count = 0
    for data in todoList:
        if str(data.time) == today:
            title = data.task
            desc = data.desc
            time = data.time

            todoDict[str(count)+title] = {"title":title,"desc":desc,"time": time}
            count += 1
    return todoDict


def getSheet(url,worksheet):
    data = gc.open_by_url(url)

    worksheet = data.worksheet(worksheet)
    return worksheet.values




def test(request):

    try:
        # subjectDict -> name : url
        #https://docs.google.com/spreadsheets/d/1urV2qsxq2GmfOokhHHJukSC1z4C6VRnVzi2WaYlVJ5I
        subjectDict = {"Software Project Practices": "https://docs.google.com/spreadsheets/d/13gdm_qfsPPHZz7WHciT1bli3vzh_QGRgN4bcgLHjOSk/edit?usp=sharing"}
        prn = "21030121228"
        path = settings.BASE_DIR/"static/keys/authKey.json"
        gc = gspread.service_account(path)
        data = {}        
        for i in subjectDict.keys():
            sheet = gc.open_by_url(subjectDict[i])
            worksheet = sheet.get_worksheet(0)
            
            heaer = worksheet.row_values(2) #getting header form row 2
            
            findbyprn= worksheet.find(prn)
            attendance =worksheet.row_values(findbyprn.row)
            del heaer[0:2] 
            del attendance[0:2]
            
            data[f"{i}"]= {'attendence':f"{attendance}",'head':f'{heaer}'}
            
        user_info = {
            "data": data
        }
        # return data
    except Exception as b:
        return HttpResponse(b)
    return HttpResponse(user_info.values())


    # today = str(datetime.now()).split(" ")[0].split("-")

    # # Create your tests here.

    # data = student.objects.filter(email = "hrp2121228@sicsr.ac.in")

    # subjectNames = {}
    # for info in data:
    #     div = info.div
    #     sem = info.sem
    #     course = info.course
    #     subject_aliases = info.subjectAlias.split(", ")
    #     for subject_alias in subject_aliases:
    #         try:
    #             subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
    #             subjectNames[subject.subjectName] = subject.subjectType
    #         except Subjects.DoesNotExist:
    #             pass
    
    
    # lectures = {}
    # for subjectName in subjectNames:
    
    #     if subjectNames[subjectName] == "Base":
    #         subjectType = f"(Div {div}):".replace("(", "%28").replace(")", "%29").replace(":", "%3A")
    #     elif subjectNames[subjectName] == "Elective":
    #         subjectType = f"{course} Sem {sem} (Elective) :".replace("(Hons.)", "").replace("(", "%28").replace(")", "%29").replace(":", "%3A")
    #     elif subjectNames[subjectName] == "Honours":
    #         subjectType = f"{course} Sem {sem} (Elective) :".replace("Hons.", "Honours").replace("(", "%28").replace(")", "%29").replace(":", "%3A")
        
    #     subjectName = subjectName.replace(" ", "+").replace("(", "%28").replace(")", "%29")
    #     subjectType = subjectType.replace(" ", "+")

    #     baseUrl = f"http://time-table.sicsr.ac.in/report.php?from_day={today[2]}&from_month={today[1]}&from_year={today[0]}&to_day={today[2]}&to_month={today[1]}&to_year={today[0]}&areamatch=&roommatch=&namematch={subjectType}{subjectName}&descrmatch=&creatormatch=&match_confirmed=2&output=0&output_format=1&sortby=r&sumby=d&phase=2&datatable=1"
    #     response = requests.get(baseUrl)

    #     csv_path = f"{subjectName} report.csv"
        
    #     with open(csv_path, "wb") as file:
    #         file.write(response.content)
    #     file.close()
        
    #     with open(csv_path) as file:
    #         csv_reader = csv.reader(file)
    #         next(csv_reader) # Skip the header row
    #         for row in csv_reader:
    #             header = [a for i,a in enumerate(row) if i not in [1, 5, 6, 7, 8, 9, 10]]
    #             header[0] = subjectName.replace("+", " ").replace("%28", "(").replace("%29", ")")
    #             lectures[header[0]] = {"subjectName": header[0].replace("Group", "").replace("(", "").replace(")", "").replace("1", "").replace("2", ""), "roomNo": header[1], "startTime": header[2], "endTime": header[3]}

    #     try:
    #         remove(csv_path)
    #     except Exception as e:
    #         print(e)

    #     todoDict = {}
    #     todoList = todo.objects.filter(email="hrp2121228@sicsr.ac.in")
    #     count = 0
    #     for data in todoList:
    #         if str(data.time) == str(today[0])+"-"+str(today[1])+"-"+str(today[2]):
    #             title = data.task
    #             desc = data.desc
    #             time = data.time

    #             todoDict[str(count)+title] = {"title":title,"desc":desc,"time": time}
    #             count += 1
    



def getAttendence(prn,subjectDict): 
    try:
        # sub_url="12LGDs1PQtSxPloP-5uOtK2YP4ebjtZ9epGgGvxUz2k0"
        data = {}
        for i in subjectDict.keys():
            sheet = gc.open_by_url(subjectDict[i])
            # worksheet = sheet.worksheet() # TODO  sheetName
            worksheet = sheet.get_worksheet(0)
            heaer = worksheet.row_values(2)
            findbyprn= worksheet.find(prn)
            attendance =worksheet.row_values(findbyprn.row)
            del heaer[0:2] 
            del attendance[0:2]
            data[f"{i}"]= {'Date': heaer, 'Attendance': attendance,}
        return data
    except Exception as b:
        return b



# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def login_user(request):
    template = loader.get_template('login.html') 
    return HttpResponse(template.render())

def attendance(request):
    template = loader.get_template('attendance.html')
    return HttpResponse(template.render())

def timeline(request):
    info = {}
    
    template = loader.get_template('timeline.html')
    if request.method == "POST":
        method_name = request.POST.get("submitBtn")
        if method_name == "findTable":
            loggedUser = request.POST["loggedUser"]
            isStudent = request.POST["isStudent"]

            startDate = request.POST["start-date"].split("-")[2]
            startMonth = request.POST["start-date"].split("-")[1]
            startYear = request.POST["start-date"].split("-")[0]
            endDate = request.POST["end-date"].split("-")[2]
            endMonth = request.POST["end-date"].split("-")[1]
            endYear = request.POST["end-date"].split("-")[0]
            opts = request.POST.getlist('match-type')
            lecture = ""
            for item in opts:
                lecture = lecture+"&typematch%5B%5D="+item
            url = f"http://time-table.sicsr.ac.in/report.php?from_day={startDate}&from_month={startMonth}&from_year={startYear}&to_day={endDate}&to_month={endMonth}&to_year={endYear}&areamatch=&roommatch={lecture}&namematch=&descrmatch=&creatormatch=&match_confirmed=2&output=0&output_format=1&sortby=s&sumby=d&phase=2&datatable=1"
            info["data"] = getTimetable(url)
            if isStudent == "Y":
                records = student.objects.filter(email=loggedUser)
            else:
                records = teachers.objects.filter(email=loggedUser)
            for record in records:
                subject_aliases = record.subjectAlias.split(", ")
                subjectNames = []
                for subject_alias in subject_aliases:
                    try:
                        subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                        subjectNames.append(subject.subjectName)
                    except Subjects.DoesNotExist:
                        pass
            info["subjectNames"] = subjectNames

        elif method_name == "addInfo":
            loggedUser = request.POST["loggedUser"]
            isStudent = request.POST["isStudent"]
            task = request.POST["task"]
            desc = request.POST["description"]
            time = request.POST["time"]
            reminder = str(request.POST["reminder"])

            if reminder == "on": 
                TODO = todo(email = loggedUser, task = task, time = time, reminder = True, desc = desc)
            else:
                TODO = todo(email = loggedUser, task = task, time = time, desc = desc)

            TODO.save()

            if isStudent == "Y":
                records = student.objects.filter(email=loggedUser)
            else:
                records = teachers.objects.filter(email=loggedUser)
            for record in records:
                subject_aliases = record.subjectAlias.split(", ")
                subjectNames = []
                for subject_alias in subject_aliases:
                    try:
                        subject = Subjects.objects.get(subjectAlias=subject_alias.strip())
                        subjectNames.append(subject.subjectName)
                    except Subjects.DoesNotExist:
                        pass
            info["subjectNames"] = subjectNames
            return redirect('TimeLine')
    return HttpResponse(template.render(info))

def notes(request):
    template = loader.get_template('notes.html')
    # send_mail("hrp2121228@sicsr.ac.in", "Hello World")
    if request.method == 'POST':
        loggedUser = request.POST["hiddenVar"]
        title = request.POST["title"]
        desc = request.POST["description"]
        uploadedFor = request.POST.getlist("uploadedFor")
        uploadedOn = current_datetime
        myfile = request.FILES['file-upload-field']
        fs = FileSystemStorage(location=settings.BASE_DIR/"static/notesFolder/")
        filename = fs.save(myfile.name, myfile)
        storeFile = notesFile(title = title, 
                              desc = desc, 
                              originalName = myfile.name, 
                              createdName = filename, 
                              fileLocation = f"./notesFolder/{filename}", 
                              uploadedFor = uploadedFor, 
                              uploadedOn = uploadedOn, 
                              uploadedBy = loggedUser)
        storeFile.save()
        return redirect("notes")
    return HttpResponse(template.render())

