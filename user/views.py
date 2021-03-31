from django.shortcuts import render
from travel.codes import return200,return403,returnList,sendMail,sendSMS
import os
import hashlib
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from user.models import User
from django.http import HttpResponse
import random
import base64

# Create your views here.
def index(request):
    return render(request,'user.html')

def login(request,use_captcha=1):
    no_captcha = request.POST.get("no_captcha")
    if(no_captcha):
        use_captcha=0
    if request.method == "GET":
        return return403('请使用 POST 请求')
    uid = request.POST.get("uid")
    uname = request.POST.get("uname")
    phone = request.POST.get("phone")
    user = request.POST.get("user")
    email = request.POST.get("email")
    password = request.POST.get("password")
    captcha = request.POST.get("captcha")
    session_captcha=request.session.get('captcha',None)
    #print('session:'+request.session.session_key+' ,login:'+captcha)
    if not password:
        return return403('无效参数')
    if(use_captcha):
        if not captcha:
            return return403('请输入验证码')
        if not session_captcha:
            return return403('未获取验证码')
        if request.session["captcha"]=='':
            return return403('验证码过期')
        if captcha.lower()!=session_captcha:
            return return403('验证码错误')
        request.session["captcha"]=""
    if uid:
        user_obj = User.objects.filter(uid=uid).first()
    elif uname:
        user_obj = User.objects.filter(uname=uname).first()
    elif phone:
        user_obj = User.objects.filter(phone=phone).first()
    elif email :
        user_obj = User.objects.filter(email=email).first()
    elif user:
        if "@" in user:
            user_obj = User.objects.filter(email=user).first()
        elif (user.isdigit() and len(user)<10):
            user_obj = User.objects.filter(uid=user).first()
        elif (user.isdigit() and len(user)>=10):
            user_obj = User.objects.filter(phone=user).first()
        else:
            user_obj = User.objects.filter(uname=user).first()
    else:
        return return403('无效参数')
    if not user_obj:
        return return403('无此用户')
    if not user_obj.pwd == hashlib.md5(password.encode(encoding='UTF-8')).hexdigest():
        #print(user_obj.pwd)
        return return403('密码错误')
    request.session["uid"] = user_obj.uid
    request.session["uname"] = user_obj.uname

    return_data = {
        'uid' : user_obj.uid,
        'uname' : user_obj.uname,
        'phone' : user_obj.phone,
        'email' : user_obj.email,
        'gender' : user_obj.gender,
        'intro' : user_obj.intro,
        'avatar' : '/media/'+user_obj.avatar.name
    }

    return returnList(return_data)


def logout(request):
    request.session.flush()
    return return200('已清除登录信息')

def register(request,use_captcha=1):
    no_captcha = request.POST.get("no_captcha")
    if(no_captcha):
        use_captcha=0
    uname = request.POST.get("uname")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    password = request.POST.get("password")
    captcha = request.POST.get("captcha")
    session_captcha=request.session.get('captcha',None)
    if(use_captcha):
        if not captcha:
            return return403('请输入验证码')
        if not session_captcha:
            return return403('未获取验证码')
        if session_captcha=='':
            return return403('验证码过期')
        if captcha.lower()!=session_captcha:
            return return403('验证码错误')
        request.session["captcha"] = ''
    if not (uname and password):
        return return403('无效参数：缺少用户名或密码')
    if uname.isdigit():
        return return403('用户名不能全为数字')
    if (phone and len(phone)<10):
        return return403('手机号格式不正确')
    string = "~!@#$%^&*()_+-*/<>,.[]\/"
    for i in string:
        if i in uname:
            return return403('用户名包含特殊字符')
    if User.objects.filter(uname=uname).first():
        return return403('用户名已存在')
    if phone:
        if User.objects.filter(phone=phone).first():
            return return403('手机号已存在')
    if email:
        if User.objects.filter(email=email).first():
            return return403('邮箱已存在')
    else:
        return return403('无效参数：缺少手机或邮箱')
    user_obj = User(uname=uname,pwd=hashlib.md5(password.encode(encoding='UTF-8')).hexdigest(),email=email,phone=phone)
    user_obj.save()
    return return200('注册成功')

def modPwd(request):
    if request.method == "GET":
        return return403('请使用 POST 请求')
    oldPwd = request.POST.get("old_password")
    newPwd = request.POST.get("new_password")
    if not (oldPwd and newPwd):
        return return403('无效参数')
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    user_obj = User.objects.filter(uid=uid).first()
    if not user_obj:
        return return403('无此用户') #待测试
    checkOldPwd=hashlib.md5(oldPwd.encode(encoding='UTF-8')).hexdigest()
    if(checkOldPwd != user_obj.pwd):
        return return403('旧密码错误')
    user_obj.pwd = hashlib.md5(newPwd.encode(encoding='UTF-8')).hexdigest()
    user_obj.save()
    return return200('成功地修改了密码')

