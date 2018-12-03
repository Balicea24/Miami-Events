from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import calendar
import sys
import inspect
from xlwt import Workbook
import os
import xlrd

class Clubs:
    def __init__(self):
        self.eventName = []
        self.eventDate = []
        self.eventUrl = []
        self.eventDay = []
        self.eventMonth = []
        self.eventFormat = []
        self.days = list(calendar.day_name)
        self.months = list(calendar.month_name)

    def getDay(self, eventDay):
        for count,day in enumerate(self.days):
            if eventDay in (''.join(list(day[0:3]))):
                return (self.days[count])

    def getMonth(self, eventMonth):
        for count,month in enumerate(self.months):
            if eventMonth in (''.join(list(month[0:3]))):
                if count < 10:
                    return (self.months[count], "0" + str(count))

                else:
                    return (self.months[count], str(count))

    def normalizeDay(self, day):
        if len(day) == 1:
            return "0" + day

        else:
            return day

    def insertInfo(self, clubName):
        clubName = wb.add_sheet(clubName)
        columns = ["eventName", "eventDate", "eventUrl", "eventDay", "eventMonth", "eventFormat"]

        for count, column in enumerate(columns):
            list(map(lambda event: clubName.write(event, count, getattr(self, column)[event]), [event for event in range(len(getattr(self, column)))]))

class Space(Clubs):
    def getUrl(self, clubName):
        self.info(BeautifulSoup(urlopen('https://www.clubspace.com/events/'), "html.parser"))
        self.insertInfo(clubName)

    def info(self, soup):
        tags = soup.find_all('div', attrs = {'class' : 'eventlist-column-info'})
        for count, tag in enumerate(tags):
            dateInfo = tag.find('time', attrs = {'class' : 'event-date'}).text.split(", ")
            if len(dateInfo[1].split(" ")[1]) > 3:
                day = self.normalizeDay((dateInfo[1].split(" ")[1])[0:2])[1]

            else:
                day = self.normalizeDay(dateInfo[1].split(" ")[1])

            if len(dateInfo[1].split(" ")[0]) > 3:
                month = self.getMonth((dateInfo[1].split(" ")[0])[0:2])[1]

            else:
                month = self.getMonth(dateInfo[1].split(" ")[0])[1]

            year = dateInfo[2]
            if count > 1:
                if int(year + month + day) < int(self.eventDate[count - 1]):
                    break

            self.eventDate.append(year + month + day)
            self.eventName.append(tag.find('h1').text)
            if len(dateInfo[0]) > 3:
                self.eventDay.append(dateInfo[0])
            else:
                self.eventDay.append(self.getDay(dateInfo[0]))

            self.eventFormat.append(month + "." + day)
            if len(dateInfo[1].split(" ")[0]) > 3:
                self.eventMonth.append(dateInfo[1].split(" ")[0])

            else:
                self.eventMonth.append(self.getMonth(dateInfo[1].split(" ")[0])[0])

        tagsUrl = soup.find_all('div', attrs = {'class' : 'eventlist-description'})
        for tag in tagsUrl[0:count]:
            self.eventUrl.append(tag.find('a')['href'])

class Treehouse(Clubs):
    def getUrl(self, clubName):
        self.info(BeautifulSoup(urlopen('https://www.eventbrite.com/o/treehouse-miami-17386576012'), "html.parser"))
        self.insertInfo(clubName)

    def info(self, soup):
        year = time.strftime("%Y")
        tags = soup.find_all('div', attrs = {'class' : 'list-card-v2 l-mar-top-2 js-d-poster'})
        for count, tag in enumerate(tags):
            dateInfo = tag.find('time', attrs = {'list-card__date'}).text.strip().split(" ")
            day = self.normalizeDay(dateInfo[2].strip())
            month = self.getMonth(dateInfo[1])[1]

            if count > 1:
                if abs(int(month) - int(self.eventDate[count - 1][4:6])) > 9:
                    year = int(time.strftime("%Y")) + 1

                if int(year + month + day) < int(self.eventDate[count - 1]):
                    break

            self.eventDate.append(year + month + day)
            self.eventUrl.append(tag.find('a')['href'])
            self.eventName.append(tag.find('div', attrs = {'list-card__title'}).text.split(" @")[0].strip())
            self.eventMonth.append(self.getMonth(dateInfo[1])[0])
            self.eventDay.append(self.getDay(dateInfo[0].split(",")[0]))
            self.eventFormat.append(month + "." + day)

