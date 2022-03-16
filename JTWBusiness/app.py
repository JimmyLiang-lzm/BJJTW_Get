"""
模块名称：JTWBusiness -> app
模块简述：本部分为事件反馈与处理部分的开发
主要功能：使用access模块反馈的页面文本，在使用HTMLParser中的处理页面函数将
        页面中的数据打包成JSON数据包格式，本模块下的函数可以直接用这些数据
        进行显示或实现相应的事件。
-> 您可以在此处开发自己需要的功能！！！
"""

# 登陆事务处理类引入
from JTWBusiness.access import UsrRobotics
# 交通委网页数据刷洗并转换为字典函数组
from HTMLParser.Parser import *
# 导入静态资源
from JTWBusiness.static import *


# 获取登录类结构体
def UsrInit(types: int, usr: str, pwd: str):
    oc = UsrRobotics(types, usr, pwd)
    # 如果初始化成功则返回爬虫类，否则返回None
    if oc.activate():
        return oc
    else:
        return None


# 获取登录账户基本信息字典
def get_baseinfo(uobj: UsrRobotics):
    mycode = uobj.get_mycode()
    res = uobj.access('GET', JTW_URLs['mymanage'] + mycode)
    if res:
        return PGET_BaseInfo(res.text)
    else:
        return {}


# 获取个人申请表格信息字典
def get_myapply(uobj: UsrRobotics):
    mycode = uobj.get_mycode()
    res = uobj.access('GET', JTW_URLs['personal_info'] + mycode)
    if res:
        return PGET_MyApply(res.text)
    else:
        return {}


# 获取所有期数：分普通指标与新能源指标
def get_IssueNumALL(uobj: UsrRobotics, regType: str):
    res = uobj.get_QuotaPool(regType, 0)
    if res:
        return PGET_IssueNubers(res.text)
    else:
        return []


# 获取已有结果的期数：分普通指标与新能源指标
def get_IssueNumPASS(uobj: UsrRobotics, regType: str):
    res = uobj.get_QuotaPass(regType, 0)
    if res:
        return PGET_IssueNubers(res.text)
    else:
        return []


# 普通指标摇号池编码公布查询：输入你要查询的个人申请编码和期数
def get_PTCApplyCode(uobj: UsrRobotics, quotacode: str, issue_number: str):
    res = uobj.get_QuotaPool('PTC', 1, issue_number, quotacode)
    if res:
        return PGET_PTCApplyCodePub(res.text)
    else:
        return {}


# 新能源审核通过编码查询：输入你要查询的个人申请编码和期数
def get_XNYApplyCode(uobj: UsrRobotics, quotacode: str, issue_number: str):
    res = uobj.get_QuotaPool('XNY', 1, issue_number, quotacode)
    if res:
        return PGET_XNYApplyCodePub(res.text)
    else:
        return {}


# 普通指标中签编码查询：输入你要查询的个人申请编码和期数
def get_PTCPassCode(uobj: UsrRobotics, quotacode: str, issue_number: str):
    res = uobj.get_QuotaPass('PTC', 1, issue_number, quotacode)
    if res:
        return PGET_PTCPassCode(res.text)
    else:
        return {}


# 新能源指标中签编码查询：输入你要查询的个人申请编码和期数
def get_XNYPassCode(uobj: UsrRobotics, quotacode: str, issue_number: str):
    res = uobj.get_QuotaPass('XNY', 1, issue_number, quotacode)
    if res:
        return PGET_XNYPassCode(res.text)
    else:
        return {}
