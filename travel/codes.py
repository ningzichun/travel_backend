from django.http import HttpResponse,HttpResponseForbidden
import json
import logging
logger = logging.getLogger('django')
def return403(str):
    logger.info(str)
    return HttpResponse('{"code":403,"msg":"%s"}' % str, content_type='application/json')
def return200(str):
    return HttpResponse('{"code":200,"msg":"%s"}' % str, content_type='application/json')
def returnList(list):
    return_data = {
        'code' : 200,
        'msg' : '获取成功',
        'data' : list
    }
    return HttpResponse(json.dumps(return_data,ensure_ascii=False), content_type='application/json')

def sendMail(target_addr,title,content):
    smtp_server = 'smtp.exmail.qq.com'
    from_addr = 'send@mrning.com'
    password = 'zsMM2!'
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From']=formataddr(["TravelLog",from_addr])
    msg['To']=formataddr(["User",target_addr]) 
    msg['Subject'] = Header(title, 'utf-8').encode()
    #server = smtplib.SMTP(smtp_server, 25)
    #server.starttls()
    server=smtplib.SMTP_SSL(smtp_server, 465)
    #server.set_debuglevel(1)
    try:
        server.login(from_addr, password)
        server.sendmail(from_addr, [target_addr], msg.as_string())
        server.quit()
    except Exception as e:
        return repr(e)
    return 'OK'

def sendSMS(phone,content):
    return False