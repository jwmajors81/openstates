import datetime
from billy.utils.fulltext import pdfdata_to_text, text_after_line_numbers

metadata = dict(
    name='Arkansas',
    abbreviation='ar',
    legislature_name='Arkansas General Assembly',
    capitol_timezone='America/Chicago',
    chambers = {
        'upper': {'name': 'Senate', 'title': 'Senator'},
        'lower': {'name': 'House', 'title': 'Representative'},
    },
    terms=[
        {'name': '2011-2012',
         'start_year': 2011,
         'end_year': 2012,
         'sessions': ['2011', '2012F']},
        {'name': '2013-2014',
         'start_year': 2013,
         'end_year': 2014,
         'sessions': ['2013']}
        ],
    session_details={
        '2011': {'start_date': datetime.date(2011, 1, 10),
                 'end_date': datetime.date(2011, 4, 27),
                 'display_name': '2011 Regular Session',
                 '_scraped_name': 'Regular Session, 2011',
                 'type': 'primary',
                 'slug': '2011R',
                },
        '2012F': {'start_date': datetime.date(2012, 2, 13),
                 'display_name': '2012 Fiscal Session',
                 '_scraped_name': 'Fiscal Session 2012',
                 'type': 'special',
                 'slug': '2012F',
                },
        '2013': {'start_date': datetime.date(2013, 1, 14),
                 'display_name': '2013 Regular Session',
                 '_scraped_name': 'Regular Session, 2013',
                 'type': 'primary',
                 'slug': '2013R',
                }
        },
    feature_flags=['influenceexplorer'],
    _ignored_scraped_sessions=['Regular Session, 2009',
                               'Fiscal Session, 2010',
                               'Regular Session, 2007',
                               'First Extraordinary Session, 2008',
                               'Regular Session, 2005',
                               'First Extraordinary Session, 2006 ',
                               'Regular Session, 2003 ',
                               'First Extraordinary Session, 2003',
                               'Second Extraordinary Session, 2003',
                               'Regular Session, 2001 ',
                               'First Extraordinary Session, 2002',
                               'Regular Session, 1999',
                               'First Extraordinary Session, 2000',
                               'Second Extraordinary Session, 2000',
                               'Regular Session, 1997 ',
                               'Regular Session, 1995 ',
                               'First Extraordinary Session, 1995 ',
                               'Regular Session, 1993 ',
                               'First Extraordinary Session, 1993 ',
                               'Second Extraordinary Session, 1993',
                               'Regular Session, 1991',
                               'First Extraordinary Session, 1991 ',
                               'Second Extraordinary Session, 1991 ',
                               'Regular Session, 1989',
                               'First Extraordinary Session, 1989',
                               'Second Extraordinary Session, 1989',
                               'Third Extraordinary Session, 1989 ',
                               'Regular Session, 1987 ',
                               'First Extraordinary Session, 1987',
                               'Second Extraordinary Session, 1987',
                               'Third Extraordinary Session, 1987',
                               'Fourth Extraordinary Session, 1987']
    )

def session_list():
    from billy.scrape.utils import url_xpath
    sessions = url_xpath(
        'http://www.arkleg.state.ar.us/assembly/2013/2013R/Pages/Previous%20Legislatures.aspx',
        '//div[@id="ctl00_ctl15_g_91c28874_44ca_4b3e_9969_7202c1ca63dd_panel"]//a')
    return [s.text_content() for s in sessions if s.text_content()]


def extract_text(doc, data):
    return text_after_line_numbers(pdfdata_to_text(data))
