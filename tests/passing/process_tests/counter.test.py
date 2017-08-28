Test.Summary = "Test the example counter When function generator with custom state, use the flag '--debug counter' in autest command to see it counting"


tr = Test.AddTestRun()
tr.Processes.Process(
    "server", "python app 1", returncode=None)
tr.Command = "echo huzzah"
tr.ReturnCode = 0
tr.Processes.Default.StartBefore(
    tr.Processes.server, ready=When.Counter(5))
