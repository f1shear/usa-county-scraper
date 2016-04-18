

import urllib2
from lxml import etree
import csv


WIKI_COUNTIES_URL = 'https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents'


def read_url(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page = response.read()
    return page


def parse_page(page):
    tree = etree.fromstring(page)
    return tree


def collect_counties():
    counties = []
    states = []

    page = read_url(WIKI_COUNTIES_URL)
    tree = parse_page(page)

    rows = tree.xpath('//table[@class="wikitable sortable"]/tr')

    header = True

    for row in rows:

        if header:
            header = False
            continue

        columns = row.getchildren()

        incits = columns[0].text
        county = columns[1].find('a').text
        state = columns[2].find('a').text

        counties.append([incits, county, state])

        if state not in states:
            states.append(state)

    return states, counties


def generate_file(counties):

    with open('counties.csv', 'wb') as csvfile:

        handler = csv.writer(
            csvfile, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for county in counties:
            handler.writerow([unicode(s).encode("utf-8") for s in county])


if __name__ == '__main__':
    states, counties = collect_counties()

    print 'Total Number of States %s' % len(states)
    print 'Total Number of Counties %s' % len(counties)

    print 'Output generated in counties.csv'

    generate_file(counties)
