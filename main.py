import lib
import json
from collections import defaultdict

class CreateAccountGroup():
    def __init__(self):
        self.config = lib.ConfigHelper()
        self.rl_sess = lib.RLSession(self.config.rl_user, self.config.rl_pass, self.config.rl_cust,
                                     self.config.rl_api_base)

    def get_ProjectInfoTags(self):
        self.url = "https://" + self.config.rl_api_base + "/search/config"  # pull "project info"
        self.rl_sess.authenticate_client()

        ProjectInfoPayload = {
            "query": "config where api.name = 'gcloud-compute-project-info' AND json.rule = labels exists",
            "timeRange": {"type": "relative", "value": {"unit": "hour", "amount": 24}, "relativeTimeType": "BACKWARD"}}
        ProjectInfo = self.rl_sess.client.post(self.url, json.dumps(ProjectInfoPayload))
        ProjectInfo_json = ProjectInfo.json()  # convert to JSON

        ProjectTagsDict = defaultdict(list)  # <<<====== Create Empty Dictionary. Stores Project name and labels

        for projects in ProjectInfo_json['data']['items']:
            for k, v in projects['data']['labels'].items():
                if k in self.config.rl_tagkeys:  # <<<======= configs.yml labels to list
                    combinedkey = k + "_" + v
                    ProjectTagsDict[combinedkey].append(projects['accountId'])
        return dict(ProjectTagsDict)


    def update_accountGroups(self,ID,name,AccountGroupIDs):                #<==Update Account Groups with Cloud Accounts
        AccountGroupPayload = json.dumps({'accountIds': AccountGroupIDs, 'name': name, 'description': 'DO NOT MODIFY. POPULATED VIA AUTOMATION'})

        self.url = "https://" + self.config.rl_api_base + "/cloud/group/" + ID
        self.rl_sess.authenticate_client()
        status = self.rl_sess.client.put(self.url,AccountGroupPayload)

        print('Updating account group {}'.format(name))

    def create_AccountGroups(self,AccountGroupName,AccountGroupIDs):     #<==Create Account Groups with Cloud Accounts
        AccountGroupPayload = json.dumps({'accountIds': AccountGroupIDs, 'name': AccountGroupName, 'description': 'DO NOT MODIFY. POPULATED VIA AUTOMATION'})

        self.url = "https://" + self.config.rl_api_base + "/cloud/group"
        self.rl_sess.authenticate_client()
        status = self.rl_sess.client.post(self.url,AccountGroupPayload)

        print('Creating account group {}'.format(AccountGroupName))

    def check_AccountGroup(self,ProjectTagsDict2): #pull account groups, compare with creat_AccountGroups, call create and update
        self.url = "https://" + self.config.rl_api_base + "/cloud/group"  # pull "Account Group info" GET
        self.rl_sess.authenticate_client()

        AccountGroupList = self.rl_sess.client.get(self.url)
        AccountGroupList_json = AccountGroupList.json()  # convert to JSON

        createcount = 0
        updatecount = 0

        NewAccountGroups = {}

        for k, v in ProjectTagsDict2.items():
            counter = 0                                    #<===Counter for finding account group names
            for AccountGroup in AccountGroupList_json:
                AccountGroupIDsList = []                   #Clear list every time
                if k == AccountGroup['name']:              #<=====If something equals, then UPDATE account group
                    counter += 1                           #<=== Increment counter upon finding match of AGnames
                    for i in v:
                        if i in AccountGroup['accountIds']:
                            continue
                        else:
                            AccountGroupIDsList.append(i)
                if AccountGroupIDsList:
                    AccountGroupIDsList.extend(AccountGroup['accountIds'])
                    ID = AccountGroup['id']
                    name = AccountGroup['name']
                    self.update_accountGroups(ID, name, AccountGroupIDsList)   #Call Update Account Group Function from above
                    updatecount += 1

            # If counter is 0 (doesn't find name) then
            # append to list to be added to create account group
            if counter == 0:
                NewAccountGroups.update({k:v})

        for k, v in NewAccountGroups.items():
            self.create_AccountGroups(k,v)
            createcount += 1
        print("\n***SUMMARY***")
        if createcount == 0 and updatecount == 0:
            print("No Account Groups were created or updated.")
        if createcount > 0:
            print("{} Account Groups were created".format(createcount))
        if updatecount > 0:
            print("{} Account Groups were updated".format(updatecount))


    def run(self):
        ProjectTagsDict2 = self.get_ProjectInfoTags()
        self.check_AccountGroup(ProjectTagsDict2)

def main():
    run_CreateAccountGroup = CreateAccountGroup()
    run_CreateAccountGroup.run()

if __name__ == "__main__":
    main()