class ElectricPickle(Clubs):
    def getUrl(self, clubName):
        self.info(BeautifulSoup(urlopen(Request('https://www.residentadvisor.net/club.aspx?id=9993', headers = {'User-Agent': 'Mozilla/5.0'})), 'html.parser'))
        self.insertInfo(clubName)

    def info(self, soup):
        tags = soup.find_all('div', attrs = {'class' : 'bbox'})
        for tag in tags[2:-1]:
            dateInfo = (tag.find('h1').contents[0])
            day = dateInfo.split(" ")[1]
            month = self.getMonth(dateInfo.split(" ")[2])[1]
            year = dateInfo.split(" ")[3]

            self.eventDate.append(year + month + day)
            self.eventUrl.append('https://www.residentadvisor.net' + tag.find('a')['href'])
            self.eventName.append(tag.find('span', attrs = {'class' : 'title'}).contents[0])
            self.eventMonth.append(self.getMonth(dateInfo.split(" ")[2])[0])
            self.eventDay.append(self.getDay(dateInfo.split(", ")[0]))
            self.eventFormat.append(month + "." + day)

class Story(Clubs):
    def getUrl(self, clubName):
        self.info(BeautifulSoup(urlopen('https://www.tixr.com/groups/story/events'), "html.parser"))
        self.insertInfo(clubName)

    def info(self, soup):
        tags = soup.find_all('a', attrs = {'alt' : True})
        for tag in tags:
            dateInfo = tag.find_all('span')[2]['content'].split("-")
            year = dateInfo[0]
            if dateInfo[2].split("T")[0] == '01':
                month = str(int(dateInfo[1]) - 1)
                if len(month) == 1:
                    month = '0' + month

                if month == '00':
                    month = '12'

                day = self.normalizeDay(str(calendar.monthrange(int(year), int(month))[1]))

            else:
                month = dateInfo[1]
                day = self.normalizeDay(str(int(dateInfo[2].split("T")[0]) - 1))

            self.eventDate.append(year + str(month) + day)
            self.eventUrl.append(tag['href'])
            self.eventName.append(tag.find('span').text)
            self.eventMonth.append(self.months[int(month)])
            self.eventDay.append(self.days[(calendar.weekday(int(year), int(month), int(day)))])
            self.eventFormat.append(str(month) + "." + day)

class LIV(Story):
    def getUrl(self, clubName):
        super().info(BeautifulSoup(urlopen('https://www.tixr.com/groups/liv/events'), "html.parser"))
        self.insertInfo(clubName)

class E11even(Story):
    def getUrl(self, clubName):
        super().info(BeautifulSoup(urlopen('https://www.tixr.com/groups/11miami/events/'), "html.parser"))
        self.insertInfo(clubName)

class DoNotSitOnTheFurniture(ElectricPickle):
    def getUrl(self, clubName):
        super().info(BeautifulSoup(urlopen(Request("https://www.residentadvisor.net/club.aspx?id=80115", headers = {'User-Agent': 'Mozilla/5.0'})), 'html.parser'))
        self.insertInfo(clubName)

if __name__ == '__main__':
    wb = Workbook()
    clsmembers = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__ and 'info' in dir(member))
    list(map(lambda club: eval(club)().getUrl(club), [club[0] for club in clsmembers]))
    current_dir = os.path.dirname(os.path.realpath(__file__))
    wb.save(str(current_dir) + '/ClubsInfo.xls')

def getInfo(club):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ClubsInfo.xls')
    book = xlrd.open_workbook(path, 'r')
    sheet = book.sheet_by_name(club)

    rows = []
    for row in range(sheet.nrows):
        rows.append(sheet.row(row))

    events = []
    for event in rows:
        events.append([])
        for type in event:
            events[-1].append(type.value)

    return events