def updateInfo(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    user_obj = User.objects.filter(uid=uid).first()
    if not user_obj:
        return return403('无此用户')
    
    if request.method == "POST":
        gender = request.POST.get("gender")
        intro = request.POST.get("intro")
        if gender:
            user_obj.gender=gender
        if intro:
            user_obj.intro=intro
        user_obj.save()
    
    return_data = {
        'uid' : user_obj.uid,
        'uname' : user_obj.uname,
        'phone' : user_obj.phone,
        'email' : user_obj.email,
        'gender' : user_obj.gender,
        'intro' : user_obj.intro,
        'avatar' : '/media/'+user_obj.avatar.name
    }
    return returnList(return_data)
    
def uploadAvatar(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')

    avatar = request.FILES.get('avatar',None)
    if not avatar:
        return return403('未获取到avatar')
    f, e = os.path.splitext(avatar.name)
    imgName=str(uid)+e
    avatar.name = imgName
    ''' # 图片规整化
    if e!='.jpg':
        return return403('仅接受.JPG')
    avatar.name = imgName
    im = Image.open(avatar)
    width, height = im.size
    if width>512 or height>512 :
        if width>512:
            rate=128/width
            height=int(height*rate)
            width=128
        if height>512:
            rate=128/height
            width=int(width*rate)
            height=128
        im = im.resize((width,height),Image.ANTIALIAS)
    #image.save()
    '''
    user_obj = User.objects.filter(uid = uid).first()
    if os.path.isfile(user_obj.avatar.path): #删除已经存在的图片
        if 'default' not in user_obj.avatar.path:
            os.remove(user_obj.avatar.path)
    user_obj.avatar = avatar
    user_obj.save()
    return return200('成功地修改了头像')

def check_code(width=90, height=40, char_length=4):  
    from travel.load_files import font,font_size
    #print(os.path.isfile('kumo.tff'))
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        # 生成随机字符（包括大小写字母和数字）
        ranNum = str(random.randint(0, 9))
        #ranLower = chr(random.randint(65, 90))
        #ranUpper = chr(random.randint(97, 120))
        #return random.choice([ranNum, ranLower, ranUpper])
        return ranNum

    def rndColor():
        # 生成随机颜色
        return (random.randint(0, 200), random.randint(10, 200), random.randint(64, 200))

    # 写文字
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = ( height - font_size ) / 2
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    # 对图像加滤波 - 深度边缘增强滤波
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  
    return img, ''.join(code)

def getCAPTCHA(request):
    if not request.session.session_key:
        request.session.create()
    #print(os.getcwd())
    img,captcha = check_code()
    stream = BytesIO()
    img.save(stream, 'png')
    base64_img = base64.b64encode(stream.getvalue()).decode()
    request.session["captcha"] = captcha.lower()
    return_data = [
        {
            "index" : 1,
            'img' : base64_img
        }
    ]
    #print('session:'+request.session.session_key+' ,code:'+captcha)
    return returnList(return_data)
    #return HttpResponse('<img src="data:image/png;base64,'+base64_img+'"/>')
    
    #base64_data = base64.b64encode(f.read())
    #return HttpResponse(stream.getvalue(), content_type='image/png')
   

def sendCodeMail(target_addr,code):
    title='TravelLog密码重置验证码'
    content='您好！<br>请使用以下代码完成验证：<b>%s</b><br>TravelLog'% code
    return sendMail(target_addr,title,content)

def sendCodePhone(target_addr,code):
    content='您的TravelLog密码重置验证码为：%s。'% code
    return sendSMS(target_addr,content)


def resetPwd(request,use_captcha=1):
    no_captcha = request.POST.get("no_captcha")
    if(no_captcha):
        use_captcha=0
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    code = request.POST.get("code")
    captcha = request.POST.get("captcha")
    newPwd = request.POST.get("new_password")
    session_captcha=request.session.get('captcha',None)
    if(use_captcha):
        if not captcha:
            return return403('请输入验证码')
        if not session_captcha:
            return return403('未获取验证码')
        if session_captcha=='':
            return return403('验证码过期')
        if captcha.lower()!=session_captcha:
            return return403('验证码错误')
    if (email or phone):  #步骤1：获取密保恢复码
        
        code = str(int(random.random()*1000000)).rjust(6,'0')
        #搜索用户
        if email:
            request.session['rec_method']='email'
            user_obj = User.objects.filter(email=email).first()
            if not user_obj:
                if use_captcha:
                    request.session["captcha"]='' #清除CAPTCHA
                return return403('找不到用户')
            request.session['rec_user']=email
            sendMailReturnCode=sendCodeMail(email,code)
            if sendMailReturnCode!='OK':
                return return403('发送邮件失败：'+sendMailReturnCode)
            request.session['code']=code
            return return200('已发送恢复码至邮箱')
        if phone:
            request.session['rec_method']='phone'
            user_obj = User.objects.filter(phone=phone).first()
            if not user_obj:
                if use_captcha:
                    request.session["captcha"]='' #清除CAPTCHA
                return return403('找不到用户')
            request.session['rec_user']=phone
            if not sendCodePhone(phone,code):
                return return403('发送短信失败')
            request.session['code']=code
            return return200('已发送恢复码至手机')
        
    elif code:    #步骤2：验证验证码
        session_code=request.session.get('code',None)
        if not session_code:
            return return403('未获取恢复码或已失效')
        if not (newPwd and code):
            return return403('参数错误')
        if code!=request.session['code']:
            if use_captcha:
                request.session["captcha"]='' #清除CAPTCHA
            return return403('恢复码错误')
        if request.session['rec_method']=='email':
            user_obj = User.objects.filter(email=request.session['rec_user']).first()
            user_obj.pwd = hashlib.md5(newPwd.encode(encoding='UTF-8')).hexdigest()
            user_obj.save()
        if request.session['rec_method']=='phone':
            user_obj = User.objects.filter(phone=request.session['rec_user']).first()
            user_obj.pwd = hashlib.md5(newPwd.encode(encoding='UTF-8')).hexdigest()
            user_obj.save()
        request.session['code']=''
        return return200('修改成功')
    else:
        return return403('参数错误')