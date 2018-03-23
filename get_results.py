# Imports the Google Cloud client library
# Probably run in local environment, eg `source activate GAE`
# requires the secret key in the system path as described in the google docs.
from google.cloud import datastore
import json


def get_all_testers():
    # Instantiates a client
    client = datastore.Client()
    query = client.query(kind='Tester')
    query_iter = query.fetch()
    return query_iter


def write_query(query, fname='subject01_query.json'):
    fmt = "%Y-%m-%d %H:%M:%S"
    data = dict(testers=[])
    for entity in query:
        answers = json.loads(entity['answers'])
        if len(answers) == 0:
            continue
        time = entity['time'].strftime(fmt)
        data['testers'].append(dict(answers=answers, time=time))
    with open(fname, 'wb') as fid:
        json.dump(data, fid, indent=1)


write_query(get_all_testers())
