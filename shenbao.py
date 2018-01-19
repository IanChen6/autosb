# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""

from guoshui import guoshui
import os
import calendar
import random
import re
from urllib.parse import urlencode
from selenium.webdriver import ActionChains
from selenium import webdriver
import time
import requests
import json
import base64
from lxml import etree
import pymssql
import threading
from selenium.webdriver.support import ui
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument
from suds.client import Client
import suds
from proxy_ceshi import get_all_proxie
try:
    import urlparse as parse
except:
    from urllib import parse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import hashlib
from log_ging.log_01 import *
from get_db import job_finish
from get_db import get_db
import sys

class autoSb(guoshui):
    def __init__(self,batchid,batchyear,batchmonth,companyid,customerid,user,pwd,fw1,fw2,hw1,hw2,fwms,fwyj,hwyj,hwms,djzs,dfzs,dczs,djms,dfms,dcms,logger):
        self.user = user
        self.pwd = pwd
        self.logger = logger
        self.batchid = batchid
        self.batchyear = batchyear
        if 0 < batchmonth < 10:
            self.batchmonth = "0" + str(batchmonth)
        else:
            self.batchmonth = batchmonth
        self.companyid = companyid
        self.customerid = customerid
        self.host, self.port, self.db = get_db(companyid)
        if batchmonth != 0:
            monthRange = calendar.monthrange(batchyear, batchmonth)
            self.days = monthRange[1]
        if not os.path.exists('resource/{}'.format(user)):
            os.mkdir('resource/{}'.format(user))
        self.fw1=float(fw1)
        self.fw2=float(fw2)
        self.hw1=float(hw1)
        self.hw2=float(hw2)
        self.fwms=float(fwms)
        self.fwyj=float(fwyj)
        self.hwyj=float(hwyj)
        self.hwms=float(hwms)
        self.djzs=djzs
        self.dfzs=dfzs
        self.dczs=dczs
        self.djms=djms
        self.dfms=dfms
        self.dcms=dcms
        if not os.path.exists('resource/{}'.format(user)):
            os.mkdir('resource/{}'.format(user))

    def zdsb(self,browser):
        wait = ui.WebDriverWait(browser, 10)
        try:
            browser.find_element_by_xpath('//a[@id="mini-36"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-34"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-9"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-7"]/span').click()
        except:
            print("系统正常")
        browser.find_element_by_css_selector('#mini-4 span').click()

        page1 = browser.page_source
        root = etree.HTML(page1)
        judge = root.xpath('//*[@class="J_sbxx-tbody"]/tr')
        a = 1
        for i in judge:
            xgm = i.xpath('.//text()')
            if ' 小规模增值税季报 ' in xgm and '申报' in xgm:
                try:
                    gsrq = xgm[5]
                    gsrq = re.search(r'(.*?)~(.*)', gsrq)
                    gsks = gsrq.group(1)
                    gsjs = gsrq.group(2)
                    browser.find_element_by_xpath(
                        '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                    hds = browser.window_handles
                    cr = browser.current_window_handle
                    for c_window in hds:
                        if c_window != cr:
                            browser.switch_to_window(c_window)
                            brct = browser.page_source
                            wait.until(lambda browser: browser.find_element_by_css_selector('#cekcWindow iframe'))
                            msg = browser.find_element_by_class_name("mini-panel-toolbar")
                            while msg.is_displayed():
                                time.sleep(3)
                            frame_element = browser.find_element_by_css_selector('#cekcWindow iframe')
                            browser.switch_to_frame(frame_element)
                            ctp = browser.page_source
                            browser.find_element_by_css_selector("#unexist span").click()
                            browser.switch_to.default_content()
                            if self.fw1 > 0:
                                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="B2$text"]'))
                                browser.find_element_by_xpath('//*[@id="B2$text"]').clear()
                                fw1 = str(self.fw1)
                                browser.find_element_by_xpath('//*[@id="B2$text"]').send_keys(fw1)

                            if self.fw2 > 0:
                                browser.find_element_by_xpath('//*[@id="B3$text"]').clear()
                                fw2 = str(self.fw2)
                                browser.find_element_by_xpath('//*[@id="B3$text"]').send_keys(fw2)
                            if self.hw1 > 0:
                                browser.find_element_by_xpath('//*[@id="A2$text"]').clear()
                                hw1 = str(self.hw1)
                                browser.find_element_by_xpath('//*[@id="A2$text"]').send_keys(hw1)
                            if self.hw2 > 0:
                                browser.find_element_by_xpath('//*[@id="A3$text"]').clear()
                                hw2 = str(self.hw2)
                                browser.find_element_by_xpath('//*[@id="A3$text"]').send_keys(hw2)

                            browser.find_element_by_css_selector('#nextStep').click()
                            try:
                                wait.until(
                                    lambda browser: browser.find_element_by_css_selector('.mini-tools-close'))
                                browser.find_element_by_css_selector('.mini-tools-close').click()
                            except Exception as e:
                                print(e)
                                print("无小弹窗")
                            if self.fwms > 0:
                                try:
                                    browser.find_element_by_xpath('//*[@id="B18$text"]').clear()
                                    try:
                                        browser.find_element_by_xpath('//span[@id="0"]').click()
                                    except:
                                        print("无弹出框")
                                    fwms = str(self.fwms)
                                    browser.find_element_by_xpath('//*[@id="B18$text"]').send_keys(fwms)
                                except:
                                    print("无法输入")
                            if self.fwyj > 0:
                                try:
                                    browser.find_element_by_xpath('//*[@id="B21$text"]').clear()
                                    try:
                                        browser.find_element_by_xpath('//span[@id="0"]').click()
                                    except:
                                        print("无弹出框")
                                    fwyj = str(self.fwyj)
                                    browser.find_element_by_xpath('//*[@id="B21$text"]').send_keys(fwyj)
                                except:
                                    print("无法输入")
                            if self.hwms > 0:
                                try:
                                    browser.find_element_by_xpath('//*[@id="A18$text"]').clear()
                                    try:
                                        browser.find_element_by_xpath('//span[@id="0"]').click()
                                    except:
                                        print("无弹出框")
                                    hwms = str(self.hwms)
                                    browser.find_element_by_xpath('//*[@id="A18$text"]').send_keys(hwms)
                                except:
                                    print("无法输入")
                            if self.hwyj > 0:
                                try:
                                    browser.find_element_by_xpath('//*[@id="A21$text"]').clear()
                                    try:
                                        browser.find_element_by_xpath('//span[@id="0"]').click()
                                    except:
                                        print("无弹出框")
                                    hwyj = str(self.hwyj)
                                    browser.find_element_by_xpath('//*[@id="A21$text"]').send_keys(hwyj)
                                except:
                                    print("无法输入")
                            fwsb = browser.find_element_by_xpath('//*[@id="B22"]/input').get_attribute("value")
                            hwsb = browser.find_element_by_xpath('//*[@id="A22"]/input').get_attribute("value")
                            sbje = float(fwsb) + float(hwsb)
                            browser.find_element_by_css_selector('#nextStep').click()
                            time.sleep(0.2)
                            browser.find_element_by_css_selector('#nextStep').click()
                            wait.until(lambda browser: browser.find_element_by_css_selector('#pbbd'))
                            browser.find_element_by_css_selector('#pbbd').click()
                            time.sleep(10)
                            ycdb = browser.page_source
                            if "不通过" not in ycdb:
                                print('比对通过')
                                wait.until(lambda browser: browser.find_element_by_css_selector("#mini-213"))
                                time.sleep(3)
                                cl = browser.page_source
                                browser.find_element_by_css_selector("#mini-213").click()
                                browser.find_element_by_css_selector('#nextStep').click()
                                frame_element = browser.find_element_by_css_selector('#sjyzmWindow iframe')
                                browser.switch_to_frame(frame_element)
                                # browser.find_element_by_xpath('//*[@onclick="normalSubmit()"]').click()#不申报
                                # time.sleep(10)
                            elif "不通过" in ycdb:
                                dbbtg = etree.HTML(ycdb)
                                dbbtg1 = dbbtg.xpath('//*[@id="mini-212"]//table/tbody/tr')
                                fail_dict = {}
                                for r in dbbtg1:
                                    t = r.xpath('.//text()')
                                    fail_dict[t[0]] = t[1]
                                fail_json = json.dumps(fail_dict, ensure_ascii=False)
                                gsparams = (self.customerid, "GS", "小规模增值税", fail_json)
                                self.insert_db("[dbo].[Python_Serivce_ShenZhen_TaxApplyCheckError]",
                                          gsparams)
                                browser.quit()
                                sys.exit()

                            browser.close()
                            browser.switch_to_window(cr)
                    gsdict = {}
                    gsdict["开始期间"] = gsks
                    gsdict["结束期间"] = gsjs
                    gsdict["申报金额"] = str(sbje)
                    gsdict["申报状态"] = "已申报"
                    gsjson = json.dumps(gsdict, ensure_ascii=False)
                    gsparams = (self.customerid, "GS", "小规模增值税", gsjson)
                    self.insert_db("[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", gsparams)
                    print('国税申报成功')
                except Exception as e:
                    print(e)
                    gsdict = {}
                    gsdict["开始期间"] = gsks
                    gsdict["结束期间"] = gsjs
                    try:
                        gsdict["申报金额"] = str(sbje)
                    except:
                        gsdict["申报金额"] = ""
                    gsdict["异常信息"] = e
                    gsdict["申报状态"] = "申报失败"
                    gsjson = json.dumps(gsdict, ensure_ascii=False)
                    gsparams = (self.customerid, "GS", "小规模增值税", gsjson)
                    self.insert_db("[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", gsparams)
                    browser.quit()
                    sys.exit()
            a += 1
        try:
            ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
            browser.get(url=ds_url)
            try:
                wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
                browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
            except Exception as e:
                print(e)
                print("弹出框与预设不一致")
            try:
                browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
            except Exception as e:
                print(e)
                print("弹出框与预设不一致")
            browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
            time.sleep(3)
            windows = browser.window_handles
            window1 = browser.current_window_handle
            for c_window in windows:
                if c_window != window1:
                    browser.close()
                    browser.switch_to_window(c_window)
            time.sleep(1)
            browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
            browser.switch_to_frame('qyIndex')
            wait.until(lambda browser: browser.find_element_by_css_selector("#menu3_3_102001"))
            browser.find_element_by_css_selector('#menu3_3_102001').click()
            browser.switch_to_frame('qymain')
            time.sleep(2)
            dspage = browser.page_source
            dsroot = etree.HTML(dspage)
            dsjudge = dsroot.xpath('//*[@id="tbody"]/tr')
            b = 1
            for i in dsjudge:
                xgm = i.xpath('.//text()')
                if '自行申报' in xgm and '我要申报' in xgm:
                    ssrq = browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[3]'.format(b)).text
                    rq = re.search(r'(.*?)至(.*)', ssrq)
                    ks = rq.group(1)
                    js = rq.group(2)
                    browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[7]/a'.format(b)).click()
                    browser.find_element_by_css_selector("#confirmSbBtn").click()
                    # browser.switch_to_frame
                    browser.switch_to.default_content()
                    time.sleep(3)
                    cont = browser.page_source
                    browser.switch_to_frame('layui-layer-iframe3')
                    cont = browser.page_source
                    browser.find_element_by_css_selector("#sbxx0_2").clear()
                    browser.find_element_by_css_selector("#sbxx0_2").send_keys(self.djzs)
                    browser.find_element_by_css_selector("#sbxx0_3").clear()
                    browser.find_element_by_css_selector("#sbxx0_3").send_keys(self.djms)
                    browser.find_element_by_css_selector("#sbxx1_2").clear()
                    browser.find_element_by_css_selector("#sbxx1_2").send_keys(self.dfzs)
                    browser.find_element_by_css_selector("#sbxx1_3").clear()
                    browser.find_element_by_css_selector("#sbxx1_3").send_keys(self.dfms)
                    browser.find_element_by_css_selector("#sbxx2_2").clear()
                    browser.find_element_by_css_selector("#sbxx2_2").send_keys(self.dczs)
                    browser.find_element_by_css_selector("#sbxx2_3").clear()
                    browser.find_element_by_css_selector("#sbxx2_3").send_keys(self.dcms)
                    per1 = browser.find_element_by_css_selector("#sbxx0_7").get_attribute("value")
                    per2 = browser.find_element_by_css_selector("#sbxx1_7").get_attribute("value")
                    per3 = browser.find_element_by_css_selector("#sbxx2_7").get_attribute("value")
                    djzs = float(self.djzs)
                    djms = float(self.djms)
                    djprice = (djzs + djms) * float(per1)
                    dfzs = float(self.dfzs)
                    dfms = float(self.dfms)
                    dfprice = (dfzs + dfms) * float(per2)
                    dczs = float(self.dczs)
                    dcms = float(self.dcms)
                    dcprice = (dczs + dcms) * float(per3)
                    sbprice = djprice + dfprice + dcprice
                    browser.switch_to.default_content()
                    cc = browser.page_source
                    # browser.find_element_by_link_text("正式申报").click() #不申报
                    browser.switch_to_frame('layui-layer-iframe3')
                    pdsb = browser.page_source
                    if "正式申报成功" in pdsb:
                        print('地税申报成功')
                        sb_status = "成功"
                        dsdict = {}
                        dsdict["开始期间"] = ks
                        dsdict["结束期间"] = js
                        dsdict["申报金额"] = str(sbprice)
                        dsdict["申报状态"] = sb_status
                        dsjson = json.dumps(dsdict, ensure_ascii=False)
                        dsparams = (self.customerid, "DS", "教育费附加、地方教育附加、城市维护建设税", dsjson)
                        self.insert_db("[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", dsparams)
                    else:
                        print('地税申报失败')
                        sb_status = "失败"
                        dsdict = {}
                        dsdict["开始期间"] = ks
                        dsdict["结束期间"] = js
                        dsdict["申报金额"] = str(sbprice)
                        dsdict["申报状态"] = sb_status
                        dsjson = json.dumps(dsdict, ensure_ascii=False)
                        dsparams = (self.customerid, "DS", "教育费附加、地方教育附加、城市维护建设税", dsjson)
                        self.insert_db("[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", dsparams)

                    break
                b += 1
            # browser.quit()
        except Exception as e:
            print("地税申报失败")
            print(e)

    def dishui(self, browser):
        print("截取地税申报信息")
        time.sleep(2)
        windows = browser.window_handles
        window1 = browser.current_window_handle
        for c_window in windows:
            if c_window != window1:
                browser.close()
                browser.switch_to_window(c_window)
        # 查询个人所得税
        wait = ui.WebDriverWait(browser, 10)
        # wait.until(
        #     lambda browser: browser.find_element_by_css_selector(
        #         "#layui-layer1 div.layui-layer-btn a"))  # timeout
        # browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
        browser.switch_to.default_content()
        browser.find_element_by_css_selector('#menu_110000_110109').click()
        time.sleep(2)
        browser.switch_to_frame('qyIndex')
        sbjkcx = browser.page_source
        wait.until(
            lambda browser: browser.find_element_by_css_selector("#menu2_13_110200"))  # 容易timeout
        browser.find_element_by_css_selector('#menu2_13_110200').click()
        time.sleep(2)
        browser.find_element_by_css_selector('#menu3_15_110202').click()
        browser.switch_to_frame('qymain')
        wait.until(lambda browser: browser.find_element_by_css_selector('#sbqq'))
        time.sleep(0.5)
        browser.find_element_by_css_selector('#zsxmDm').find_element_by_xpath(
            '//option[@value="10106"]').click()  # 选择个人所得税
        sb_startd = browser.find_element_by_css_selector('#sbqq')
        sb_startd.clear()
        sb_startd.send_keys('{}-{}-01'.format(self.batchyear, self.batchmonth))
        sb_endd = browser.find_element_by_css_selector('#sbqz')
        sb_endd.clear()
        sb_endd.send_keys('{}-{}-{}'.format(self.batchyear, self.batchmonth, self.days))
        # time.sleep(1)
        browser.find_element_by_css_selector('#query').click()
        time.sleep(2)
        grsd = self.save_png(browser, 'resource/{}/地税个人所得税已申报查询.png'.format(self.user))
        # 表格信息爬取
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="ysbjl_table"]/tbody/tr')
        index = 0
        pg = browser.page_source
        if "没有" not in pg:
            for i in select:
                pdf_list = []
                pdf_list.append(grsd)
                browser.find_element_by_xpath(
                    '//table[@id="ysbjl_table"]/tbody/tr[@data-index="{}"]//input[@name="btSelectItem"]'.format(
                        index)).click()
                time.sleep(2)
                browser.find_element_by_css_selector('#print').click()
                # url=browser.find_element_by_name('sbbFormCj').get_attribute('action')
                jsxx = i.xpath('.//text()')
                pzxh = jsxx[0]
                print(jsxx)
                b_ck = browser.get_cookies()
                ck = {}
                for x in b_ck:
                    ck[x['name']] = x['value']
                post_url = parse.urljoin("https://dzswj.szds.gov.cn",
                                         browser.find_element_by_name('sbbFormCj').get_attribute(
                                             'action'))
                post_data = {'SubmitTokenTokenId': '', 'yzpzxhArray': pzxh, 'btSelectItem': 'on'}
                headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                           'Accept-Language': 'zh-CN,zh;q=0.8',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                           'X-Requested-With': 'XMLHttpRequest'}
                resp = requests.post(url=post_url, headers=headers, data=post_data, timeout=10,
                                     cookies=ck).text
                pdf_content = requests.post(url=post_url, headers=headers, data=post_data,
                                            timeout=10,
                                            cookies=ck).content
                if "错误" not in resp:
                    with open("resource/{}/申报表详情{}.pdf".format(self.user, pzxh), 'wb') as w:
                        w.write(pdf_content)
                    pdf = self.upload_img("resource/{}/申报表详情{}.pdf".format(self.user, pzxh))
                    pdf_list.append(pdf)
                params = (
                    self.batchid, self.batchyear, self.batchmonth, self.companyid, self.customerid,
                    str(pzxh),
                    str(jsxx[1]),
                    None,
                    str(jsxx[2]), "",
                    str(jsxx[3]), "", "",
                    self.img2json(pdf_list))  # self.img2json("申报表详情{}.pdf".format(pzxh))
                print(params)
                self.insert_db("[dbo].[Python_Serivce_DSTaxApplyShenZhen_Add]", params)
                index += 1
        # 城市建设税
        browser.switch_to_default_content()
        browser.switch_to_frame('qyIndex')
        browser.switch_to_frame('qymain')
        wait.until(lambda browser: browser.find_element_by_css_selector('#sbqq'))
        browser.find_element_by_css_selector('#zsxmDm').find_element_by_xpath(
            '//option[@value="10109"]').click()  # 选择城市建设税
        sb_startd = browser.find_element_by_css_selector('#sbqq')
        sb_startd.clear()
        sb_startd.send_keys('{}-{}-01'.format(self.batchyear, self.batchmonth))
        sb_endd = browser.find_element_by_css_selector('#sbqz')
        sb_endd.clear()
        sb_endd.send_keys('{}-{}-{}'.format(self.batchyear, self.batchmonth, self.days))
        # time.sleep(1)
        browser.find_element_by_css_selector('#query').click()
        time.sleep(2)
        csjs = self.save_png(browser, 'resource/{}/地税城市建设税已申报查询.png'.format(self.user))
        # 表格信息爬取
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="ysbjl_table"]/tbody/tr')
        index = 0
        pg = browser.page_source
        if "没有" not in pg:
            for i in select:
                pdf_list = []
                pdf_list.append(csjs)
                browser.find_element_by_xpath(
                    '//table[@id="ysbjl_table"]/tbody/tr[@data-index="{}"]//input[@name="btSelectItem"]'.format(
                        index)).click()
                time.sleep(2)
                browser.find_element_by_css_selector('#print').click()
                # url=browser.find_element_by_name('sbbFormCj').get_attribute('action')
                jsxx = i.xpath('.//text()')
                pzxh = jsxx[0]
                print(jsxx)
                b_ck = browser.get_cookies()
                ck = {}
                for x in b_ck:
                    ck[x['name']] = x['value']
                post_url = parse.urljoin("https://dzswj.szds.gov.cn",
                                         browser.find_element_by_name('sbbFormCj').get_attribute(
                                             'action'))
                post_data = {'SubmitTokenTokenId': '', 'yzpzxhArray': pzxh, 'btSelectItem': 'on'}
                headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                           'Accept-Language': 'zh-CN,zh;q=0.8',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                           'X-Requested-With': 'XMLHttpRequest'}
                resp1 = requests.post(url=post_url, headers=headers, data=post_data, timeout=10,
                                      cookies=ck).text
                pdf_content = requests.post(url=post_url, headers=headers, data=post_data,
                                            timeout=10,
                                            cookies=ck).content
                if "错误" not in resp1:
                    with open("resource/{}/申报表详情{}.pdf".format(self.user, pzxh), 'wb') as w:
                        w.write(pdf_content)
                    time.sleep(0.5)
                    pdf1 = self.upload_img("resource/{}/申报表详情{}.pdf".format(self.user, pzxh))
                    pdf_list.append(pdf1)
                    pdf_dict = self.parse_pdf("resource/{}/申报表详情{}.pdf".format(self.user, pzxh))
                    js = self.img2json(pdf_list)
                    js = json.loads(js)
                    js["pdf数据"] = pdf_dict
                    pdf_json = json.dumps(js, ensure_ascii=False)
                    print(pdf_json)
                else:
                    pdf_json = self.img2json(pdf_list)

                params = (
                    self.batchid, self.batchyear, self.batchmonth, self.companyid, self.customerid,
                    str(pzxh),
                    str(jsxx[1]),
                    str(jsxx[2]),
                    str(jsxx[3]), str(jsxx[4]), str(jsxx[5]), str(jsxx[6]), str(jsxx[7]),
                    pdf_json)  # self.img2json("申报表详情{}.pdf".format(pzxh))
                print(params)
                self.insert_db("[dbo].[Python_Serivce_DSTaxApplyShenZhen_Add]", params)
                index += 1
        # 企业所得税
        browser.switch_to_default_content()
        browser.switch_to_frame('qyIndex')
        browser.switch_to_frame('qymain')
        wait.until(lambda browser: browser.find_element_by_css_selector('#sbqq'))
        browser.find_element_by_css_selector('#zsxmDm').find_element_by_xpath(
            '//option[@value="10104"]').click()  # 选择企业所得税
        sb_startd = browser.find_element_by_css_selector('#sbqq')
        sb_startd.clear()
        sb_startd.send_keys('{}-{}-01'.format(self.batchyear, self.batchmonth))
        sb_endd = browser.find_element_by_css_selector('#sbqz')
        sb_endd.clear()
        sb_endd.send_keys('{}-{}-{}'.format(self.batchyear, self.batchmonth, self.days))
        # time.sleep(1)
        browser.find_element_by_css_selector('#query').click()
        time.sleep(2)
        qysd = self.save_png(browser, 'resource/{}/地税企业所得税已申报查询.png'.format(self.user))
        # 表格信息爬取
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="ysbjl_table"]/tbody/tr')
        index = 0
        pg = browser.page_source
        if "没有" not in pg:
            for i in select:
                pdf_list = []
                pdf_list.append(qysd)
                browser.find_element_by_xpath(
                    '//table[@id="ysbjl_table"]/tbody/tr[@data-index="{}"]//input[@name="btSelectItem"]'.format(
                        index)).click()
                time.sleep(2)
                browser.find_element_by_css_selector('#print').click()
                # url=browser.find_element_by_name('sbbFormCj').get_attribute('action')
                jsxx = i.xpath('.//text()')
                pzxh = jsxx[0]
                print(jsxx)
                b_ck = browser.get_cookies()
                ck = {}
                for x in b_ck:
                    ck[x['name']] = x['value']
                post_url = parse.urljoin("https://dzswj.szds.gov.cn",
                                         browser.find_element_by_name('sbbFormCj').get_attribute(
                                             'action'))
                post_data = {'SubmitTokenTokenId': '', 'yzpzxhArray': pzxh, 'btSelectItem': 'on'}
                headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                           'Accept-Language': 'zh-CN,zh;q=0.8',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                           'X-Requested-With': 'XMLHttpRequest'}
                resp2 = requests.post(url=post_url, headers=headers, data=post_data, timeout=10,
                                      cookies=ck).text
                pdf_content = requests.post(url=post_url, headers=headers, data=post_data,
                                            timeout=10,
                                            cookies=ck).content
                if "错误" not in resp2:
                    with open("resource/{}/申报表详情{}.pdf".format(self.user, pzxh), 'wb') as w:
                        w.write(pdf_content)
                    pdf2 = self.upload_img("resource/{}/申报表详情{}.pdf".format(self.user, pzxh))
                    pdf_list.append(pdf2)
                params = (
                    self.batchid, self.batchyear, self.batchmonth, self.companyid, self.customerid,
                    str(pzxh),
                    str(jsxx[1]),
                    str(jsxx[2]),
                    str(jsxx[3]), str(jsxx[4]), str(jsxx[5]), str(jsxx[6]), str(jsxx[7]),
                    self.img2json(pdf_list))  # self.img2json("申报表详情{}.pdf".format(pzxh))
                print(params)
                self.insert_db("[dbo].[Python_Serivce_DSTaxApplyShenZhen_Add]", params)
                index += 1
        print("截取地税申报信息已完成")
        # 未申报查询
        gbds = browser.window_handles
        dq = browser.current_window_handle
        for s in gbds:
            if s != dq:
                browser.switch_to_window(s)
                browser.close()
                browser.switch_to_window(dq)
        browser.switch_to_default_content()
        browser.switch_to_frame('qyIndex')
        browser.find_element_by_css_selector('#menu3_14_110201').click()
        browser.switch_to_frame('qymain')
        page = browser.page_source
        # browser.switch_to_window(window1)
        wait = ui.WebDriverWait(browser, 10)
        wait.until(lambda browser: browser.find_element_by_css_selector('#txtStart'))
        ds_start_date = browser.find_element_by_xpath('//*[@id="txtStart"]')
        ds_start_date.clear()
        ds_start_date.send_keys('2015-01-01')
        ds_end_date = browser.find_element_by_xpath("//*[@id='txtEnd']")
        ds_end_date.clear()
        ds_end_date.send_keys('{}-{}-{}'.format(self.batchyear, self.batchmonth, self.days))
        # time.sleep(1)
        browser.find_element_by_css_selector('#query').click()
        time.sleep(2)
        jietu = self.save_png(browser, 'resource/{}/地税未申报查询.png'.format(self.user))
        # 缴款表格信息爬取
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="dataTab"]/tbody/tr')

        for i in select:
            jkxx = i.xpath('.//text()')
            if "没有符合条件的数据" in jkxx:
                break
            taxjson = {}
            taxjson["结果截图"] = jietu
            taxjson["征收项目"] = jkxx[0]
            taxjson["开始日期"] = jkxx[1]
            taxjson["结束日期"] = jkxx[2]
            taxjson["申报期限"] = jkxx[3]
            taxjson["征收代理方式"] = jkxx[4]
            taxjson["是否逾期"] = jkxx[5]
            taxjson["操作"] = jkxx[6]
            taxjson = json.dumps(taxjson, ensure_ascii=False)
            params = (
                self.batchid, self.batchyear, self.batchmonth, self.companyid, self.customerid,
                taxjson)
            print(params)
            self.insert_db("[dbo].[Python_Service_DSTaxExpireShenZhen_Add] ", params)

        # 已缴款查询
        gbds = browser.window_handles
        dq = browser.current_window_handle
        for s in gbds:
            if s != dq:
                browser.switch_to_window(s)
                browser.close()
                browser.switch_to_window(dq)
        browser.switch_to_default_content()
        browser.switch_to_frame('qyIndex')
        browser.find_element_by_css_selector('#menu3_17_110204').click()
        browser.switch_to_frame('qymain')
        page = browser.page_source
        # browser.switch_to_window(window1)
        wait = ui.WebDriverWait(browser, 10)
        wait.until(lambda browser: browser.find_element_by_css_selector('#jkqq'))
        ds_start_date = browser.find_element_by_xpath('//*[@id="jkqq"]')
        ds_start_date.clear()
        ds_start_date.send_keys('{}-{}-01'.format(self.batchyear, self.batchmonth))
        ds_end_date = browser.find_element_by_xpath("//*[@id='jkqz']")
        ds_end_date.clear()
        ds_end_date.send_keys('{}-{}-{}'.format(self.batchyear, self.batchmonth, self.days))
        # time.sleep(1)
        browser.find_element_by_css_selector('#query').click()
        time.sleep(2)
        jietu = self.save_png(browser, 'resource/{}/地税已缴款查询.png'.format(self.user))
        # 缴款表格信息爬取
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="yjkxx_table"]/tbody/tr')
        index2 = 0
        pz_l = []
        pz_t = 0
        jietulist = []
        jietulist.append(jietu)
        # if len
        for i in select:
            jkxx = i.xpath('.//text()')
            if "没有符合条件的数据" in jkxx:
                break
            pz = jkxx[0]
            print(jkxx)
            pz_l.append(pz)
            if pz != pz_t:
                browser.find_element_by_xpath(
                    '//table[@id="yjkxx_table"]/tbody/tr[@data-index="{}"]//input[@name="btSelectItem"]'.format(
                        index2)).click()
                time.sleep(2)
                wait.until(lambda browser: browser.find_element_by_css_selector('#cxjkmx'))
                browser.find_element_by_css_selector('#cxjkmx').click()
                time.sleep(2)
                windows = browser.window_handles
                window2 = browser.current_window_handle
                for c_window in windows:
                    if c_window != window2:
                        browser.switch_to_window(c_window)
                        cc = browser.page_source
                        time.sleep(0.5)
                        print(c_window)
                        print(pz)
                        png_name = "resource/{}/缴款凭证号{}.png".format(self.user, pz)
                        j = self.save_png(browser, png_name)
                        jietulist.append(j)
                        sbsj = {}
                        bb = browser.page_source
                        root = etree.HTML(bb)
                        zgsb = root.xpath('//table[@id="lineTable"]/tbody/tr')
                        for i in zgsb[1:-1]:
                            cjb = i.xpath('./td/text()')
                            zt = cjb[2]
                            out = "".join(cjb[6].strip())
                            sbsj[zt] = out
                        cb = self.img2json(jietulist)
                        cb = json.loads(cb)
                        cb["缴款数据"] = sbsj
                        jkjs = json.dumps(cb, ensure_ascii=False)
                        print(jkjs)
                        browser.close()
                        browser.switch_to_window(window2)
                        time.sleep(1)
                        browser.switch_to_frame('qyIndex')
                        browser.switch_to_frame('qymain')
            else:
                jkjs = self.img2json(jietulist)
            pz_t = pz
            index2 += 1
            params = (
                self.batchid, self.batchyear, self.batchmonth, self.companyid, self.customerid,
                str(jkxx[0]),
                str(jkxx[1]),
                str(jkxx[2]),
                str(jkxx[3]), str(jkxx[4]), str(jkxx[5]), str(jkxx[6]), str(jkxx[7]),
                jkjs)
            print(params)
            self.insert_db("[dbo].[Python_Serivce_DSTaxChargeShenZhen_Add]", params)
        print("截取地税缴款信息已完成")

    def parse_biaoge(self, browser, shuiming):
        self.logger.info("customerid:{}截取国税{}申报信息".format(self.customerid,shuiming))
        wait = ui.WebDriverWait(browser, 10)
        wait.until(lambda browser: browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input"))
        year = self.batchyear
        month = self.batchmonth
        days = self.days
        qsrq = '{}{}01'.format(year, month)
        zzrq = '{}{}{}'.format(year, month, days)
        browser.get(url='http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html')
        browser.find_element_by_css_selector("#sz .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sz .mini-buttonedit-input").send_keys("{}".format(shuiming))
        browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input").send_keys(qsrq)
        browser.find_element_by_css_selector("#sbrqz .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sbrqz .mini-buttonedit-input").send_keys(zzrq)
        browser.find_element_by_css_selector("#stepnext .mini-button-text").click()
        time.sleep(2)
        imgname = self.save_png(browser, 'resource/{}/国税{}{}申报结果截图.png'.format(self.user, shuiming, month))
        # 表格信息爬取
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="mini-grid-table-bodysbqkGrid"]/tbody/tr')
        a = 1
        for i in select[1:]:
            shuizhong = i.xpath('.//text()')
            a += 1
            img_list = []
            img_list.append(imgname)
            img_list3 = []
            if "查询申报表" in shuizhong:
                self.logger.info("customerid:{}有申报表需要查询".format(self.customerid))
                img_list3 = self.parse_shenbaobiao(browser, a, month)
                self.logger.info("customerid:{}获取申报表完成".format(self.customerid))

            img_list = img_list + img_list3
            # logger.info("打印信息")
            print(shuizhong)
            self.logger.info(shuizhong)
            self.logger.info("customerid:{}开始插入数据库".format(self.customerid))
            params = (
                self.batchid, self.batchyear, self.batchmonth, self.companyid, self.customerid,
                str(shuizhong[1]),
                str(shuizhong[2]),
                str(shuizhong[3]), str(shuizhong[4]), str(shuizhong[5]), str(shuizhong[6]),
                self.img2json(img_list))
            self.logger.info(params)
            self.insert_db("[dbo].[Python_Serivce_GSTaxApplyShenZhen_Add]", params)
            self.logger.info("customerid:{}数据库插入完成".format(self.customerid))
        self.logger.info("customerid:{}截取国税申报信息已完成".format(self.customerid))


    def excute_spider(self):
        try:
            cookies = self.login()
            self.logger.info("customerid:{}获取cookies".format(self.customerid))
            jsoncookies = json.dumps(cookies,ensure_ascii=False)
            if "账号和密码不匹配" in jsoncookies:
                self.logger.warn("customerid:{}账号和密码不匹配".format(self.customerid))
                job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-2', "账号和密码不匹配")
                return
            with open('cookies/{}cookies.json'.format(self.customerid), 'w') as f:  # 将login后的cookies提取出来
                f.write(jsoncookies)
                f.close()
        except Exception as e:
            self.logger.warn(e)
            self.logger.warn("customerid:{}登陆失败".format(self.customerid))
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "登录失败")
            return False
        try:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
            dcap["phantomjs.page.settings.loadImages"] = True
            # browser = webdriver.PhantomJS(
            #     executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe',
            #     desired_capabilities=dcap)
            browser = webdriver.PhantomJS(
            executable_path='/home/tool/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
            desired_capabilities=dcap)
            browser.implicitly_wait(10)
            browser.viewportSize = {'width': 2200, 'height': 2200}
            browser.set_window_size(1400, 1600)  # Chrome无法使用这功能
            # browser = webdriver.Chrome(executable_path='D:/BaiduNetdiskDownload/chromedriver.exe')  # 添加driver的路径
        except Exception as e:
            self.logger.warn(e)
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "浏览器启动失败")
            return False
        try:
            index_url = "http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html"
            browser.get(url=index_url)
            browser.delete_all_cookies()
            with open('cookies/{}cookies.json'.format(self.customerid), 'r', encoding='utf8') as f:
                cookielist = json.loads(f.read())
            for (k, v) in cookielist.items():
                browser.add_cookie({
                    'domain': '.szgs.gov.cn',  # 此处xxx.com前，需要带点
                    'name': k,
                    'value': v,
                    'path': '/',
                    'expires': None})
            shenbao_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html'
            browser.get(url="http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")
            browser.get(url=shenbao_url)
            time.sleep(3)
            self.zdsb(browser)
        except Exception as e:
            self.logger.info("customerid:{}XGMSB出错".format(self.customerid))
            self.logger.warn(e)
            self.logger.info("小规模申报失败")
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "自动申报失败")
            browser.quit()
            return False
        try:
            # 地税查询
            self.dishui(browser)

        except Exception as e:
            self.logger.warn(e)
            params = (
                self.batchid, self.customerid, "python_job", "地税查询异常")
            self.insert_db("[dbo].[Python_Serivce_Job_Exception]", params)
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "地税查询失败")
            browser.quit()
        try:
            shenbao_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html'
            browser.get(url="http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")
            browser.get(url=shenbao_url)
            time.sleep(3)
            self.shuizhongchaxun(browser)
        except Exception as e:
            self.logger.info("customerid:{}GSYCX出错".format(self.customerid))
            self.logger.warn(e)
            self.logger.info("国税已申报查询失败")
            params = (
                self.batchid, self.customerid, "python_job", "国税申报查询异常")
            self.insert_db("[dbo].[Python_Serivce_Job_Exception]", params)
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "国税已申报查询失败")
            browser.quit()
            return False
        try:
            # 国税缴款查询
            jk_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/jk_jsxxcx.html'
            browser.get(url=jk_url)
            self.parse_jiaokuan(browser)
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '1', '成功爬取')
            print("爬取完成")
            self.logger.info("customerid:{}全部爬取完成".format(self.customerid))
        except Exception as e:
            self.logger.warn(e)
            params = (
                self.batchid, self.customerid, "python_job", "国税缴款查询异常")
            self.insert_db("[dbo].[Python_Serivce_Job_Exception]", params)
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "国税已缴款查询失败")
            browser.quit()
            return False






