codedata = {
    '11':{'name': '北京市', 'imgs': ['beijing.png']},
    '12':{'name': '天津市', 'imgs': ['tj.png']},
    '13':{'name': '河北省', 'imgs': ['sjz.png']},
    '14':{'name': '山西省', 'imgs': ['taiyuan.png']},
    '15':{'name': '内蒙古自治区', 'imgs': ['hhht.png']},
    '21':{'name': '辽宁省', 'imgs': ['shenyang.png']},
    '22':{'name': '吉林省', 'imgs': ['changchun.png']},
    '23':{'name': '黑龙江省', 'imgs': ['heb.png']},
    '31':{'name': '上海市', 'imgs': ['sh.png']},
    '32':{'name': '江苏省', 'imgs': ['nanjing.png']},
    '33':{'name': '浙江省', 'imgs': ['hangzhou.png']},
    '34':{'name': '安徽省', 'imgs': ['anhui.png']},
    '35':{'name': '福建省', 'imgs': ['fuzhou.png']},
    '36':{'name': '江西省', 'imgs': ['nanchang.png']},
    '37':{'name': '山东省', 'imgs': ['jinan.png']},
    '41':{'name': '河南省', 'imgs': ['zhengzhou.png']},
    '42':{'name': '湖北省', 'imgs': ['wuhan.png']},
    '43':{'name': '湖南省', 'imgs': ['changsha.png']},
    '44':{'name': '广东省', 'imgs': ['guangzhou.png']},
    '45':{'name': '广西壮族自治区', 'imgs': ['nanning.png']},
    '46':{'name': '海南省', 'imgs': ['haikou.png']},
    '50':{'name': '重庆市', 'imgs': ['cq.png']},
    '51':{'name': '四川省', 'imgs': ['sichuan.png']},
    '52':{'name': '贵州省', 'imgs': ['guiyang.png']},
    '53':{'name': '云南省', 'imgs': ['kunming.png']},
    '54':{'name': '西藏自治区', 'imgs': ['lasa.png']},
    '61':{'name': '陕西省', 'imgs': ['xian.png']},
    '62':{'name': '甘肃省', 'imgs': ['lanzhou.png']},
    '63':{'name': '青海省', 'imgs': ['xining.png']},
    '64':{'name': '宁夏回族自治区', 'imgs': ['yinchuan.png']},
    '65':{'name': '新疆维吾尔自治区', 'imgs': ['wlmq.png']},
    '71':{'name': '台湾省', 'imgs': ['taibei.png']},
    '81':{'name': '香港特别行政区', 'imgs': ['xg.png']},
    '82':{'name': '澳门特别行政区', 'imgs': ['aomen.png']},
    '3702':{'name': '青岛市', 'imgs': ['qingdao.png']},
    '00':{'name': '默认值', 'imgs': ['def1.png','def2.png','def3.png','def4.png','def5.png']},
}

import random
def code2img(postcode):
    if postcode in codedata:
        return random.sample(codedata[postcode]['imgs'],1)[0]
    return False