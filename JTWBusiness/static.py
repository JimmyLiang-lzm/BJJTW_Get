"""
本文件为北京交通委摇号程序各个URL的定义文件
请勿随便更改此文件！！！
"""

JTW_URLs = {
    'index': 'https://xkczb.jtw.beijing.gov.cn/',
    'login': 'https://apply.jtw.beijing.gov.cn/apply/app/common/person/login',
    'lvcode_img': 'https://apply.jtw.beijing.gov.cn/apply/app/common/validCodeImage',  # 带参数ee=（获取次数）
    'lvcode_verify': 'https://apply.jtw.beijing.gov.cn/apply/app/common/checkValidCode',  # 带验证码验证参数
    'mymanage': 'https://apply.jtw.beijing.gov.cn/apply/app/user/person/manage/',  # 个人主页面带用户唯一设备码
    'personal_info': 'https://apply.jtw.beijing.gov.cn/apply/app/user/person/choosePerson/',  # 带用户唯一设备码
    'logout': 'https://apply.jtw.beijing.gov.cn/apply/app/common/logout',
    # 带用户唯一设备码，在GET下带参数regType（PTC、XNY），在POST下带pagenum、issueNumber、applyCode、validCode
    'QuotaPool': 'https://apply.jtw.beijing.gov.cn/apply/app/pool/personQuery/',
    # 带用户唯一设备码，在GET下带参数regType（PTC、XNY），在POST下带pagenum、issueNumber、applyCode、validCode
    'QuotaPass': 'https://apply.jtw.beijing.gov.cn/apply/app/norm/personQuery/',
    # 带用户唯一设备码，指标验证（POST）：id、name、idType、idCode、validCode
    'QuotaVerify': 'https://apply.jtw.beijing.gov.cn/apply/app/norm/personquery/',
}

LOGIN_FORM = {
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

