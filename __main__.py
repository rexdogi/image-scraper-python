#!/usr/bin/env python3.5

from google_images_download import google_images_download
import requests
import json
import sys
import argparse
from os import remove

parser = argparse.ArgumentParser(description='Args')

parser.add_argument('-no_download', '--no_download', default=False, help='scraped urls will not be downloaded',
                    type=str, required=False)
parser.add_argument('-endpoint', '--endpoint', default='http://localhost:8080/dashboard/upload/google-images',
                    help='endpoint',
                    type=str, required=False)

parser.add_argument('-search', '--search', default='', help='search',
                    type=str, required=False)

parser.add_argument('-limit', '--limit', default=100, help='limit',
                    type=int, required=False)

parsed_args = parser.parse_args()

response = google_images_download.googleimagesdownload()
arguments = {
    "keywords": parsed_args.search,
    "limit": parsed_args.limit,
    "print_urls": True,
    "extract_metadata": True,
    "chromedriver": './chromedriver',
    'no_download': parsed_args.no_download,
}

absolute_image_paths = response.download(arguments)

with open('./logs/' + parsed_args.search + '.txt', 'r') as myfile:
    data = json.load(myfile)


headers = {'Content-Type': 'application/json'}

response = requests.post(parsed_args.endpoint, data=json.dumps(data), headers=headers)

print(data)

remove('./logs/' + parsed_args.search + '.txt')
