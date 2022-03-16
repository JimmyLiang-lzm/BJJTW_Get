"""
注意：这是本框架的使用范例
功能：完整的输出爬取的所有信息
"""

import getpass
import datetime
from JTWBusiness.app import *


# 字典显示函数
def show_dict(obj, k: int = -1):
    if isinstance(obj, dict):
        k += 1
        for d in obj:
            for _ in range(k):
                print('     ', end='')
            if isinstance(obj[d], dict):
                print(d, ':')
                show_dict(obj[d], k)
            elif isinstance(obj[d], list):
                print(d, ':')
                show_dict(obj[d], k+1)
            else:
                print(d, ':', obj[d])
    elif isinstance(obj, list):
        for _ in range(k):
            print('     ', end='')
        for l in obj:
            if isinstance(l, (dict, list)):
                show_dict(l, k)
            else:
                print(l, end=' ')
        print('')


usr_login_info = '0 -> 个人用户登录\n' \
                 '1 -> 企业用户手机号登录（非营运）\n' \
                 '2 -> 企业用户机构代码登录（非营运）\n' \
                 '3 -> 事业单位及其他手机号登录\n' \
                 '4 -> 事业单位及其他机构代码登录\n' \
                 '5 -> 个体用户手机号登录（营运）\n' \
                 '6 -> 企业用户手机号登录（营运）\n' \
                 '7 -> 企业用户机构代码登录（营运）\n'

if __name__ == '__main__':
    print('========欢迎使用北京市小客车指标调控管理信息系统爬虫程序========')
    print(usr_login_info)
    # 用户输入
    in_type = int(input('输入您的账户类型：'))
    user = input('输入您的账号：')
    password = getpass.getpass('输入您的密码：')

    # 计时器开始
    st = datetime.datetime.now()

    # 登录账号并得到爬虫结构体
    oc = UsrInit(in_type, user, password)

    # 构建反馈字典
    feedDict = {}

    # 判断是否正常登录
    if not oc:
        print('登录失败！')
    else:

        # 若登录成功进行全部数据获取
        print('爬虫正在工作，请稍等片刻……')
        # 初始化变量
        v = 0
        my_apply_code = ''
        ptc_latest_issue_number = ''
        xny_latest_issue_number = ''
        ptc_latest_pass_number = ''
        xny_latest_pass_number = ''

        # 获取登录账户基本信息
        feedDict['账户基本信息'] = get_baseinfo(oc)

        # 获取个人申请表格信息字典
        feedDict['个人申请表'] = get_myapply(oc)
        if feedDict['个人申请表']['个人申请编码']:
            my_apply_code = feedDict['个人申请表']['个人申请编码']
            v += 1

        # 获取普通指标所有期数
        feedDict['普通指标所有期数'] = get_IssueNumALL(oc, 'PTC')
        if feedDict['普通指标所有期数']:
            ptc_latest_issue_number = feedDict['普通指标所有期数'][0]
            v += 1

        # 获取新能源指标所有期数
        feedDict['新能源指标所有期数'] = get_IssueNumALL(oc, 'XNY')
        if feedDict['新能源指标所有期数']:
            xny_latest_issue_number = feedDict['新能源指标所有期数'][0]
            v += 1

        # 获取普通指标已有结果的期数
        feedDict['普通指标有结果期数'] = get_IssueNumPASS(oc, 'PTC')
        if feedDict['普通指标有结果期数']:
            ptc_latest_pass_number = feedDict['普通指标有结果期数'][0]
            v += 1

        # 获取新能源已有结果期数
        feedDict['新能源有结果期数'] = get_IssueNumPASS(oc, 'XNY')
        if feedDict['新能源有结果期数']:
            xny_latest_pass_number = feedDict['新能源有结果期数'][0]
            v += 1

        # 最新一期本账户指标资格与通过资料爬取
        if v != 5:
            print('账户爬取信息不全面，无法进行本账户指标资格查询！！')
        else:
            feedDict['普通指标资格公布'] = get_PTCApplyCode(oc, my_apply_code, ptc_latest_issue_number)
            feedDict['新能源审核通过'] = get_XNYApplyCode(oc, my_apply_code, xny_latest_issue_number)
            feedDict['普通指标中签查询'] = get_PTCPassCode(oc, my_apply_code, ptc_latest_pass_number)
            feedDict['新能源指标中签查询'] = get_XNYPassCode(oc, my_apply_code, xny_latest_pass_number)

    # 计时器停止
    et = datetime.datetime.now()
    print('=============================== 结果展示 ===============================')
    show_dict(feedDict)
    print('=======================================================================')
    print('爬取用时：', (et - st).seconds, 's')
    print('程序执行完毕！！')
