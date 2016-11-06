import urlparse
import urllib
from BeautifulSoup import BeautifulSoup
#!/usr/bin/python

import sys

def main():

    urls = []
    if len(sys.argv) > 2:
        arg = 1
        while arg < len(sys.argv):
            url = "http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year="+sys.argv[arg]+"&make="+sys.argv[arg+1]+"&pageno=1&sortBy=Comb&tabView=0&rowLimit=200"
            urls.insert(arg-1, url)
            arg+=2

    tablehead = 'CarModel,EngineDisplacement,Transmission,FuelType,ImgUrl,MPG,UserEco\n'
    while len(urls) > 0:
        try:
            htmltext = ''
            htmltext = urllib.urlopen(urls[0]).read()
        except:
            print urls[0]

        soup = BeautifulSoup(htmltext)
        urls.pop(0)

        table = soup.find('table', attrs={'class': 'cars display responsive stickyHeader'})

        for table_body in table.findAll('tbody'):
            rowNum = 0
            if table_body:
                rows = table_body.findAll('tr')
                for row in rows:
                    if rowNum == 0:
                        model = row.find('td').find('a', href=True)
                        detail = row.find('span', attrs={'class': 'config'})
                        if model:
                            tablehead = tablehead + ' ' + model.text + '  ' + detail.text

                    if row.find('td', attrs={'class': 'mpg-epa'}):
                        imgurl = row.find('td', attrs={'class': 'vphoto'}).find('img', attrs={'class': 'img-thumbnail img-responsive veh-photo'})
                        fuelecoTable = row.find('td', attrs={'class': 'mpg-epa'}).find('div',attrs={'class': 'panel panel-default mpg-border'}).find('div',attrs={'class':'panel-body'}).find('table',attrs={'class':'results'}).findAll('tbody')
                        fueleco = ''
                        for fuelecorow in fuelecoTable:
                            fueleco = fuelecorow.find('td', attrs={'class': 'mpg-comb'})
                            break

                        usereco = row.find('td', attrs={'class': 'mpg-user'})
                        tablehead = tablehead + ',' + str(imgurl)
                        tablehead = tablehead + ',' + str(fueleco.text)
                        tablehead = tablehead + ',' + str(usereco.text)
                        tablehead = tablehead + '\n'
                    rowNum += 1
        #tablehead = tablehead + '\n'
    tablehead = tablehead + '\n'
    f = open('Output.csv','w')
    f.write(str(tablehead))
pass

if __name__ == '__main__':
    main()