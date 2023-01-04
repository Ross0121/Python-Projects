#try and except blocks contain required comments
def attendance_report():

    
    try: 
        rollNo = [str(i) for i in regStuds['Roll No']]
    except:
        print("ERROR in obtaining list of registered students")
    
    try:
        dateList = list({datetime.strptime(str(i).split(" ")[0],"%d-%m-%Y").date() for i in df['Timestamp']  if datetime.strptime(str(i).split(" ")[0],"%d-%m-%Y").strftime('%a') in ['Mon','Thu']})
        dateList.sort()
    except:
        print("ERROR in obtaining list of registered students")

    try:   
        duplicate = {date : {} for date in dateList}
        dupInf = {rollNumber : {date.strftime('%d-%m-%Y') : 0 for date in dateList} for rollNumber in rollNo}
        attendedDates = {rollNumber : [] for rollNumber in rollNo}
        fakeAttendence=[]
        fakeInfo = {rollNumber : {date.strftime('%d-%m-%Y') : 0 for date in dateList} for rollNumber in rollNo}
    except:
        print("ERROR in Dictionary creation")

    try:
        for i in range(len(df['Timestamp'])):
            dateObj = datetime.strptime(str(df['Timestamp'][i]), '%d-%m-%Y %H:%M')
            date = dateObj.date()
            #Check if the person attended the class on monday or thursday
            if dateObj.weekday() == 0 or dateObj.weekday() == 3:
                if(dateObj.hour<14 or dateObj.hour>=15):
                    fakeAttendence.append((str(df['Attendance'][i])).split(" ")[0])
                    fakeInfo[(str(df['Attendance'][i])).split(" ")[0]][date.strftime('%d-%m-%Y')]+=1
                if(dateObj.hour==14):
                    studentRollNo=(str(df['Attendance'][i])).split(" ")[0]
                    if studentRollNo == 'nan' or studentRollNo not in rollNo:
                        continue
                    if studentRollNo in duplicate[date]:
                        duplicate[date][studentRollNo]['entries'].append(dateObj)
                        dupInf[(str(df['Attendance'][i])).split(" ")[0]][date.strftime('%d-%m-%Y')]+=1
                    else:
                        duplicate[date][studentRollNo] = {'name': df['Attendance'][i].split(' ', 1)[1], 'entries': [dateObj]}
                        attendedDates[studentRollNo].append(date.strftime('%d-%m-%Y'))
                        actualAttendance.append(studentRollNo)       
            else:
                fakeAttendence.append((str(df['Attendance'][i])).split(" ")[0])
    except:
        print("ERROR in calculating reqd attendance categories")

    try:
        for i in range(len(regStuds['Name'])):
            
            for date in dateList:
                if date.strftime('%d-%m-%Y') in attendedDates[regStuds['Roll No'][i]]:
                    atten.at[i, date.strftime('%d-%m-%Y')]='P'
                else:
                    atten.at[i, date.strftime('%d-%m-%Y')]='A'
            atten.at[i,'Actual Lecture Taken']=len(dateList)
            atten.at[i,'Total Real Attendance']=actualAttendance.count(regStuds['Roll No'][i])
            atten.at[i,'Percentage (attendance_count_actual/total_lecture_taken) 2 digit decimal']=(round((atten['Total Real Attendance'][i]/len(dateList))*100,2))
 
            individual = pd.DataFrame()
            individual.at[0, 'Date']=''
            for j,date in enumerate(dateList):
                individual.at[j+1, 'Date'] = date.strftime('%d-%m-%Y')
            individual.at[0,'Roll No'] = regStuds['Roll No'][i]
            individual.at[0,'Name'] = regStuds['Name'][i]
            individual.at[0,'total_attendance_count']=''
            individual.at[0,'Real']=actualAttendance.count(regStuds['Roll No'][i])
            individual.at[0,'Absent']=len(dateList)-actualAttendance.count(regStuds['Roll No'][i])
            for j,date in enumerate(dateList):
                individual.at[j+1,'invalid']=fakeInfo[(str(df['Attendance'][i])).split(" ")[0]][date.strftime('%d-%m-%Y')]
                individual.at[j+1, 'duplicate']=dupInf[regStuds['Roll No'][i]][date.strftime('%d-%m-%Y')]
                if date.strftime('%d-%m-%Y') in attendedDates[regStuds['Roll No'][i]]:
                    individual.at[j+1, 'Real']=1
                    individual.at[j+1, 'Absent']=0
                else:
                    individual.at[j+1, 'Absent']=1
                    individual.at[j+1, 'Real']=0
                individual.at[j+1, 'total_attendance_count']=individual.at[j+1, 'Real']+individual.at[j+1,'invalid']+individual.at[j+1, 'duplicate']
    
            try:
                individual.to_excel('output/' + regStuds['Roll No'][i] + '.xlsx',index=False)
            except PermissionError:
                print("You don't have the permission to read/write in this directory. Please grant permission or change the working directory")
    except:
        print("Error in printing reports")    
    
    
try:
    from platform import python_version
    from datetime import datetime
    start_time = datetime.now()

    ver = python_version()

    if ver == "3.8.10":
        print("Correct Version Installed")
    else:
        print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")
    import pandas as pd
    import csv
  
    regStuds=pd.read_csv("input_registered_students.csv")
    df=pd.read_csv("input_attendance.csv")
    atten=pd.DataFrame()
    atten['Roll']=regStuds['Roll No'].copy()
    atten['Name']=regStuds['Name'].copy()
    actualAttendance=[]
    attendance_report()
    atten.to_excel('./output/attendance_report_consolidated.xlsx',index=False)
except FileNotFoundError:
    
    print("File could not be found in the parent directory")
except ImportError:
    
    print("Sorry, module 'Pandas' could not be imported")
#This shall be the last lines of the code.
print("o/p file ready :]")
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
