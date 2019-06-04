# -!- coding: utf-8 -!-

import re
import urllib.request
import urllib.parse
import time
from PIL import Image
import os

def craw(chinese):
    url='http://hanyu.baidu.com/s?wd='+urllib.parse.quote(chinese)+'&ptype=zici'
    print(chinese)
    header = {
    #Windows
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    #Android
    #'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
    }
    serverError=True
    gifnum = 0
    while serverError:
        try:
            request = urllib.request.Request(url, headers=header)
            reponse = urllib.request.urlopen(request).read()
            #html = str(reponse)
            html = reponse.decode('UTF-8')
            #print(reponse.decode('UTF-8'))

            # store html
            f = open(chinese + '.html', 'w', encoding='utf-8')
            f.write(reponse.decode('UTF-8'))
            f.close()

            # get gif
            imgs = re.compile('data-gif="(.+?\.gif)"').findall(html)
            for img in imgs:
                imagename= chinese+'.gif'
                imageurl=img
                try:
                    #下载gif
                    urllib.request.urlretrieve(imageurl,filename=imagename)
                    #分解gif
                    im = Image.open(imagename)
                    pngDir = imagename[:-4]
                    #创建存放每帧图片的文件夹
                    if not os.path.exists(pngDir):
                        os.mkdir(pngDir)
                    try:
                        while True:
                            #保存当前帧图片
                            current = im.tell()
                            im.save(pngDir+'/'+str(current)+'.png')
                            #获取下一帧图片
                            im.seek(current+1)
                            gifnum = gifnum + 1
                    except EOFError:
                        pass
                except:
                    print(chinese+' failure')
            
            print(gifnum)

            # get pinyin
            pinyin = re.compile('<div class="pronounce" id="pinyin">.+?(<b>.+?</b>)', re.DOTALL).findall(html)
            print(pinyin)

            # get radical
            radical = re.compile('<label>部 首</label>.+?(<span>.+?</span>)', re.DOTALL).findall(html)
            print(radical)

            # get stroke_count
            stroke_count = re.compile('<label>笔 画</label>.+?(<span>.+?</span>)', re.DOTALL).findall(html)
            print(stroke_count)

            return [gifnum, pinyin, radical, stroke_count]
            serverError=False
        except:
            print(chinese+'server error')
            time.sleep(40)

strs = ['一','乙','二','十','丁','厂','七','卜','人','入','八','九','几','儿','了','力','乃','刀','又','三','于','干','亏','士','工','土','才','寸','下','大','丈','与','万','上','小','口','巾','山','千','乞','川','亿','个','勺','久','凡','及','夕','丸','么','广','亡','门','义','之','尸','弓','己','已','子','卫','也','女','飞','刃','习','叉','马','乡','丰','王','井','开','夫','天','无','元','专','云','扎','艺','木','五','支','厅','不','太','犬','区','历','尤','友','匹','车','巨','牙','屯','比','互','切','瓦','止','少','日','中','冈','贝','内','水','见','午','牛','手','毛','气','升','长','仁','什','片','仆','化','仇','币','仍','仅','斤','爪','反','介','父','从','今','凶','分','乏','公','仓','月','氏','勿','欠','风','丹','匀','乌','凤','勾','文','六','方','火','为','斗','忆','订','计','户','认','心','尺','引']

head = '''
<html>
<head>
    <title>zitie</title>
</head>
<body>
    <table style="font-size:20px">
'''
body = '''
        <tr >
            <td>
                <label>拼音:</label> %s 
                <label>部首:</label> %s  
                <label>笔画:</label> %s
            </td>
        </tr>
        <tr>
            <td>
                <img src="%s.png" width="57px" height="57px">
                <img src="%s/0.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
                <img src="%s/0.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
                <img src="bg.png" width="57px" height="57px">
            </td>
        </tr>
'''
foot = '''
    </table>
</body>
</html>
'''
content = ''
for st in strs:
    data = craw(st)
    print(data)
    content += body%(data[1][0], data[2][0], data[3][0], st + '/' + str(data[0]), st, st)
    #print(content)

    time.sleep(5)

f = open('out.html', 'w', encoding='utf-8')
f.write(head + content + foot)
f.close()