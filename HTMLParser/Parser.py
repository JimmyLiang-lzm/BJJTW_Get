"""
模块名称：HTMLParser -> Parser
模块简述：本部分为用户个人页数据刷洗处理
主要功能：使用bs4与re库对获取的用户个人页网页页面进行数据刷洗，过滤出有用的数据
"""

from bs4 import BeautifulSoup


# 清洗特定字符串
def washer(inText: str, clearText: list):
    for ch in clearText:
        inText = inText.replace(ch, '')
    return inText


# 获取基本信息
def PGET_BaseInfo(HTMLText: str):
    feedback = {}
    try:
        # 获取账号基本信息
        soup = BeautifulSoup(HTMLText, 'html.parser')
        tmp = soup.find(id='userInfo').findChildren('td')
        feedback['姓名'] = tmp[0].text
        feedback['证件类型'] = tmp[1].text
        feedback['证件号码'] = tmp[2].text
        feedback['手机'] = tmp[3].text
        feedback['注册时间'] = tmp[4].text
    except Exception as err:
        print(err)
    return feedback


# 获取个人申请表格
def PGET_MyApply(HTMLText: str):
    feedback = {}
    try:
        # 建立美汁儿对象
        soup = BeautifulSoup(HTMLText, 'html.parser').find(id='content')
        form_tmp = soup.find_all('dl')
        # 获取表格内内容
        for dl in form_tmp:
            tmp = washer(dl.text, [' ', '\t', '\r', '\xa0'])
            tmp = tmp.split('\n')
            havetitle = ''
            for dd in tmp:
                if dd == '':
                    continue
                dtmp = dd.split('：')
                if len(dtmp) == 2:
                    if dtmp[1] == '':
                        havetitle = dtmp[0]
                        feedback[dtmp[0]] = ''
                    feedback[dtmp[0]] = dtmp[1]
                elif len(dtmp) == 1:
                    if havetitle != '':
                        feedback[havetitle] = dtmp[0]
                    else:
                        continue
                else:
                    continue
        # 通知事件
        info_tmp = ''
        for p in soup.find_all('p'):
            info_tmp += washer(p.text, [' ', '\t', '\r', '\xa0', '\n'])
        feedback['通知信息'] = info_tmp
    except Exception as err:
        print(err)
    return feedback


# 获取期数
def PGET_IssueNubers(HTMLText: str):
    feedback = []
    try:
        soup = BeautifulSoup(HTMLText, 'html.parser')
        tmp = soup.find('select', id="issueNumber").findChildren('option')
        for op in tmp:
            feedback.append(op.get('value'))
    except Exception as err:
        print(err)
    return feedback


# 普通指标摇号池编码公布
def PGET_PTCApplyCodePub(HTMLText: str):
    feedback = {'申请编码': '', '基数列表': [], '备注': ''}
    try:
        soup = BeautifulSoup(HTMLText, 'html.parser')
        feedback['申请编码'] = soup.find('input', id='applyCode').get('value')
        tmp = soup.find('div', id="resulttable").findChildren('tr')
        for tr in tmp:
            td = tr.findChildren('td')
            if len(td) == 3:
                obj = {'序号': td[0].text, '摇号基数序号': td[2].text}
                feedback['基数列表'].append(obj)
        addi = soup.find('div', id="resulttable").findChild('td', id='resultTd')
        if addi:
            feedback['备注'] = addi.text.strip()
    except Exception as err:
        print(err)
    return feedback


# 普通指标中签编码
def PGET_PTCPassCode(HTMLText: str):
    feedback = {'申请编码': '', '是否中签': False, '备注': ''}
    try:
        soup = BeautifulSoup(HTMLText, 'html.parser')
        tmp = soup.find('div', id="resulttable").findChild('td', id='resultTd')
        feedback['申请编码'] = soup.find('input', id='applyCode').get('value')
        if not tmp:
            feedback['是否中签'] = True
        feedback['备注'] = tmp.text.strip()
        print(tmp.text)
    except Exception as err:
        print(err)
    return feedback


# 个人新能源审核通过编码
def PGET_XNYApplyCodePub(HTMLText: str):
    feedback = {'申请编码': '', '编码详情': [], '备注': ''}
    try:
        soup = BeautifulSoup(HTMLText, 'html.parser')
        feedback['申请编码'] = soup.find('input', id='applyCode').get('value')
        tmp = soup.find('div', id="resulttable").findChildren('tr')
        for tr in tmp:
            td = tr.findChildren('td')
            if len(td) == 4:
                obj = {'序号': td[0].text, '编码序号': td[2].text, '轮候时间': td[3].text.strip()}
                feedback['编码详情'].append(obj)
        addi = soup.find('div', id="resulttable").findChild('td', id='resultTd')
        if addi:
            feedback['备注'] = addi.text.strip()
    except Exception as err:
        print(err)
    return feedback


# 个人新能源指标编码
def PGET_XNYPassCode(HTMLText: str):
    feedback = {'申请编码': '', '是否中签': False, '排位': '', '备注': ''}
    try:
        soup = BeautifulSoup(HTMLText, 'html.parser')
        tmp = soup.find('div', id="resulttable").findChild('td', id='resultTd')
        feedback['申请编码'] = soup.find('input', id='applyCode').get('value')
        if not tmp:
            feedback['是否中签'] = True
            tmp = soup.find('div', id="resulttable").findChildren('tr')[1]
            feedback['排位'] = tmp.findChildren('td')[1].text
        feedback['备注'] = tmp.text.strip()
        print(tmp.text)
    except Exception as err:
        print(err)
    return feedback
