#!/usr/bin/env python3
#
# dependencies
# pip3 install requests
# pip3 install python-dateutil

# run
# python3 logs-to-csv.py

import functools
import csv

import requests
import dateutil.parser
import urllib3

CONFIG_BASE_SERVER_URI = 'https://sds.stormshieldcs.eu'
CONFIG_TOKEN = 'YOUR_TOKEN_HERE'
CONFIG_OUTPUT_CSV = 'logs.csv'


def get_page(url):
    def _get_next_url(headers, current_url):
        def _extract_header_link_info(header):
            split = header.split('; ')
            return [split[1][5: - 1], split[0][1:- 1]]

        def _reducer(accumulator, link):
            accumulator[link[0]] = link[1]
            return accumulator

        filter_links = list(map(_extract_header_link_info,
                                headers['Link'].split(', ')))
        json_link = functools.reduce(_reducer, filter_links, {})
        if json_link['next'] == json_link['last'] == current_url:
            return None
        else:
            return json_link['next']

    res = requests.get(url, headers={
        'Authorization': CONFIG_TOKEN, 'Content-Type': 'application/json'
    }, verify=False)
    if res.status_code != 200:
        raise Exception(
            'An error occured! -> code: {} - message: {}'.format(res.status_code, res.json()['error']))
    return {'logs': res.json(), 'next': _get_next_url(res.headers, url)}


def list_to_csv(items):
    headers = []
    for item in items:
        headers = list(set(headers) | set(item.keys()))
    headers = sorted(headers)
    csv_list = [headers]
    for item in items:
        row = []
        for header in headers:
            value = item.get(header, '')
            if isinstance(value, list):
                value = ';'.join([email.get('email') for email in value])
            row.append(value)
        csv_list.append(row)
    return csv_list


def main():
    current_page = CONFIG_BASE_SERVER_URI + '/api/v1/logs?page=1'
    all_logs = []
    while current_page is not None:
        page = get_page(current_page)
        current_page = page['next']
        all_logs += page['logs']

    csv_list = list_to_csv(all_logs)

    with open(CONFIG_OUTPUT_CSV, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(csv_list)


if __name__ == '__main__':
    main()
