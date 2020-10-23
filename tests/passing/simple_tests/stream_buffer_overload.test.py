Test.Summary = "Test the output by overloading the stream buffers"

Test.Setup.Copy("../testers/dump_text.py")

t = Test.AddTestRun()
t.Command = 'python dump_text.py'
t.ReturnCode = 0
t.Processes.Default.Streams.All = Testers.ContainsExpression("end", "we should see end after 100k prints")
