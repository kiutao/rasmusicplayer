# -*- coding: utf-8 -*-
import urllib2
import json
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

    shtml = r'http://s.music.163.com/search/get/?src=lofter&type=1&filterDj=true&s=%s'%(searchname)
    html = urllib2.urlopen(shtml)
    html = html.read()   #句柄转化成字符串处理

#counts = collections.Counter(html)
#counts = counts['=']   #此处最好用len函数判断songs底下的段落数目
#counts = counts/4

    html = json.loads(html)   #解码json格式
    counts = html['result']['songCount']
    counts = int(counts)

    if counts>0 and number>0 :
        name = html['result']['songs'][number]['name']
        singer = html['result']['songs'][number]['artists'][0]['name']
        album = html['result']['songs'][number]['album']['name']
        songid = html['result']['songs'][number]['id']
#url1 = html['result']['songs'][0]['audio']
        url = "http://music.163.com/song/media/outer/url?id=" + str(songid) + ".mp3"
        print '\n\033[1;36;40m'+str(number)+'.歌名：%s \n  歌手：%s \n  专辑：%s \033[0m'%(name,singer,album)
        a = 'mpg123 -C %s'%(url)
        print '\n\033[5;31;40m♪♪\033[0m\033[0;31;40m正在播放第'+ str(number)+'首曲目\033[0m\033[5;31;40m♪♪\033[0m'
        commands.getoutput(a)
    else:
        print "编号超出所有歌曲总数:", counts
        exit()

if __name__ == "__main__":
    main(sys.argv[1:])

