"""
模块名称：JTWBusiness -> access
模块简述：本部分为网站爬虫机器人登录处理事件类
主要功能：突破交通委反爬虫系统并登录到用户内部，外部模块使用为requests、ddddocr。
        鸣谢爬虫大佬sml2h3的验证码突破协助！！！！
"""

import time
import requests
import random
from ddddocr import DdddOcr

# 引入URL
from JTWBusiness.static import *


# 用户机器人类
class UsrRobotics(object):
    # 初始化登录
    def __init__(self, types: int = 0, usr: str = '', pwd: str = ''):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.190 Safari/537.36',
        }
        self.OCR = DdddOcr(show_ad=False)
        self.my_code = ''
        self.UsrSession = requests.session()
        self.UsrSession.headers.update(self.header)
        self.types = types
        self.usr = usr
        self.pwd = pwd
        self.first = True

    # 激活/重载该用户登录状态
    def activate(self):
        try:
            self.UsrSession.get(JTW_URLs['index'], timeout=(5, 5))
            tmp = self.jtw_login()
            if tmp['code']:
                raise Exception('Access Deny！')
            self.my_code = tmp['scode']
            self.UsrSession.get(tmp['redir_url'], timeout=(5, 5))
            if self.first:
                print('成功激活该成员！')
                self.first = False
            else:
                print('重新登录用户……')
            return True
        except Exception as err:
            print('发生错误：', err)
            return False

    # 登录/表单验证码突破
    def get_lvcode(self):
        vt = 1
        res_str = ''
        while vt <= 5:
            try:
                pic = self.UsrSession.get(JTW_URLs['lvcode_img'], timeout=(5, 5),
                                          params={'ee': str(vt)})
                print('图片验证码Session：', pic.cookies)
                # 识别图片
                res_str = self.OCR.classification(pic.content)
                print("识别的验证码为：", res_str)
                # 验证验证码是否正确
                para = {'validCode': res_str, 'jsonpCallback': 'mycallback', 'name': 'value',
                        '_': str(int(round(time.time() * 1000)))}
                res = self.UsrSession.get(JTW_URLs['lvcode_verify'], timeout=(5, 5), params=para)
                print("验证反馈：", res.text)
                if 'true' in res.text:
                    print('验证码正确！')
                    break
                else:
                    raise Exception('验证码识别有误！')
            except Exception as err:
                print('验证码识别出现错误：', err)
                vt += 1
            st = random.uniform(0.0, 1.5)
            print('Program Will Sleep in %0.2f Sec.' % st)
            time.sleep(st)
        if vt > 5:
            return ''
        return res_str

    """
    # 成员登录
        0：个人用户登录，1：企业用户手机号登录（非营运），2：企业用户机构代码登录（非营运），
        3：事业单位及其他手机号登录，4：事业单位及其他机构代码登录，5：个体用户手机号登录（营运），
        6：企业用户手机号登录（营运），7：企业用户机构代码登录（营运）
    """
    def jtw_login(self) -> dict:
        # 初始化表单字典
        form_data = LOGIN_FORM
        feedback = {'code': 0}
        # 个人用户登录
        if self.types == 0:
            form_data['personMobile'] = self.usr
            form_data['password'] = self.pwd
        # 企业用户手机号登录（非营运）
        elif self.types == 1:
            form_data['userType'] = '1'
            form_data['userTypeSelect'] = '1'
            form_data['unitMobile'] = self.usr
            form_data['password'] = self.pwd
        # 企业用户机构代码登录（非营运）
        elif self.types == 2:
            form_data['userType'] = '1'
            form_data['userTypeSelect'] = '1'
            form_data['unitLoginTypeSelect'] = '1'
            form_data['loginType'] = 'ORGCODE'
            form_data['orgCode'] = self.usr
            form_data['password'] = self.pwd
        # 事业单位及其他手机号登录
        elif self.types == 3:
            form_data['userType'] = '2'
            form_data['userTypeSelect'] = '2'
            form_data['unitMobile'] = self.usr
            form_data['password'] = self.pwd
        # 事业单位及其他机构代码登录
        elif self.types == 4:
            form_data['userType'] = '2'
            form_data['userTypeSelect'] = '2'
            form_data['unitLoginTypeSelect'] = '1'
            form_data['loginType'] = 'ORGCODE'
            form_data['orgCode'] = self.usr
            form_data['password'] = self.pwd
        # 个体用户手机号登录（营运）
        elif self.types == 5:
            form_data['userType'] = '3'
            form_data['userTypeSelect'] = '0'
            form_data['serviceType'] = '0'
            form_data['personMobile'] = self.usr
            form_data['password'] = self.pwd
        # 企业用户手机号登录（营运）
        elif self.types == 6:
            form_data['userType'] = '4'
            form_data['userTypeSelect'] = '1'
            form_data['serviceUserTypeSelect'] = '1'
            form_data['serviceType'] = '0'
            form_data['unitMobile'] = self.usr
            form_data['password'] = self.pwd
        # 企业用户机构代码登录（营运）
        elif self.types == 7:
            form_data['userType'] = '4'
            form_data['serviceUserTypeSelect'] = '1'
            form_data['serviceType'] = '0'
            form_data['unitLoginTypeSelect'] = '1'
            form_data['loginType'] = 'ORGCODE'
            form_data['orgCode'] = self.usr
            form_data['password'] = self.pwd
        # 其他未识别的类型
        else:
            feedback['err'] = '未定义表单类型！'
            feedback['code'] = 2
            return feedback
        # 破解验证码
        form_data['validCode'] = self.get_lvcode()
        # 发送表单数据
        try:
            res_post = self.UsrSession.post(JTW_URLs['login'], timeout=(5, 5), data=form_data)
            res = res_post.json()
            feedback['redir_url'] = res['rediectUrl']
            feedback['scode'] = res['rediectUrl'].split('/')[-1]
        except Exception as err:
            print(err)
            feedback['code'] = 1
            feedback['err'] = str(err)
            return feedback
        return feedback

    # 自动访问函数
    def access(self, method: str, url: str, **para):
        st = 0
        while st <= 5:
            try:
                if method == 'GET':
                    res = self.UsrSession.get(url, timeout=(5, 5), **para)
                elif method == 'POST':
                    res = self.UsrSession.post(url, timeout=(5, 5), **para)
                else:
                    return None
                redi_his = res.history
                # print(len(redi_his), redi_his)
                # 判断是否发生重映射，并判断是否登录失败
                if len(redi_his) > 0:
                    # print(redi_his[-1].status_code, redi_his[-1].headers.get('location'))
                    if (redi_his[-1].status_code != 200) and (
                            'xkczb.jtw.beijing.gov.cn?message=' in redi_his[-1].headers.get('location')):
                        raise Exception('NoLogin')
                return res
            except Exception as err:
                print(type(err), err)
                if str(err) == 'NoLogin':
                    self.activate()
                st += 1
        return None

    # 测试显示反馈文本
    def test_show(self, method: str, url: str, **para):
        res = self.access(method, url, **para)
        if res:
            print(res.text)
        else:
            print(res)

    # 重载该用户信息
    def reload_usrInfo(self, types: int = 0, usr: str = '', pwd: str = '', do_now: bool = False):
        self.my_code = ''
        self.UsrSession = requests.session()
        self.UsrSession.headers.update(self.header)
        self.types = types
        self.usr = usr
        self.pwd = pwd
        self.first = True
        if do_now:
            self.activate()
        return 0

    # 退出用户登录状态
    def deactivate(self):
        try:
            self.UsrSession.get(JTW_URLs['logout'], timeout=(5, 5))
            print('您已经成功退出登录状态！')
        except Exception as err:
            print('退出登录状态失败：', err)

    # 获取该设备唯一标识码
    def get_mycode(self):
        return self.my_code

    # 摇号池信息获取
    def get_QuotaPool(self, regType: str, method: int, iN: str = '', aC: str = '', pn: int = 1):
        if method == 0:
            param = {'regType': regType}
            res = self.access('GET', JTW_URLs['QuotaPool'] + self.my_code, params=param)
            return res
        elif method == 1:
            datas = {'pageNo': str(pn), 'regType': regType, 'issueNumber': iN, 'applyCode': aC,
                     'validCode': self.get_lvcode()}
            res = self.access('POST', JTW_URLs['QuotaPool'] + self.my_code, data=datas)
            return res
        else:
            return None

    # 摇号中签信息获取
    def get_QuotaPass(self, regType: str, method: int, iN: str = '', aC: str = '', pn: int = 1):
        if method == 0:
            param = {'regType': regType}
            res = self.access('GET', JTW_URLs['QuotaPass'] + self.my_code, params=param)
            return res
        elif method == 1:
            datas = {'pageNo': str(pn), 'regType': regType, 'issueNumber': iN, 'applyCode': aC,
                     'validCode': self.get_lvcode()}
            res = self.access('POST', JTW_URLs['QuotaPass'] + self.my_code, data=datas)
            return res
        else:
            return None
