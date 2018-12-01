# -*- coding: utf-8 -*-
import urllib2
import json
import re
import sys, getopt
import commands
import collections
reload(sys)
sys.setdefaultencoding('utf-8')

def main(argv):
    searchname = ''
    number = '0'
    try:
        opts, args = getopt.getopt(argv,'h',["name=","num="])
    except getopt.GetoptError:
        print '对不起，参数输入不完整，请重新输入'
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print '\n本项目源采用网易云音乐，播放器采用mpg123\n--name 写入歌曲名字\n--num  选择歌曲序号\n<- , -> 可快进快退\n9,0可增加减小音量'
            sys.exit()
        elif opt in ("--name"):
            searchname = arg
        elif opt in ("--num"):
            number = int(arg)

    shtml = r'http://search.kuwo.cn/r.s?all=%s&ft=music&itemset=web_2013&client=kt&pn=0&rn=5&rformat=json&encoding=utf8'%(searchname)
    html = urllib2.urlopen(shtml)
    html = html.read()   #句柄转化成字符串处理
    html = html.replace("'", '"')
#    sys.exit()

#counts = collections.Counter(html)
#counts = counts['=']   #此处最好用len函数判断songs底下的段落数目
#counts = counts/4

    html = json.loads(html)   #解码json格式
    allcnt = html['TOTAL']
    counts = html['SHOW']

    #counts = int(counts)

    if counts> 0 and number>=0 :
        name = html['abslist'][number]['SONGNAME']
        singer = html['abslist'][number]['ARTIST']
        album = html['abslist'][number]['ALBUM']
        songid = html['abslist'][number]['MUSICRID']
        shtml = r'http://antiserver.kuwo.cn/anti.s?type=convert_url&rid=%s&format=mp3&response=url'%(songid)
        html = urllib2.urlopen(shtml)
        url = html.read()
        print url
        print '\n\033[1;36;40m'+str(number)+'.歌名：%s \n  歌手：%s \n  专辑：%s \033[0m'%(name,singer,album)
        a = 'mpg123 -C %s'%(url)
        print '\n\033[5;31;40m♪♪\033[0m\033[0;31;40m正在播放第'+ str(number)+'首曲目\033[0m\033[5;31;40m♪♪\033[0m'
        commands.getoutput(a)
    else:
        print "编号超出所有歌曲总数:", counts
        exit()

if __name__ == "__main__":
    main(sys.argv[1:])

