import ConfigParser
import datetime
import os
import re
import user

import bugzilla

from pylarion.exceptions import PylarionLibException
from pylarion.hyperlink import Hyperlink
from pylarion.plan import Plan
from pylarion.text import Text
from pylarion.user import User
from pylarion.work_item import Requirement
import time

BUGZILLA_SERVER = "https://bugzilla.redhat.com/xmlrpc.cgi"
BUGZILLA_PRODUCT= "Red Hat OpenStack"
BUGZILLA_VERSION = "13.0 (Queens)"
POLARION_PRODUCT = "RHELOpenStackPlatform"
POLARION_VERSION = "RHOS13"



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


def convert_polarion_dfg(bug_dfg):
    dfg_id = ""
    if bug_dfg.startswith("DFG:Ceph"):
        dfg_id = "24"
    elif bug_dfg.startswith("DFG:Compute"):
        dfg_id = "6"
    elif bug_dfg.startswith("DFG:CloudApp"):
        dfg_id = "23"
    elif bug_dfg.startswith("DFG:Containers"):
        dfg_id = "25"
    elif bug_dfg.startswith("DFG:DF"):
        dfg_id = "7"
    elif bug_dfg.startswith("DFG:HardProv"):
        dfg_id = "9"
    elif bug_dfg.startswith("DFG:Infra"):
        dfg_id = "5"
    elif bug_dfg.startswith("DFG:MetMon"):
        dfg_id = "27"
    elif bug_dfg.startswith("DFG:NFV"):
        dfg_id = "11"
    elif bug_dfg.startswith("DFG:Networking"):
        dfg_id = "10"
    elif bug_dfg.startswith("DFG:ODL"):
        dfg_id = "3"
    elif bug_dfg.startswith("DFG:OVN"):
        dfg_id = "17"
    elif bug_dfg.startswith("DFG:OpsTools"):
        dfg_id = "4"
    elif bug_dfg.startswith("DFG:PIDONE"):
        dfg_id = "19"
    elif bug_dfg.startswith("DFG:ReleaseDelivery"):
        dfg_id = "13"
    elif bug_dfg.startswith("DFG:Security"):
        dfg_id = "14"
    elif bug_dfg.startswith("DFG:Storage"):
        dfg_id = "15"
    elif bug_dfg.startswith("DFG:Telemetry"):
        dfg_id = "16"
    elif bug_dfg.startswith("DFG:UI"):
        dfg_id = "8"
    elif bug_dfg.startswith("DFG:Upgrades"):
        dfg_id = "22"
    elif bug_dfg.startswith("DFG:Workflows"):
        dfg_id = "28"
    elif bug_dfg.startswith("DFG:OpenShiftonOpenStack"):
        dfg_id = "26"
    else:
        dfg_id = ""

    return dfg_id


def convert_polarion_priority(bugzilla_priority):
    priority = ''
    if bugzilla_priority == "urgent":
        priority = float(90.0)
    elif bugzilla_priority == "high":
        priority = float(70.0)
    elif bugzilla_priority == "medium":
        priority = float(50.0)
    elif bugzilla_priority == "low":
        priority = float(30.0)
    elif bugzilla_priority == "unspecified":
        priority = float(10.0)

    return priority

def convert_polarion_severity(bugzilla_severity):
    severity = ""
    if bugzilla_severity == "urgent":
        severity = "must_have"
    elif bugzilla_severity == "high":
        severity = "must_have"
    elif bugzilla_severity == "medium":
        severity = "should_have"
    elif bugzilla_severity == "low":
        severity = "nice_to_have"
    elif bugzilla_severity == "unspecified":
        severity = "will_not_have"

    return severity

def get_bug_params(bug):
    named_parms = dict()
    bug_summary = re.sub(r"[^\x00-\x7F]+", " ", bug.summary)
    priority = bug.priority
    severity = bug.severity
    bug_id = bug.id
    description = ""
    if bug.getcomments():
        comment = bug.getcomments()[0]
        # the description is always the first comment.
        description = comment["text"]

    dfg = bug.internal_whiteboard

    return bug_summary, named_parms, description, bug.weburl, bug_id, priority,severity, dfg

def isRequirementInPolarion(bug_link):
    for i in range(0, 10):  # WA for Polarion disconnection from time to time
        try:
            if Requirement.query('"{}"'.format(bug_link)):
                print "\nRequirement already in Polarion: " + str(bug_link)
                return True
            break
        except Exception as inst:
            print inst
            i += 1
            time.sleep(10)

    return False

