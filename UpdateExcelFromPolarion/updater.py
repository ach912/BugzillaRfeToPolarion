from __future__ import print_function
from pylarion.test_run import TestRun
from pylarion.work_item import TestCase


import httplib2
import os
import time

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


    # access excel file and update results
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    # https://docs.google.com/spreadsheets/d/1y4eBJhcZ0HsB5JUH5MPcFXWtc2zbP9XbgdCIF0S4iHs/edit#gid=1503195790
    spreadsheetId = '1y4eBJhcZ0HsB5JUH5MPcFXWtc2zbP9XbgdCIF0S4iHs'

    # Get all test runs by Polarion query, extract test run id and test run results (pass, fail, pending block, total...)
    # plannedin.KEY:RHOS12


    test_runs_uris = TestRun.search('NOT status:invalid AND plannedin.KEY:RHOS12 AND TestRunType.KEY:(regression featureverification)')
    #    test_runs_uris = TestRun.search('20171016-1350')
    print ("Number of items %s" % len(test_runs_uris))
    loop_counter = 1;
    missing_test_run_in_excel = ''
    non_test_cases_item = 0




    for test_run_uri in test_runs_uris:
#    for i in range(104,135):
 #       test_run_uri = test_runs_uris[i]
        #get excel values
        rangeName = 'RHOS 12!A2:V'
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
        automation_counter = 0
        critical_counter = 0
        critical_auto_counter = 0
        automation_percentage = 0
        blocked_counter = 0
        total_counter = 0


        for record in records:
            # print record.result
            #check if test is automated

            test = TestCase.query(record.test_case_id)

            # 'caseautomation.KEY:automated AND ' +
            # print('Test case ID: ' + record.test_case_id)
            # Check if the object type is a testcase and not a header for example!
            if test:

                #calculate critical automated and rest automated
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
        if total_counter > 0:
            automation_percentage = int(float(automation_counter)/float(total_counter) * 100)

        print ('Total pass:', pass_counter)
        print ('Total fail:', fail_counter)
        print ('Total blocked:', blocked_counter)
        print ('Total pending:', pending_counter)
        print ('Total automated:', automation_counter)
        print('Number of critical:', critical_counter)
        print('Number of critical auto:', critical_auto_counter)
        print ('Automation percentage:', automation_percentage)
        print ('Total number of test cases:', total_counter)


        row_counter = 1  # offset due to headers
        title_column_number = 1
        total_column_number = 7
        pass_column_number = 8
        fail_column_number = 9
        blocked_column_number = 10
        test_run_id_column_number = 17
        automation_percentage_column_number = 15
        critical_test_number = 19
        is_test_run_exist_in_excel = None

        if not values:
            print('No data found.')
        else:
            for row in values:
                is_test_run_exist_in_excel = True
                row_counter +=1
                # Check that row contains test run id in cell R AND check that test_run_id is match
                if row.__len__() >= 18 and row[test_run_id_column_number] == test_run_id:
                    print('Row number is: ' + str(row_counter))
  #                  print('%s, %s, %s, %s, %s, %s, %s :' % (row[title_column_number], row[total_column_number], row[pass_column_number], row[fail_column_number], row[blocked_column_number],row[automation_percentage_column_number], row[critical_test_number]))
                    values = [
                        [total_counter,pass_counter,fail_counter,blocked_counter]
                    ]
                    body = {
                        'values': values
                    }

                    rangeName =  'RHOS 12!H' + str(row_counter) + ':K' + str(row_counter)
                    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()

                    # update automation percentage field
                    values = [
                        [automation_percentage]
                    ]
                    body = {
                        'values': values
                    }
                    rangeName = 'RHOS 12!P' + str(row_counter)
                    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option,body=body).execute()


                    # update PQI values...
                    values = [
                        [automation_counter,critical_counter,critical_auto_counter]
                    ]
                    body = {
                        'values': values
                    }
                    rangeName = 'RHOS 12!S' + str(row_counter) + ':U' + str(row_counter)
                    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option,body=body).execute()

                    # done with update, move to next test run
                    break
        #Check if test run exist in excel file and was updated
        if not is_test_run_exist_in_excel:
            missing_test_run_in_excel += test_run_id + ", "

    print ("Missing Test Runs in Excel: " + missing_test_run_in_excel)
    print ("Number of headers in test runs: ", non_test_cases_item)

if __name__ == '__main__':
    start_time = time.time()

    main()

    print("time elapsed: {:.2f}s".format(time.time() - start_time))