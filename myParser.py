#BODY1 DIV1 TABLE3 TBODY1 TR1 TD3 TABLE2 TBODY1 TR1 TD1 TABLE1 TBODY1 START READING /TBODY

from html.parser import HTMLParser

class myParser(HTMLParser):
    def __init__(self,convert_charrefs=True):
        HTMLParser.__init__(self,convert_charrefs=True)
        self.readHy=False
        self.readingHy=False
        self.LatestHy=""
        self.NoRe=0
        self.hyresult=[]

    def handle_starttag(self, tag, attrs):
        if tag=='td' :
            if not (len(attrs) == 3):
                pass
            else:
                for k in attrs:
                    if k not in [("height","33"),("align","left"),( "valign","top")]:
                        break
                    else:
                        self.readHy=True
        elif tag=='a':
            if (not self.readHy) or (self.NoRe >= 42):
                pass
            else:
                self.NoRe+=1
                self.readingHy=True
                for (v1,v2) in attrs:
                    if v1=="href":
                        self.LatestHy=v2
    def handle_data(self,data):
        if self.readingHy:
            self.hyresult.append((data,self.LatestHy))

    def handle_endtag(self, tag):
        if tag=='a':
            self.readingHy=False

    def getResult(self):
        return self.hyresult[2:]
















