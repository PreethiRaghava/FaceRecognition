import pandas as pd
import time
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import datetime


def get_time_diff_in_seconds(present_time,last_updated_time):
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date1=datetime.strptime(str(present_time).split('.')[0],datetimeFormat)
    date2=datetime.strptime(str(last_updated_time).split('.')[0],datetimeFormat)
    diff = date2-date1
    diff=diff.seconds
    return diff

################################################## email Subject  #######################################################
def overall_subject():
    Overall_subject_mail = "Employee Timesheet From " + overall_attendence["DATE"].min()+' - ' + str(datetime.now().strftime("%d-%m-%Y"))
    return Overall_subject_mail

def present_subject():
    Present_subject_mail = "Employee Timesheet On " + str(datetime.now().strftime("%d-%m-%Y"))
    return Present_subject_mail

#Overall_hr_subject_mail = "Employee Timesheet From " + str(datetime.now().strftime("%d-%m-%Y"))
#Present_hr_subject_mail = "Employee Timesheet On " + str(datetime.now().strftime("%d-%m-%Y"))

################################################## email body  ##########################################################
def overall_body():
    Overall_body_mail = 'Dear Sir,'+'\n'+'\n'+'\n'+'Please find the attachment of Employee Timesheet From '+overall_attendence["DATE"].min()+' - '+str(datetime.now().strftime("%d-%m-%Y"))+'.\n\n\n'+'Regards,'+'\n'+'ADMS-Data Analytics'+'\n'+'\n'+'\n'+'This is an System Generated E-mail. If you have any queries Please contact to the E-mail id: sairaghava.parisa@spsoft.in'
    return Overall_body_mail

def present_body():
    Present_body_mail = 'Dear Sir,'+'\n'+'\n'+'\n'+'Please find the attachment of Employee Timesheet On '+str(datetime.now().strftime("%d-%m-%Y"))+'.\n\n\n'+'Regards,'+'\n'+'ADMS-Data Analytics'+'\n'+'\n'+'\n'+'This is an System Generated E-mail. If you have any queries Please contact to the E-mail id: sairaghava.parisa@spsoft.in'
    return Present_body_mail

#Overall_hr_body_mail = 'Dear Sir/Ma\'am,'+'\n'+'\n'+'\n'+'Please find the attachment of Employee Timesheet From '+overall_attendence["DATE"].min()+' - '+str(datetime.now().strftime("%d-%m-%Y"))+'.\n\n\n'+'Regards,'+'\n'+'ADMS-Data Analytics'
#Present_hr_body_mail = 'Dear Sir/Ma\'am,'+'\n'+'\n'+'\n'+'Please find the attachment of Employee Timesheet On '+str(datetime.now().strftime("%d-%m-%Y"))+'.\n\n\n'+'Regards,'+'\n'+'ADMS-Data Analytics'

start_time =pd.to_datetime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

from_address="preethi.polamoni@spsoft.in"
names_send_dict={"ADMS-Data Analytics":"preethi.polamoni@spsoft.in","Java":"sairaghava.parisa@spsoft.in",
                 "Rockwell":"uday.baidoddi@spsoft.in","Project Leader":"vasanthrao.kobbana@spsoft.in",
                 "S/W Development":"gopikrishna.perumandla@spsoftglobal.com"}


def get_mail(name):
    return names_send_dict.get(name)

while True:
    present_time= pd.to_datetime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    counter_time_in_seconds=get_time_diff_in_seconds(start_time,present_time)
    email_send_time_counter_hours=counter_time_in_seconds/3600

    #recipient_email_list=["sairaghava.parisa@spsoft.in","vasanthrao.kobbana@spsoft.in","uday.baidoddi@spsoft.in","gopikrishna.perumandla@spsoftglobal.com","preethi.polamoni@spsoft.in"]
    if (email_send_time_counter_hours==1):
        get_scheduledata()
        #time.sleep(60)
        overall_attendence=pd.read_csv('overall_attendence.csv')
        #present_day=pd.read_csv('present_day.csv')
        
        username = from_address
        password = 'spsoft@123'
        
