from google_images_download import google_images_download
import requests
import json
import sys
import argparse
from os import remove
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# parser = argparse.ArgumentParser(description='Args')
#
# parser.add_argument('-no_download', '--no_download', default=False, help='scraped urls will not be downloaded',
#                     type=str, required=False)
# parser.add_argument('-endpoint', '--endpoint', default='http://localhost:8080/dashboard/upload/google-images',
#                     help='endpoint',
#                     type=str, required=False)
#
# parser.add_argument('-search', '--search', default='', help='search',
#                     type=str, required=False)
#
# parser.add_argument('-limit', '--limit', default=100, help='limit',
#                     type=int, required=False)

parser = reqparse.RequestParser()
parser.add_argument('endpoint', type=str, default='http://localhost:8080/dashboard/upload/google-images')
parser.add_argument('search', type=str, default='', required=False)
parser.add_argument('limit', type=str, default=100, required=False)
parser.add_argument('no_download', type=str, default=True, required=False)
parser.add_argument('domain', type=str, default='', required=False)
parser.add_argument('time', type=str, default='', required=False)


class Scrape(Resource):
    def get(self):
        parsed_args = parser.parse_args()

        print(parsed_args.search)

        response = google_images_download.googleimagesdownload()
        arguments = {
            "keywords": parsed_args.search,
            "limit": parsed_args.limit,
            "print_urls": True,
            "extract_metadata": True,
            'time': parsed_args.time,
            'specific_site': parsed_args.domain,
            # "chromedriver": './chromedriver',
            'no_download': parsed_args.no_download,
        }

        absolute_image_paths = response.download(arguments)

        with open('./logs/' + parsed_args.search + '.txt', 'r') as myfile:
            data = json.load(myfile)

        headers = {'Content-Type': 'application/json'}

        response = requests.post(parsed_args.endpoint, data=json.dumps(data), headers=headers)

        print(data)

        remove('./logs/' + parsed_args.search + '.txt')

        return response


api.add_resource(Scrape, '/scrape')

if __name__ == '__main__':
    app.run(debug=True)
