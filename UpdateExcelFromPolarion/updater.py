from __future__ import print_function
from pylarion.test_run import TestRun
from pylarion.work_item import TestCase
from pylarion.work_item import Requirement
from pylarion.test_record import TestRecord

import httplib2
import os
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():


    isUpdateAutomationValue = False
    # access excel file and update results
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    # https://docs.google.com/spreadsheets/d/1y4eBJhcZ0HsB5JUH5MPcFXWtc2zbP9XbgdCIF0S4iHs/edit#gid=1503195790
    spreadsheetId = '1y4eBJhcZ0HsB5JUH5MPcFXWtc2zbP9XbgdCIF0S4iHs'

    # Get all test runs by Polarion query, extract test run id and test run results (pass, fail, pending block, total...)


    test_runs_uris = TestRun.search('NOT status:invalid AND plannedin.KEY:RHOS15 AND updated:[20190415 TO 20190417]')
    # test_runs_uris = TestRun.search('20180625-0836')
    print ("Number of items %s" % len(test_runs_uris))
    loop_counter = 1;
    missing_test_run_in_excel = ''
    non_test_cases_item = 0

    for test_run_uri in test_runs_uris:
    # for i in range(41,107):
    #     test_run_uri = test_runs_uris[i]

        #get excel values
        rangeName = 'RHOS 15!A2:X'
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])
        value_input_option = 'RAW'

        print('Updating test run number: ' + str(loop_counter))
        loop_counter +=1

        print (test_run_uri.uri)
        test_run = TestRun(uri=test_run_uri.uri)
        test_run_id = test_run.test_run_id

        print ('Test run title: ' + test_run.title)
        print ('Test run ID: ' + test_run.test_run_id)


        records = test_run.records
        pass_counter = 0
        fail_counter = 0
        pending_counter = 0
        automation_counter = 0.0
        critical_counter = 0
        critical_auto_counter = 0
        #automation_percentage = 0
        blocked_counter = 0
        total_counter = 0

        #Collect inforamtion about test runs, how many test pass

        if test_run.TestRunType == 'Acceptance':

            for record in records:
                if record.result == 'passed':
                    pass_counter += 1
                elif record.result == 'failed':
                    fail_counter += 1
                elif record.result == 'blocked':
                    blocked_counter += 1
                else:
                    pending_counter += 1
        else:
            for record in records:
                # print record.result
                #check if test is automated

                test = TestCase.query(record.test_case_id)


                # print('Test case ID: ' + record.test_case_id)
                # Check if the object type is a testcase and not a header for example!
                if test and not Requirement.query(record.test_case_id):

                    #calculate critical automated and rest automated
                    if isUpdateAutomationValue:
                        if test[0].caseautomation.lower() == 'automated':
                            automation_counter +=1
                            if test[0].caseimportance.lower() == 'critical':
                                critical_auto_counter += 1
                        #count number of critical cases
                        if test[0].caseimportance.lower() == 'critical':
                            critical_counter += 1

                    if record.result == 'passed':
                        pass_counter += 1
                    elif record.result == 'failed':
                        fail_counter += 1
                    elif record.result == 'blocked':
                        blocked_counter += 1
                    else:
                        pending_counter += 1
                else:
                    non_test_cases_item += 1

        total_counter = pass_counter + fail_counter + blocked_counter + pending_counter
        # if total_counter > 0:
        #     automation_percentage = int(float(automation_counter)/float(total_counter)) #*100

        print ('Total pass:', pass_counter)
        print ('Total fail:', fail_counter)
        print ('Total blocked:', blocked_counter)
        print ('Total pending:', pending_counter)
        print ('Total automated:', automation_counter)
        print('Number of critical:', critical_counter)
        print('Number of critical auto:', critical_auto_counter)
        #print ('Automation percentage:', automation_percentage)
        print ('Total number of test cases:', total_counter)

        row_counter = 1  # offset due to headers
        title_column_number = 2
        total_column_number = 8
        pass_column_number = 9
        fail_column_number = 10
        blocked_column_number = 11
        test_run_id_column_number = 20
        automation_percentage_column_number = 18
        critical_test_number = 22
        is_test_run_exist_in_excel = None

        if not values:
            print('No data found.')
        else:
            for row in values:
                is_test_run_exist_in_excel = False
                row_counter +=1
                # Check that row contains test run id in cell R AND check that test_run_id is match
                if row.__len__() >= 20 and row[test_run_id_column_number] == test_run_id:
                    print('Row number is: ' + str(row_counter))
                    is_test_run_exist_in_excel = True
                    #  print('%s, %s, %s, %s, %s, %s, %s :' % (row[title_column_number], row[total_column_number], row[pass_column_number], row[fail_column_number], row[blocked_column_number],row[automation_percentage_column_number], row[critical_test_number]))
                    values = [
                        [total_counter, total_counter,pass_counter,fail_counter,blocked_counter]
                    ]
                    body = {
                        'values': values
                    }

                    rangeName =  'RHOS 15!H' + str(row_counter) + ':L' + str(row_counter)
                    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()

                    # # update automation percentage field
                    # values = [
                    #     [automation_percentage]
                    # ]
                    # body = {
                    #     'values': values
                    # }
                    # rangeName = 'RHOS 13!S' + str(row_counter)
                    # result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption='USER_ENTERED',body=body).execute()


                    # update PQI values...
                    if isUpdateAutomationValue and test_run.TestRunType != 'Acceptance':
                        values = [
                            [automation_counter,critical_counter,critical_auto_counter]
                        ]
                        body = {
                            'values': values
                        }
                        rangeName = 'RHOS 15!V' + str(row_counter) + ':X' + str(row_counter)
                        result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option,body=body).execute()

                    # done with update, move to next test run
                    break
        #Check if test run exist in excel file and was updated
        if not is_test_run_exist_in_excel:
            missing_test_run_in_excel += test_run_id + ", "

    print ("Missing Test Runs in Excel: " + missing_test_run_in_excel)
    print ("Number of headers or requirements in test runs: ", non_test_cases_item)




def check_for_spare_test_runs_in_excel():

    print("Test run in excel but not in Polarion already: ")
    test_run_ids = [""]
    print(test_run_ids.__len__())


    for id in test_run_ids:
        test_run = TestRun.search(id)
        if not test_run.__len__():
            print(id)



if __name__ == '__main__':
    start_time = time.time()

    main()
    # check_for_spare_test_runs_in_excel()


    print("time elapsed: {:.2f}s".format(time.time() - start_time))