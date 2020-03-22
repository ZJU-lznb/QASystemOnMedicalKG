# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
import xlwt
from urllib.request import quote
g_sheet = None
g_file = None
g_count = 0
name_xls  =''
class get_patent_data_as_xls:
    def __init__(self):
        global name_xls
        key = input('请输入需要查询的关键词')
        page = input('请给出需要的页数')
        name_xls = input('保存名称')
        pageint = int(page)

        a = get_patent_data_as_xls.download_pat_info(self,key,pageint)
    def set_style(self,nameAndDate, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.nameAndDate = nameAndDate
        font.bold = False
        font.color_index = 4
        font.height = height
        style.font = font
        return style


# 写Excel
    def creatExl(self,data):
        global g_sheet, g_file, g_count
        g_file = xlwt.Workbook()
        g_sheet = g_file.add_sheet('attention', cell_overwrite_ok=True)
        row0 = ["序号", "类型", "编号", "名称", "链接", "发明人", "摘要"]
        get_patent_data_as_xls.write_raw(self,row0)


    def write_raw(self,data):
        global g_sheet, g_file, g_count,name_xls
        default = xlwt.easyxf('font: name Arial;')
        for i in range(0, len(data)):
            # g_sheet.write(g_count,i,data[i],set_style('Times New Roman',220,True))
            g_sheet.write(g_count, i, data[i], default)
        g_count = g_count + 1
        g_file.save('{0}.xls'.format(name_xls))


# 下载专利信息 主函数
    def download_pat_info(self,key,pageCnt):
        global g_count
        eachPageUrls = []

        get_patent_data_as_xls.creatExl(self,key)
        keyUrl = quote(key)
        baseUrl = 'http://www2.soopat.com/Home/Result?SearchWord=' + keyUrl + '&FMZL=Y&SYXX=Y&WGZL=Y&FMSQ=Y'

        for i in range(0, pageCnt):
            if i != 0:
                # 第一页序号不一样
                url = baseUrl + '&PatentIndex=' + str(i * 10)
            else:
                url = baseUrl
            eachPageUrls.append(url)
            print(url)

        for url in eachPageUrls:
            print(g_count)
            req = requests.get(url)
            req.encoding = 'utf-8'
            html = req.text
            table_bf = BeautifulSoup(html, 'lxml')

            try:
                for each in table_bf.find_all('div', attrs={
                    "style": "min-height: 180px;max-width: 1080px;"}):  # attrs={'scope':"col"}):
                    # print(each.get_text())
                    content = []
                    # 序号
                    content.append(str(g_count))
                    typeblock = each.find('h2')
                    type = typeblock.find('font')
                    # [发明]
                    nameAndDate = typeblock.find('a')
                    date = nameAndDate.find('font', attrs={"size": "-1"})
                    list = nameAndDate.get_text().split(' - ')
                    # 201910993873.X
                    date = list[1]

                    name = list[0]
                    content.append(date)
                    # 类型
                    content.append(type.get_text()[1:])
                    # 名称
                    content.append(name)
                    # 链接
                    content.append('http://www2.soopat.com' + nameAndDate['href'])
                    # XXX有限责任公司
                    head = each.find('span', attrs={"class": "PatentAuthorBlock"})
                    company = head.find('a')
                    content.append(company.get_text())
                    # 摘要正文
                    text = each.find('span', attrs={"class": "PatentContentBlock"})
                    content.append(text.get_text())
                    get_patent_data_as_xls.write_raw(self,content)
                    # print(content)
            except Exception as aa:
                print(aa)


if __name__ == '__main__':

    hd = get_patent_data_as_xls()

    print('保存完成')