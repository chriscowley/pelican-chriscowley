#!/usr/bin/env python
import argparse
from datetime import date

def generate_metadata():
    metadata = dict()
    parser = argparse.ArgumentParser(description='Create a new Pelican post')
    parser.add_argument('-T', '--title',
            help='Title of the new post',
            required=True
            )
    args = vars(parser.parse_args())
    metadata['title'] = args['title']
    metadata['slug'] = args['title'].lower().replace(' ', '-')
    metadata['date'] = date.today().isoformat()
    return metadata

def create_post(metadata):
    filename = "content/" + metadata['date'] + "-" + metadata['slug'] + ".rst"
    underline = ""
    for i in range(len(metadata['title'])):
        underline += "#"

    header = [
            "%s\n" % metadata['title'],
            "%s\n\n" % underline,
            ":slug: %s\n" % metadata['slug'],
            ":data: %s\n" % metadata['date'],
            ":category: <fill me>\n",
            ":tags: \n",
            ":summary: \n",
            "\nContent\n",
            ]
    outputfile = open(filename, 'w')
    outputfile.writelines(header)
    outputfile.close()

    print ("Created %s\n" % filename)


if __name__ == "__main__":
    metadata = generate_metadata()
    create_post(metadata)
