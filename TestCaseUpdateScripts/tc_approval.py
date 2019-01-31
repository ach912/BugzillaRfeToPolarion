# coding=utf-8
import datetime

import sys
from pylarion.test_run import TestRun
from pylarion.test_record import TestRecord
from pylarion.work_item import TestCase, Requirement
from pylarion.document import Document
from pylarion.text import Text
import unicodedata


# id:(RHELOpenStackPlatform/RHELOSP-32630 RHELOpenStackPlatform/RHELOSP-32628 RHELOpenStackPlatform/RHELOSP-32626 RHELOpenStackPlatform/RHELOSP-32624 RHELOpenStackPlatform/RHELOSP-32622 RHELOpenStackPlatform/RHELOSP-32616 RHELOpenStackPlatform/RHELOSP-29359 RHELOpenStackPlatform/RHELOSP-29358 RHELOpenStackPlatform/RHELOSP-29356 RHELOpenStackPlatform/RHELOSP-28167 RHELOpenStackPlatform/RHELOSP-28137 RHELOpenStackPlatform/RHELOSP-27970 RHELOpenStackPlatform/RHELOSP-27969 RHELOpenStackPlatform/RHELOSP-27968 RHELOpenStackPlatform/RHELOSP-27953 RHELOpenStackPlatform/RHELOSP-27952 RHELOpenStackPlatform/RHELOSP-27951 RHELOpenStackPlatform/RHELOSP-27930 RHELOpenStackPlatform/RHELOSP-27927 RHELOpenStackPlatform/RHELOSP-27926 RHELOpenStackPlatform/RHELOSP-27925 RHELOpenStackPlatform/RHELOSP-27924 RHELOpenStackPlatform/RHELOSP-27923 RHELOpenStackPlatform/RHELOSP-27922 RHELOpenStackPlatform/RHELOSP-27921 RHELOpenStackPlatform/RHELOSP-27919 RHELOpenStackPlatform/RHELOSP-27918 RHELOpenStackPlatform/RHELOSP-27917 RHELOpenStackPlatform/RHELOSP-27916 RHELOpenStackPlatform/RHELOSP-27915 RHELOpenStackPlatform/RHELOSP-27914 RHELOpenStackPlatform/RHELOSP-27913 RHELOpenStackPlatform/RHELOSP-27912 RHELOpenStackPlatform/RHELOSP-27911 RHELOpenStackPlatform/RHELOSP-27910 RHELOpenStackPlatform/RHELOSP-27909 RHELOpenStackPlatform/RHELOSP-27908 RHELOpenStackPlatform/RHELOSP-27907 RHELOpenStackPlatform/RHELOSP-27906 RHELOpenStackPlatform/RHELOSP-27905 RHELOpenStackPlatform/RHELOSP-27904 RHELOpenStackPlatform/RHELOSP-27901 RHELOpenStackPlatform/RHELOSP-27899 RHELOpenStackPlatform/RHELOSP-27896 RHELOpenStackPlatform/RHELOSP-27895 RHELOpenStackPlatform/RHELOSP-27893 RHELOpenStackPlatform/RHELOSP-27891 RHELOpenStackPlatform/RHELOSP-27882 RHELOpenStackPlatform/RHELOSP-27881 RHELOpenStackPlatform/RHELOSP-27880 RHELOpenStackPlatform/RHELOSP-27879 RHELOpenStackPlatform/RHELOSP-27878 RHELOpenStackPlatform/RHELOSP-27859 RHELOpenStackPlatform/RHELOSP-27858 RHELOpenStackPlatform/RHELOSP-27856 RHELOpenStackPlatform/RHELOSP-27852 RHELOpenStackPlatform/RHELOSP-27835 RHELOpenStackPlatform/RHELOSP-27834 RHELOpenStackPlatform/RHELOSP-27833 RHELOpenStackPlatform/RHELOSP-27831 RHELOpenStackPlatform/RHELOSP-27830 RHELOpenStackPlatform/RHELOSP-27829 RHELOpenStackPlatform/RHELOSP-27828 RHELOpenStackPlatform/RHELOSP-27827 RHELOpenStackPlatform/RHELOSP-27825 RHELOpenStackPlatform/RHELOSP-27824 RHELOpenStackPlatform/RHELOSP-27820 RHELOpenStackPlatform/RHELOSP-27819 RHELOpenStackPlatform/RHELOSP-27818 RHELOpenStackPlatform/RHELOSP-27817 RHELOpenStackPlatform/RHELOSP-27811 RHELOpenStackPlatform/RHELOSP-27810 RHELOpenStackPlatform/RHELOSP-27809 RHELOpenStackPlatform/RHELOSP-27807 RHELOpenStackPlatform/RHELOSP-27798 RHELOpenStackPlatform/RHELOSP-27784 RHELOpenStackPlatform/RHELOSP-27701 RHELOpenStackPlatform/RHELOSP-27396 RHELOpenStackPlatform/RHELOSP-27073 RHELOpenStackPlatform/RHELOSP-27072 RHELOpenStackPlatform/RHELOSP-27071 RHELOpenStackPlatform/RHELOSP-27070 RHELOpenStackPlatform/RHELOSP-27045 RHELOpenStackPlatform/RHELOSP-27044 RHELOpenStackPlatform/RHELOSP-27038 RHELOpenStackPlatform/RHELOSP-27037 RHELOpenStackPlatform/RHELOSP-27035 RHELOpenStackPlatform/RHELOSP-27033 RHELOpenStackPlatform/RHELOSP-27028 RHELOpenStackPlatform/RHELOSP-26981 RHELOpenStackPlatform/RHELOSP-26980 RHELOpenStackPlatform/RHELOSP-26979 RHELOpenStackPlatform/RHELOSP-26978 RHELOpenStackPlatform/RHELOSP-26977 RHELOpenStackPlatform/RHELOSP-26976 RHELOpenStackPlatform/RHELOSP-26975 RHELOpenStackPlatform/RHELOSP-26974 RHELOpenStackPlatform/RHELOSP-26973 RHELOpenStackPlatform/RHELOSP-26972 RHELOpenStackPlatform/RHELOSP-26967 RHELOpenStackPlatform/RHELOSP-26966 RHELOpenStackPlatform/RHELOSP-26965 RHELOpenStackPlatform/RHELOSP-26962 RHELOpenStackPlatform/RHELOSP-26961 RHELOpenStackPlatform/RHELOSP-26960 RHELOpenStackPlatform/RHELOSP-26959 RHELOpenStackPlatform/RHELOSP-26958 RHELOpenStackPlatform/RHELOSP-26957 RHELOpenStackPlatform/RHELOSP-26881 RHELOpenStackPlatform/RHELOSP-26431 RHELOpenStackPlatform/RHELOSP-26430 RHELOpenStackPlatform/RHELOSP-26429 RHELOpenStackPlatform/RHELOSP-26290 RHELOpenStackPlatform/RHELOSP-26288 RHELOpenStackPlatform/RHELOSP-26283 RHELOpenStackPlatform/RHELOSP-26281 RHELOpenStackPlatform/RHELOSP-26279 RHELOpenStackPlatform/RHELOSP-26277 RHELOpenStackPlatform/RHELOSP-26275 RHELOpenStackPlatform/RHELOSP-26092 RHELOpenStackPlatform/RHELOSP-26091 RHELOpenStackPlatform/RHELOSP-26090 RHELOpenStackPlatform/RHELOSP-26088 RHELOpenStackPlatform/RHELOSP-26087 RHELOpenStackPlatform/RHELOSP-26086 RHELOpenStackPlatform/RHELOSP-26084 RHELOpenStackPlatform/RHELOSP-26083 RHELOpenStackPlatform/RHELOSP-26082 RHELOpenStackPlatform/RHELOSP-26081 RHELOpenStackPlatform/RHELOSP-26073 RHELOpenStackPlatform/RHELOSP-26071 RHELOpenStackPlatform/RHELOSP-26070 RHELOpenStackPlatform/RHELOSP-26069 RHELOpenStackPlatform/RHELOSP-26068 RHELOpenStackPlatform/RHELOSP-26063 RHELOpenStackPlatform/RHELOSP-26061 RHELOpenStackPlatform/RHELOSP-25152 RHELOpenStackPlatform/RHELOSP-25149 RHELOpenStackPlatform/RHELOSP-25148 RHELOpenStackPlatform/RHELOSP-24647)
#items = TestCase.query('project.id:RHELOpenStackPlatform')

