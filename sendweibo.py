from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
browser = webdriver.Chrome(options=options)

print("尝试进入微博登录页面")
browser.get('https://weibo.com/login.php')
try:
    element = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.ID, 'loginname'))
    )
finally:
    time.sleep(2)
    print("进入微博登录页面成功")

    print('尝试定位账号输入位置')
    username = browser.find_element_by_id('loginname')
    username.click()
    username.send_keys('18684000603')
    print('输入账号')

    print('尝试定位密码输入位置')
    password = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
    password.click()
    password.send_keys('yx19921006')
    print('输入密码')
    time.sleep(3)
    loginAction = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
    print('点击登录')
    loginAction.click()

    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[2]/textarea'))
        )
    except:
        loginAction = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
        print('登录失败，第二次点击登录')
        loginAction.click()
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[2]/textarea'))
            )
        except:
            loginAction = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
            print('第二次登录失败，第三次次点击登录')
            loginAction.click()

    finally:
        print("当前时间:" + time.strftime("%Y-%m-%d", time.localtime(time.time())))
        year = time.strftime('%Y', time.localtime())
        year = int(year)
        days = time.strftime('%j', time.localtime())
        days = int(days)
        if (year % 100 != 0 and year % 4 == 0) or (year % 100 == 0):
            # 是闰年
            if days < 169:
                a = days / 28
                a = int(a)

                if a >= 1:
                    month = a

                if a < 1:
                    month = 1

                b = days - month * 28

                if b >= 0:
                    day = b

                if b < 0:
                    day = days

                month = str(month)
                year = str(year)
                day = str(day)
                text = '今天是伊士曼计划日历的' + year + '年' + month + '月' + day + "日"

            if a == 169:
                text = "今天是伊士曼计划日历的" + year + "年" + "6月29日"
            if a > 169:
                a = a - 1
                a = days / 28
                a = int(a)

                if a >= 1:
                    month = a

                if a < 1:
                    month = 1

                b = days - month * 28

                if b >= 0:
                    day = b

                if b < 0:
                    day = days

                month = str(month)
                year = str(year)
                day = str(day)
                text = '今天是伊士曼计划日历的' + year + '年' + month + '月' + day + "日"

        else:
            # 不是闰年
            a = days / 28
            a = int(a)
            if a >= 1:
                month = a

            if a < 1:
                month = 1

            b = days - month * 28

            if b >= 0:
                day = b

            if b < 0:
                day = days

            month = str(month)
            year = str(year)
            day = str(day)
            text = '今天是伊士曼计划日历的' + year + '年' + month + '月' + day + "日"

        print(text)
        time.sleep(2)
        content = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[2]/textarea')
        content.click()
        content.send_keys(text)

        publish = browser.find_element_by_xpath('//*[@id="v6_pl_content_publishertop"]/div/div[3]/div[1]/a')
        time.sleep(2)
        publish.click()
        time.sleep(10)

        browser.close()
