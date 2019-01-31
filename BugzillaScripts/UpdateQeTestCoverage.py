import ConfigParser
import datetime
import os
import re
import user

import bugzilla

BUGZILLA_SERVER = "https://bugzilla.redhat.com/xmlrpc.cgi"
BUGZILLA_PRODUCT= "Red Hat OpenStack"
BUGZILLA_VERSION = "13.0 (Queens)"


class ConfigFileMissingException(Exception):
    pass

def parse_config():
    conf_file = os.path.join(user.home, ".pylarion")
    if not os.path.isfile(conf_file):
        raise ConfigFileMissingException

    config = ConfigParser.RawConfigParser()
    config.read(conf_file)
    params_dict = {}
    for params in config.items("webservice"):
        params_dict[params[0]] = params[1]

    return params_dict

def get_rfes_from_bugzilla():
    # Open connection into bugzilla
    user_params = parse_config()
    username = user_params.get("user") + "@redhat.com"
    password = user_params.get("password")

  #  rhbugzilla = bugzilla.RHBugzilla()

    bz_connection = bugzilla.RHBugzilla(url=BUGZILLA_SERVER)
    bz_connection.login(username,password)
    # query

    print "Bugzilla connection: " + str(bz_connection.logged_in)

    query = bz_connection.build_query(
        savedsearch="QE_Test_Coverage_RHOS_7"
    )

    bz_rfes = bz_connection.query(query)

    return bz_rfes, bz_connection


if __name__ == "__main__":

    bug_list, bz_connection = get_rfes_from_bugzilla()
    print "Number of bugs in saved Search" + BUGZILLA_VERSION + ": %s" %bug_list.__len__()

    for bug in bug_list:
        print('Updating Bugzilla: {}'.format(bug.id))
        bug.updateflags({'qe_test_coverage': '-'})







