#encoding=utf-8
import re
import getopt
import sys

'''
通过Burpsuite的BurpJSLinkFinder插件发现的链接，生成目录字典
'''

class span:
    def __init__(self,filename):
        self.filename = filename

    #获取目标文件每一行内容
    def getlines(self):
        with open(self.filename,'r') as file:
            lines = file.readlines()
            return lines

    # 筛选出url,去掉重复选项
    def offurl(self, urls):
        url = sorted(set(urls))
        return url

    #获得urls
    def findurl(self):
        lines = self.getlines()
        urls = []
        for line in lines:
            hp = re.compile('http://', re.I)
            hps = re.compile('https://', re.I)
            r = hp.search(line)
            rs = hps.search(line)
            # 过滤一些特殊字符
            line = line.replace(',', '').replace('\\n', '')
            line = self.offpicture(line)
            if line != None:
                if r != None:
                    url = re.findall('http://(.*)$', line)[0]
                    urls.append("http://" + url)

                if rs != None:
                    url = re.findall('https://(.*)$', line)[0]
                    urls.append("https://" + url)
        return urls

    #筛选出域名，去掉重复选项
    def offdomain(self,urls):
        #设置域名集合
        domains = []
        for url in urls:
            pot = []
            for i in re.finditer('/', url):
                pot.append(re.findall('\((.*),', str(i.span())))
            p = str(pot).split(",")
            wod = []
            for j in p:
                wod.append(re.findall("'(.*)'",j)[0])
            if(len(wod) <= 2 ):
                domains.append(url[int(wod[1])+1:])
            else:
                domains.append(url[int(wod[1])+1:int(wod[2])])
        #利用集合唯一性，删除列表重复项
        domain = sorted(set(domains))
        return domain



    def offpicture(self,url):
        dn = ['.png','.jpg','.eot','.svg','.woff','.ttf','.jpeg','.css']
        b = 0
        for a in dn:
            if re.search(a,url) != None:
                b += 1
        if b == 0:
            return url

    #uri
    def uri(self):
        text = []
        lines = self.getlines()
        for line in lines:
            if re.match('\\t',line) != None:
                uri = re.findall('- (.*)$',line)[0]
                if re.match('http',uri) == None:
                    uris = self.offpicture(uri)
                    if uris != None:
                        if uris[0] != '/':
                            text.append('/'+ uris)
                        else:
                            text.append(uris)
        return text

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   return inputfile,outputfile




if __name__ == "__main__":
    inputfile,outputfile = main(sys.argv[1:])
    Link = span(inputfile)
    #获取urls
    urls = Link.findurl()
    #获取domains
    domains = Link.offdomain(urls)
    #获取uri
    uris = Link.uri()
    with open(outputfile,'w') as file:
        file.write("#BurpLinkFinder tools#"+"\n"*3)
        
        #write domains
        file.write("[+] find the domains below\n")
        for domain in domains:
            file.write("\t" + domain + "\n")


        #write urls
        file.write("\n"*3 + "[+] find the urls below\n")
        for url in urls:
            file.write("\t"+url+"\n")


        #write uri
        file.write("\n"*3 + "[+] find the uri below\n")
        for uri in uris:
            file.write("\t"+uri+"\n")
        print("整理完成")





