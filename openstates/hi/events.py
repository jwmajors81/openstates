import datetime as dt

from billy.scrape import NoDataForPeriod
from billy.scrape.events import Event, EventScraper

from .utils import get_short_codes

import lxml.html
import pytz


URL = "http://www.capitol.hawaii.gov/upcominghearings.aspx"


class WIEventScraper(EventScraper):
    jurisdiction = 'hi'

    def lxmlize(self, url):
        page = self.urlopen(url)
        page = lxml.html.fromstring(page)
        page.make_links_absolute(url)
        return page

    def get_related_bills(self, href):
        ret = []
        page = self.lxmlize(href)
        bills = page.xpath(".//a[contains(@href, 'Bills')]")
        for bill in bills:
            try:
                row = bill.iterancestors(tag='tr').next()
            except StopIteration:
                continue
            tds = row.xpath("./td")
            descr = tds[1].text_content()
            ret.append({"bill_id": bill.text_content(),
                        "type": "consideration",
                        "descr": descr})

        return ret

    def scrape(self, session, chambers):
        get_short_codes(self)

        page = self.lxmlize(URL)
        table = page.xpath(
            "//table[@id='ctl00_ContentPlaceHolderCol1_GridView1']")[0]

        for event in table.xpath(".//tr")[1:]:
            tds = event.xpath("./td")
            committee = tds[0].text_content().strip()
            bills = [x.text_content() for x in tds[1].xpath(".//a")]
            descr = [x.text_content() for x in tds[1].xpath(".//span")]
            if len(descr) != 1:
                raise Exception
            descr = descr[0]
            when = tds[2].text_content().strip()
            where = tds[3].text_content().strip()
            notice = tds[4].xpath(".//a")[0]
            notice_href = notice.attrib['href']
            notice_name = notice.text
            when = dt.datetime.strptime(when, "%m/%d/%Y %I:%M %p")

            event = Event(session, when, 'committee:meeting', descr,
                          location=where)

            blacklist = ["INFO-CPC-TOU-LAB",
                         "INFO-CPN-ENE",
                         "INFO-WAM-HRE"]
            if committee in blacklist:
                continue

            if "/" in committee:
                committees = committee.split("/")
            else:
                committees = [committee,]

            for committee in committees:
                committee = self.short_ids[committee]
                event.add_participant('host', committee['name'], 'committee',
                                      chamber=committee['chamber'])

            event.add_source(URL)
            event.add_document(notice_name,
                               notice_href,
                               mimetype='text/html')

            for bill in self.get_related_bills(notice_href):
                event.add_related_bill(
                    bill['bill_id'],
                    description=bill['descr'],
                    type=bill['type']
                )

            self.save_event(event)
