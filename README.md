# CreateAccountGroupsFromTags

Version: *1.0*
Author: *Marc Hobson and Eddie Beuerlein*

### Summary
This script will take GCP labels from running the RQL against 'gcloud-compute-project-info', match it against the list of keys in the config yaml and will take the value and create/update account groups based on the key/value pair.  It will then add any clound account/project that has that key/value pair to the account group.  This will allow you to run custom alert report, compliance report and alert rules based on these dyanmic account groups based on GCP labels.

### Requirements and Dependencies

1. Python 3.7 or newer

2. OpenSSL 1.0.2 or newer

(if using on Mac OS, additional items may be nessessary.)

3. Pip

```sudo easy_install pip```

4. Requests (Python library)

```sudo pip install requests```

5. YAML (Python library)

```sudo pip install pyyaml```

### Configuration

1. Navigate to *config/configs.yml*

2. Fill out your Prisma Cloud access key/secret, and stack info. To determine stack, look at your browser when access console (appX.prismacloud.io, where X is the stack number.  Change this to apiX.prismacloud.io and populate it in the configs.yml.

3. Pick the keys from the labels area of *gcloud-compute-project-info*

### Run

```
python main.py

```