def get_rfes_from_bugzilla():
    # Open connection into bugzilla
    user_params = parse_config()
    username = user_params.get("user") + "@redhat.com"
    password = user_params.get("password")

  #  rhbugzilla = bugzilla.RHBugzilla()

    bz_connection = bugzilla.RHBugzilla(url=BUGZILLA_SERVER)
    bz_connection.login(username,password)
    # Build RFE query
    #https: // bugzilla.redhat.com / buglist.cgi?action = wrap & bug_status = NEW & bug_status = ASSIGNED & bug_status = POST & bug_status = MODIFIED & bug_status = ON_DEV & bug_status = ON_QA & bug_status = VERIFIED & classification = Red % 20
    #Hat & f1 = component & f2 = cf_devel_whiteboard & f3 = cf_devel_whiteboard & keywords = FutureFeature % 2
    #C % 20 & keywords_type = allwords & list_id = 8251986 & o1 = notsubstring & o2 = substring & o3 = notsubstring & product = Red % 20
    #Hat % 20 OpenStack & v1 = doc & v2 = osp13add & v3 = osp13rem

    print "Bugzilla connection: " + str(bz_connection.logged_in)

    query = bz_connection.build_query(
        product = BUGZILLA_PRODUCT,
        #version = BUGZILLA_VERSION,.
        keywords = "FutureFeature",
        status = "NEW, ASSIGNED, POST, MODIFIED, ON_DEV, ON_QA, VERIFIED"
    )

    query["query_format"] = "advanced"
    query["classification"] = "Red Hat"
    query["f1"] = "component"
    query["o1"] = "notsubstring"
    query["v1"] = "doc"
    query["f2"] = "cf_devel_whiteboard"
    query["o2"] = "substring"
    query["v2"] = "osp13add"
    query["f3"] = "cf_devel_whiteboard"
    query["o3"] = "notsubstring"
    query["v3"] = "osp13rem"

    bz_rfes = bz_connection.query(query)

    return bz_rfes, bz_connection

def create_requirements(bz_rfes, bz_connection):
    idx = 103


    plan = Plan(project_id=POLARION_PRODUCT, plan_id=POLARION_VERSION)
    req_ids = list()

    # bz_rfe = bz_rfes[0]
    #for x in range(103,127):
    for bz_rfe in bz_rfes:
        #bz_rfe = bz_rfes[x]

        bug_title, named_parms, bug_description, bug_link, bug_id, bug_priority,bug_severity, bug_dfg = get_bug_params(bz_rfe)
        print "\n%s - start bug %s" % (datetime.datetime.now(), idx),
        idx +=1
        print '"{}"'.format(bug_link)


        if isRequirementInPolarion(bug_link) == False:

            #TODO Convert bugzilla to Polarion priority and set
            #named_parms["priority"] = convert_polarion_priority(bug_priority)

            # Convert bugzilla to Polarion severity and set
            named_parms["severity"] = convert_polarion_severity(bug_severity)

            # Set Polarion requirement type
            named_parms["reqtype"] = "functional"

            #Cenvert DFG name from bugzilla to dfg_id in Polarion
            named_parms["d_f_g"] = convert_polarion_dfg(bug_dfg)

            #Get bug description from first comment and add to Polarion requirement
            desc = ""
            if bug_description:
                desc = Text(bug_description.encode('ascii', 'ignore').decode('ascii'))
                # decode("utf-8"))
                desc.content_type = "text/plain"

            # Add hyperlink to bugzilla
            link = Hyperlink()
            link.role = "ref_ext"
            link.uri = bug_link

            for i in range(0,10): #WA for Polarion disconnection from time to time
                try:
                    req = Requirement.create(project_id=POLARION_PRODUCT, title=bug_title, desc=desc, **named_parms)
                    break
                except Exception as inst:
                    print inst
                    i+=1
                    time.sleep(10)



            req.add_hyperlink(link.uri, link.role)
            req.status = "approved"
            req.update()

            #Get requirement ID and update bugzilla extrenal link tracker
            bz_connection.add_external_tracker(str(bz_rfe.id), str(req.work_item_id), ext_type_description="Polarion Requirement")
            req_ids.append(req.work_item_id)

        print "%s - end bug: %s - %s" % (datetime.datetime.now(), req.work_item_id, link.uri)


    plan.add_plan_items(req_ids)


if __name__ == "__main__":

    bz_rfes, bz_connection = get_rfes_from_bugzilla()
    print "Number of RFEs in " + BUGZILLA_VERSION + ": %s" %bz_rfes.__len__()
    create_requirements(bz_rfes, bz_connection)


