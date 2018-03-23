# Subjective Test One

Simple forced choice subjective test running on Google App Engine (GAE)
displaying randomised video with a choice question.
Saves 'Tester' entities to the datastore. Check google documentation for entities as methods may change.

### start the server

    dev_appserver.py app.yaml

### deploy the app

    gcloud app deploy app.yaml

### Activate the default cloud storage bucket

https://console.cloud.google.com

To activate the default Cloud Storage bucket for your app:

Click Create under Default Cloud Storage Bucket in the App Engine settings
page for your project. Notice the name of this bucket: it is in the form
<project-id>.appspot.com.


### Make sure to add the external libraries

https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27

    pip install -t lib/ <library_name>

see:

    appengine_config.py

### Media files in the config.

The key media_files in the config, lists the files that will be displayed, and also will be the key in the results. Most probably, the keys can be remote or locally stored.