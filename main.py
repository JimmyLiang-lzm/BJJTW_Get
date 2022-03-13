from io import BytesIO
import time
import requests
import random
from PIL import Image
from ddddocr import DdddOcr

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.190 Safari/537.36',
}

OCR = DdddOcr(show_ad=False)
my_code = {}

# 首页url：https://xkczb.jtw.beijing.gov.cn/
# 验证码获取url：https://apply.jtw.beijing.gov.cn/apply/app/common/validCodeImage?ee=1
# 登录url：https://apply.jtw.beijing.gov.cn/apply/app/common/person/login
# 返回重映射json，重映射地址url在“rediectUrl”中，一般为：https://apply.jtw.beijing.gov.cn/apply/app/user/person/manage/(唯一session编码)
# 我的个人申请url：https://apply.jtw.beijing.gov.cn/apply/app/user/person/choosePerson/(唯一session编码)

session = requests.session()
session.get('https://xkczb.jtw.beijing.gov.cn/', headers=header)


def GET_VCode():
    global session, header, OCR
    vt = 1
    res_str = ''
    while vt <= 5:
        try:
            pic = session.get(f'https://apply.jtw.beijing.gov.cn/apply/app/common/validCodeImage?ee={vt}',
                              headers=header, timeout=(5, 10))
            img = Image.open(BytesIO(pic.content))
            print('验证码图片长宽：%d * %d' % img.size)
            print('图片验证码Session：', pic.cookies)
            # 识别图片
            res_str = OCR.classification(pic.content)
            print("识别的验证码为：", res_str)
            # 验证验证码是否正确
            para = {'validCode': res_str, 'jsonpCallback': 'mycallback', 'name': 'value',
                    '_': str(int(round(time.time() * 1000)))}
            res = session.get('https://apply.jtw.beijing.gov.cn/apply/app/common/checkValidCode',
                              headers=header, timeout=(5, 10), params=para)
            print("验证反馈：", res.text)
            if 'true' in res.text:
                print('验证码正确！')
                break
            else:
                img.show()
                raise Exception('验证码识别有误！')
        except Exception as err:
            print('验证码识别出现错误：', err)
            vt += 1
        st = random.uniform(3.5, 6.5)
        print('Program Will Sleep in {} Sec.'.format(st))
        time.sleep(st)
    if vt > 5:
        return ''
    return res_str


def jtw_login(types=0, usr='', pwd='', vcode='') -> dict:
    global session, header
    form_data = {
        'userType': '0',
        'ranStr': '',
        'userTypeSelect': '0',
        'serviceUserTypeSelect': '0',
        'serviceType': '1',
        'personMobile': '',
        'unitLoginTypeSelect': '0',
        'loginType': 'MOBILE',
        'unitMobile': '',
        'orgCode': '',
        'password': '',
        'pin': '',
        'validCode': '',
    }
    feedback = {'code': 0}
    # 个人用户/非营运车
    if types == 0:
        form_data['personMobile'] = usr
        form_data['password'] = pwd
        form_data['validCode'] = vcode
    else:
        feedback['err'] = '未定义表单类型！'
        feedback['code'] = 2
        return feedback
    try:
        res_post = session.post('https://apply.jtw.beijing.gov.cn/apply/app/common/person/login',
                                headers=header, timeout=(5, 10), data=form_data)
        res = res_post.json()
        feedback['redir_url'] = res['rediectUrl']
        feedback['scode'] = res['rediectUrl'].split('/')[-1]
    except Exception as err:
        print(err)
        feedback['code'] = 1
        feedback['err'] = str(err)
        return feedback
    return feedback


def Get_UsrMenu():
    vcode = GET_VCode()
    if vcode == '':
        return False
    global session, header, my_code
    my_code = jtw_login(0, '15650788101', '@1999123lzm', vcode)
    if my_code['code']:
        return False
    res = session.get(my_code['redir_url'], headers=header, timeout=(5, 10))
    return res.text


def Get_PersonalApply(mcode: str = ''):
    global session, header
    req_url = 'https://apply.jtw.beijing.gov.cn/apply/app/user/person/choosePerson/' + mcode
    res = session.get(req_url, headers=header, timeout=(5, 10))
    return res.text


if __name__ == '__main__':
    Get_UsrMenu()
    time.sleep(2)
    Get_PersonalApply(my_code['scode'])

