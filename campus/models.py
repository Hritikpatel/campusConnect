from django.db import models

# Create your models here.

class loginCrad(models.Model):
    email = models.EmailField(max_length=30,null=True) # Email
    password = models.CharField(max_length=15, null=True) # setID / #EmployeeID
    isStudent = models.CharField(max_length=1, null=True) # Y, N


class student(models.Model):
    photo = models.CharField(max_length=50, null=True) # +
    dob = models.CharField(max_length=10, null=True) # 00/00/0000 = 10
    address = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=30, unique=True, null=True) # Email
    phone = models.CharField(max_length=13, null=True) 
    setID = models.CharField(max_length=9, unique=True, null=True) # 210350266
    prn = models.CharField(max_length=11, unique=True, null=True) # 21030121228
    div = models.CharField(max_length=1, null=True) # A, B, C, D...
    course = models.CharField(max_length=10, null=True) # BCA, BBA-IT
    fullname = models.CharField(max_length=20, null=True) # ABC XYZ
    subjectAlias = models.CharField(max_length=200, null=True) # "SPP, JAVA, Mobile..."
    sem = models.CharField(max_length=3) # I, II, III, IV, V, VI
    year = models.CharField(max_length=7) # 2021-24...


class teachers(models.Model):
    empid  = models.CharField(max_length=15, null=True) # EmployeeID
    fullname  = models.CharField(max_length=50, null=True) # EmployeeName
    subjectAlias = models.CharField(max_length=50, null=True) # "SPP, JAVA, Mobile..."
    email = models.EmailField(max_length=30, null=True) # Email

    
class Subjects(models.Model):
    subjectName = models.CharField(max_length=50, null=True) # Software Project Practices
    subjectType = models.CharField(max_length=50) # base(div-E), BCA(Honours), BCA Sem IV (Elective)
    subjectAlias = models.CharField(max_length=10, unique=True, null=True) # SPP: Software Project Practices, JEF:  Java Enterprise Framework,

class todo(models.Model):
    email = models.CharField(max_length=30, null=True)
    task = models.CharField(max_length=50, null=True)
    desc = models.CharField(max_length = 100)
    time = models.DateField(null=True)
    reminder = models.BooleanField(default=False, null=True)


class notesFile(models.Model):
    title = models.CharField(max_length=30, null=False)
    desc = models.CharField(max_length=30, null=False)
    originalName = models.CharField(max_length=50)
    createdName = models.CharField(max_length=50)
    fileLocation = models.CharField(max_length = 50, null=False)
    uploadedFor = models.CharField(max_length=20)
    uploadedOn = models.DateField()
    uploadedBy = models.CharField(max_length=20, null=False)

class attendanceSheets(models.Model):
    subject = models.CharField(max_length=50) #SPP
    divList = models.CharField(max_length=1, null=True) #E
    sharedBy = models.CharField(max_length=50) # Email of teacher
    urlShared = models.TextField() 
    sheetName = models.TextField()

class lectureMod(models.Model):
    head = models.CharField(max_length=100)
    start = models.CharField(max_length=25)
    end = models.CharField(max_length=25)
    changedFor = models.CharField(max_length=25)




# TODO 