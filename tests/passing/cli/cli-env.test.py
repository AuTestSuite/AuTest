Test.Summary = "Test --env cli arguments"

# Env for Test object scope
Test.Env['MYLISTVALUE'] = "A:B"

Setup.Copy.FromDirectory('../../nested/cli/')

t = Test.AddTestRun("Testing --env passing")
t.Processes.Default.Command = 'autest -f env --env MYLISTVALUE=$MYLISTVALUE:c MYVALUE=testvalue'
t.Processes.Default.Streams.All = "gold/passing.gold"
t.ReturnCode = 0
