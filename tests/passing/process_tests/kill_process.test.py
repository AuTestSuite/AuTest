Test.Summary = '''
Test Running of two processes own by test and killing one of them as part of a set of test runs
This shows a hack/workaround until we get some better logic in to handle this in a more ideal way
'''

def SetPid(event):
    Test.Env['SERVERPID'] = str(event.object.pid())

Setup.Copy("app.py", "fakecurl")
Setup.Copy("app.py", "server1")

# pretent we have two server with a relationship
parent_server = Test.Processes.Process("parent", "python server1 100")
parent_server.RunningEvent.Connect(SetPid)
child_server = Test.Processes.Process("child", "python server1 100")


tr = Test.AddTestRun("Send request")
tr.Processes.Default.Command = "python fakecurl 2"
tr.Processes.Default.ReturnCode = 0
tr.Processes.Default.StartBefore(parent_server)
tr.Processes.Default.StartBefore(child_server)
tr.StillRunningAfter = child_server
tr.StillRunningAfter = parent_server


tr = Test.AddTestRun("Kill Server")
# need some process to allow the running event to go off
if Condition.IsPlatform('win32'):
    tr.Processes.Default.Command = 'taskkill -F -PID ${SERVERPID}'
else:
    tr.Processes.Default.Command = 'kill -9 ${SERVERPID}'

tr.Processes.Default.ReturnCode = 0

tr = Test.AddTestRun("Send request2")
tr.Processes.Default.Command = "python fakecurl 2"
tr.Processes.Default.ReturnCode = 0
tr.StillRunningBefore = child_server
tr.NotRunningBefore = parent_server
tr.NotRunningAfter = parent_server