# items = TestCase.query('NOT status:approved AND id:(RHELOpenStackPlatform/RHELOSP-32630 RHELOpenStackPlatform/RHELOSP-32628 RHELOpenStackPlatform/RHELOSP-32626 RHELOpenStackPlatform/RHELOSP-32624 RHELOpenStackPlatform/RHELOSP-32622 RHELOpenStackPlatform/RHELOSP-32616 RHELOpenStackPlatform/RHELOSP-29359 RHELOpenStackPlatform/RHELOSP-29358 RHELOpenStackPlatform/RHELOSP-29356 RHELOpenStackPlatform/RHELOSP-28167 RHELOpenStackPlatform/RHELOSP-28137 RHELOpenStackPlatform/RHELOSP-27970 RHELOpenStackPlatform/RHELOSP-27969 RHELOpenStackPlatform/RHELOSP-27968 RHELOpenStackPlatform/RHELOSP-27953 RHELOpenStackPlatform/RHELOSP-27952 RHELOpenStackPlatform/RHELOSP-27951 RHELOpenStackPlatform/RHELOSP-27930 RHELOpenStackPlatform/RHELOSP-27927 RHELOpenStackPlatform/RHELOSP-27926 RHELOpenStackPlatform/RHELOSP-27925 RHELOpenStackPlatform/RHELOSP-27924 RHELOpenStackPlatform/RHELOSP-27923 RHELOpenStackPlatform/RHELOSP-27922 RHELOpenStackPlatform/RHELOSP-27921 RHELOpenStackPlatform/RHELOSP-27919 RHELOpenStackPlatform/RHELOSP-27918 RHELOpenStackPlatform/RHELOSP-27917 RHELOpenStackPlatform/RHELOSP-27916 RHELOpenStackPlatform/RHELOSP-27915 RHELOpenStackPlatform/RHELOSP-27914 RHELOpenStackPlatform/RHELOSP-27913 RHELOpenStackPlatform/RHELOSP-27912 RHELOpenStackPlatform/RHELOSP-27911 RHELOpenStackPlatform/RHELOSP-27910 RHELOpenStackPlatform/RHELOSP-27909 RHELOpenStackPlatform/RHELOSP-27908 RHELOpenStackPlatform/RHELOSP-27907 RHELOpenStackPlatform/RHELOSP-27906 RHELOpenStackPlatform/RHELOSP-27905 RHELOpenStackPlatform/RHELOSP-27904 RHELOpenStackPlatform/RHELOSP-27901 RHELOpenStackPlatform/RHELOSP-27899 RHELOpenStackPlatform/RHELOSP-27896 RHELOpenStackPlatform/RHELOSP-27895 RHELOpenStackPlatform/RHELOSP-27893 RHELOpenStackPlatform/RHELOSP-27891 RHELOpenStackPlatform/RHELOSP-27882 RHELOpenStackPlatform/RHELOSP-27881 RHELOpenStackPlatform/RHELOSP-27880 RHELOpenStackPlatform/RHELOSP-27879 RHELOpenStackPlatform/RHELOSP-27878 RHELOpenStackPlatform/RHELOSP-27859 RHELOpenStackPlatform/RHELOSP-27858 RHELOpenStackPlatform/RHELOSP-27856 RHELOpenStackPlatform/RHELOSP-27852 RHELOpenStackPlatform/RHELOSP-27835 RHELOpenStackPlatform/RHELOSP-27834 RHELOpenStackPlatform/RHELOSP-27833 RHELOpenStackPlatform/RHELOSP-27831 RHELOpenStackPlatform/RHELOSP-27830 RHELOpenStackPlatform/RHELOSP-27829 RHELOpenStackPlatform/RHELOSP-27828 RHELOpenStackPlatform/RHELOSP-27827 RHELOpenStackPlatform/RHELOSP-27825 RHELOpenStackPlatform/RHELOSP-27824 RHELOpenStackPlatform/RHELOSP-27820 RHELOpenStackPlatform/RHELOSP-27819 RHELOpenStackPlatform/RHELOSP-27818 RHELOpenStackPlatform/RHELOSP-27817 RHELOpenStackPlatform/RHELOSP-27811 RHELOpenStackPlatform/RHELOSP-27810 RHELOpenStackPlatform/RHELOSP-27809 RHELOpenStackPlatform/RHELOSP-27807 RHELOpenStackPlatform/RHELOSP-27798 RHELOpenStackPlatform/RHELOSP-27784 RHELOpenStackPlatform/RHELOSP-27701 RHELOpenStackPlatform/RHELOSP-27396 RHELOpenStackPlatform/RHELOSP-27073 RHELOpenStackPlatform/RHELOSP-27072 RHELOpenStackPlatform/RHELOSP-27071 RHELOpenStackPlatform/RHELOSP-27070 RHELOpenStackPlatform/RHELOSP-27045 RHELOpenStackPlatform/RHELOSP-27044 RHELOpenStackPlatform/RHELOSP-27038 RHELOpenStackPlatform/RHELOSP-27037 RHELOpenStackPlatform/RHELOSP-27035 RHELOpenStackPlatform/RHELOSP-27033 RHELOpenStackPlatform/RHELOSP-27028 RHELOpenStackPlatform/RHELOSP-26981 RHELOpenStackPlatform/RHELOSP-26980 RHELOpenStackPlatform/RHELOSP-26979 RHELOpenStackPlatform/RHELOSP-26978 RHELOpenStackPlatform/RHELOSP-26977 RHELOpenStackPlatform/RHELOSP-26976 RHELOpenStackPlatform/RHELOSP-26975 RHELOpenStackPlatform/RHELOSP-26974 RHELOpenStackPlatform/RHELOSP-26973 RHELOpenStackPlatform/RHELOSP-26972 RHELOpenStackPlatform/RHELOSP-26967 RHELOpenStackPlatform/RHELOSP-26966 RHELOpenStackPlatform/RHELOSP-26965 RHELOpenStackPlatform/RHELOSP-26962 RHELOpenStackPlatform/RHELOSP-26961 RHELOpenStackPlatform/RHELOSP-26960 RHELOpenStackPlatform/RHELOSP-26959 RHELOpenStackPlatform/RHELOSP-26958 RHELOpenStackPlatform/RHELOSP-26957 RHELOpenStackPlatform/RHELOSP-26881 RHELOpenStackPlatform/RHELOSP-26431 RHELOpenStackPlatform/RHELOSP-26430 RHELOpenStackPlatform/RHELOSP-26429 RHELOpenStackPlatform/RHELOSP-26290 RHELOpenStackPlatform/RHELOSP-26288 RHELOpenStackPlatform/RHELOSP-26283 RHELOpenStackPlatform/RHELOSP-26281 RHELOpenStackPlatform/RHELOSP-26279 RHELOpenStackPlatform/RHELOSP-26277 RHELOpenStackPlatform/RHELOSP-26275 RHELOpenStackPlatform/RHELOSP-26092 RHELOpenStackPlatform/RHELOSP-26091 RHELOpenStackPlatform/RHELOSP-26090 RHELOpenStackPlatform/RHELOSP-26088 RHELOpenStackPlatform/RHELOSP-26087 RHELOpenStackPlatform/RHELOSP-26086 RHELOpenStackPlatform/RHELOSP-26084 RHELOpenStackPlatform/RHELOSP-26083 RHELOpenStackPlatform/RHELOSP-26082 RHELOpenStackPlatform/RHELOSP-26081 RHELOpenStackPlatform/RHELOSP-26073 RHELOpenStackPlatform/RHELOSP-26071 RHELOpenStackPlatform/RHELOSP-26070 RHELOpenStackPlatform/RHELOSP-26069 RHELOpenStackPlatform/RHELOSP-26068 RHELOpenStackPlatform/RHELOSP-26063 RHELOpenStackPlatform/RHELOSP-26061 RHELOpenStackPlatform/RHELOSP-25152 RHELOpenStackPlatform/RHELOSP-25149 RHELOpenStackPlatform/RHELOSP-25148 RHELOpenStackPlatform/RHELOSP-24647)')
# query=caseimportance.KEY%3Acritical%20AND%20NOT%20status%3A(approved%20inactive)%20AND%20caseautomation.KEY%3Aautomated
items = TestCase.query("status:needsupdate")

