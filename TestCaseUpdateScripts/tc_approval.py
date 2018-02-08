# coding=utf-8
import datetime
from pylarion.test_run import TestRun
from pylarion.test_record import TestRecord
from pylarion.work_item import TestCase, Requirement
from pylarion.document import Document



#items = TestCase.query('project.id:RHELOpenStackPlatform')

items = TestCase.query('casecomponent.KEY:Heat AND author.id:(augol rrasouli tshefi)')


print "Number of items %s" % len(items)

for item in items:
	print item.uri
	tc = TestCase(uri=item.uri)
	print tc.title
	tc.status="inactive"
	tc.update()


# items = TestCase.query('status:needsupdate')
# items = TestCase.query("status:(proposed) AND updated:[20130101 TO 20161201]")
# items = TestCase.query("status:(draft proposed ) AND created:[20130101 TO 20161201]")
# items = TestCase.query(“status:approved AND NOT HAS_VALUE:description”)
# items = TestCase.query(status:approved AND caselevel.KEY:component”)
