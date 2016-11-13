import urlparse
import urllib
from BeautifulSoup import BeautifulSoup
#!/usr/bin/python

import sys

def main():

    urls = []

    urls.insert(1,"http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year=2005&make=Toyota&pageno=1&sortBy=Comb&tabView=0&rowLimit=200");
    urls.insert(2,"http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year=2005&make=Suzuki&pageno=1&sortBy=Comb&tabView=0&rowLimit=200");
    urls.insert(3,
                "http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year=2010&make=Toyota&pageno=1&sortBy=Comb&tabView=0&rowLimit=200");
    urls.insert(4,
                "http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year=2010&make=Suzuki&pageno=1&sortBy=Comb&tabView=0&rowLimit=200");

    urls.insert(5,"http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year=2015&make=Toyota&pageno=1&sortBy=Comb&tabView=0&rowLimit=200");
    urls.insert(6,
                "http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year=2015&make=Suzuki&pageno=1&sortBy=Comb&tabView=0&rowLimit=200");
    urls.insert(7,"http://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year=2005&make=Honda&pageno=1&sortBy=Comb&tabView=0&rowLimit=200");

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
                        fuelecoTable = ''
                        try:
                            fuelecoTable = row.find('td', attrs={'class': 'mpg-epa'}).find('div',attrs={'class': 'panel panel-default mpg-border'}).find('div',attrs={'class':'panel-body'}).find('table',attrs={'class':'results'}).findAll('tbody')
                            fueleco = ''
                            for fuelecorow in fuelecoTable:
                                fueleco = fuelecorow.find('td', attrs={'class': 'mpg-comb'})
                                break
                        except:
                            pass
                        finally:
                            if fuelecoTable is not '':
                                usereco = row.find('td', attrs={'class': 'mpg-user'})
                                tablehead = tablehead + ',' + str(imgurl['src'])
                                tablehead = tablehead + ',' + str(fueleco.text)
                                tablehead = tablehead + ',' + str(usereco.text)
                                tablehead = tablehead + '\n'
                    rowNum += 1
        #tablehead = tablehead + '\n'
    tablehead = tablehead + '\n'
    f = open('Output.csv','w')
    f.write(str(tablehead))
    print tablehead
pass

if __name__ == '__main__':
    main()