############################################ email body and Overall Attachment  #########################################
        
        for key in names_send_dict.keys():
            #filter_by_name=overall_attendence[overall_attendence['Department']==str(key)]
            #filter_by_name.to_csv("overall_attendence_dept.csv")
            msg = MIMEMultipart()
            msg["From"] = from_address
            to_address =get_mail(key)
            #print(to_address)
            msg["To"] = to_address
            msg["Subject"] = overall_subject()
                        
            body = overall_body()
            body = MIMEText(body) # convert the body to a MIME compatible string
            msg.attach(body)
            
            attachment_path_1='overall_attendence_final.csv'
            attachment_1 = MIMEBase('application', "octet-stream")
            attachment_1.set_payload(open(attachment_path_1, "rb").read())
            encoders.encode_base64(attachment_1)
            attachment_1.add_header('Content-Disposition', 'attachment', filename= str(datetime.now().strftime("%d-%m-%Y"))+' overall_attendence.csv') 
            msg.attach(attachment_1)
            
            server = smtplib.SMTP('sg3plvcpnl208309.prod.sin3.secureserver.net')
            server.starttls()
            server.login(username,password)
            server.sendmail(from_address,to_address,msg.as_string())
            server.quit()

########################################### email body and Present Attachment  #########################################

        for key in names_send_dict.keys():
            #filter_by_name1=present_day[present_day['Department']==str(key)]
            #filter_by_name1.to_csv("present_day_dept.csv")
            msg = MIMEMultipart()
            msg["From"] = from_address
            to_address =get_mail(key)
            msg["To"] = to_address
            msg["Subject"] = Present_subject_mail
                      
            body = Present_body_mail
            body = MIMEText(body) # convert the body to a MIME compatible string
            msg.attach(body)
            
            attachment_path_2='present_day_attdence.csv'
            attachment_2 = MIMEBase('application', "octet-stream")
            attachment_2.set_payload(open(attachment_path_2, "rb").read())
            encoders.encode_base64(attachment_1)
            attachment_2.add_header('Content-Disposition', 'attachment', filename= str(datetime.now().strftime("%d-%m-%Y"))+' present_attendence_by_name.csv') 
            msg.attach(attachment_2)
            
            server = smtplib.SMTP('sg3plvcpnl208309.prod.sin3.secureserver.net')
            server.starttls()
            server.login(username,password)
            Server.sendmail(from_address,to_address,msg.as_string())
            server.quit()
            
############################################# HR email with Overall Attachment ##########################################
            
#         hr_mail= "gopikrishna.perumandla@spsoftglobal.com"
#         msg = MIMEMultipart()
        
#         msg["From"] = from_address
#         msg["To"] = hr_mail
#         msg["Subject"] = Overall_hr_subject_mail

#         body = Overall_hr_subject_mail
#         body = MIMEText(body) 
#         msg.attach(body)
        
#         attachment_path_3='overall_attendence.csv'
#         attachment_3 = MIMEBase('application', "octet-stream")
#         attachment_3.set_payload(open(attachment_path_3, "rb").read())
#         encoders.encode_base64(attachment_3)
#         attachment_3.add_header('Content-Disposition', 'attachment', filename= str(datetime.now().strftime("%d-%m-%Y"))+' overall_attendence_timeSheet.csv')
#         msg.attach(attachment_3)
        
#         server = smtplib.SMTP('sg3plvcpnl208309.prod.sin3.secureserver.net')
#         server.starttls()
#         server.login(username,password)
#         server.sendmail(from_address,hr_mail,msg.as_string())
#         server.quit()

# ############################################# HR email with Present Attachment ##########################################

#         #hr_mail1= "gopikrishna.perumandla@spsoftglobal.com"
#         msg = MIMEMultipart()
        
#         msg["From"] = from_address
#         msg["To"] = hr_mail
#         msg["Subject"] = Present_hr_subject_mail
        
#         body = Present_hr_body_mail
#         body = MIMEText(body) 
#         msg.attach(body)
        
#         attachment_path_4='present_day.csv'
#         attachment_4 = MIMEBase('application', "octet-stream")
#         attachment_4.set_payload(open(attachment_path_4, "rb").read())
#         encoders.encode_base64(attachment_2)
#         attachment_4.add_header('Content-Disposition', 'attachment', filename= str(datetime.now().strftime("%d-%m-%Y"))+' Present_day_attendence_timeSheet.csv') 
#         msg.attach(attachment_4)
        
#         server = smtplib.SMTP('sg3plvcpnl208309.prod.sin3.secureserver.net')
#         server.starttls()
#         server.login(username,password)
#         server.sendmail(from_address,hr_mail,msg.as_string())
#         server.quit()
        
        start_time=present_time
