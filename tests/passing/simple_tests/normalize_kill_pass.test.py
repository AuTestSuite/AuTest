Test.Summary = "Tests normalizing SIGKILL return code"


def StopProcess(event, time):
    if event.TotalRunTime > time:
        event.object.Stop()
    return 0, "stop process", "The process will be killed"


Setup.Copy('../testers/normalizeKillTest.py')

Test.Variables.Autest.NormalizeKill = 5

tr = Test.AddTestRun()
tr.Processes.Default.Command = 'python normalizeKillTest.py'
tr.Processes.Default.ReturnCode = 5
tr.RunningEvent.Connect(Testers.Lambda(lambda ev: StopProcess(ev, 2)))