print "Number of items %s" % len(items)

for item in items:
	# try:
	print item.uri
	tc = TestCase(uri=item.uri)
	print tc.title

	# if tc.description:
	# 	tc.description = tc._check_encode(tc.description)
	# else:

	# tc.description = "TBD"
	# tc.description.decode('utf-8')


	# tc.automation_script = "https://rhos-qe-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/"
	# auto_test_id = tc.get_custom_field('automation-test-id').value
	# tc.automation_script = auto_test_id
	try:
		# tc.add_approvee('achernet')
		# tc.edit_approval('achernet','approved')
		# if tc.customerscenario == False:
		tc.status = 'proposed'
		# tc.automation_script =  tc._check_encode(tc.automation_script)
		# tc.customerscenario = True
		tc.update()
	except StandardError:
		print 'Why, like this?'
		print "Unexpected error:", sys.exc_info()[0]
	# except:
	# 	print "Unexpected error:", sys.exc_info()[0]




	#tc.status="approved"

	# tc.get_custom_field('automation-test-id').value = tc._check_encode(tc.get_custom_field('automation-test-id').value)
	# auto_test_id = tc.get_custom_field('automation-test-id').value

	# print auto_test_id
	# print tc.automation_script
	# if tc.description:
	# tc.description = tc._check_encode(tc.description)
	 # tc.automation_script = tc._check_encode(tc.automation_script)
	# tc.automation_script = auto_test_id
	# print tc.automation_script