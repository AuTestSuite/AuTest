Test.Summary = "Test --env cli arguments"

# Env for Test object scope
Test.Env['MYLISTVALUE'] = "A:B"

Setup.Copy.FromDirectory('../../nested/cli/')

t = Test.AddTestRun("Testing --env passing")
t.Processes.Default.Command = 'autest -f env-co2 --env MYVALUE=testvalue MYLISTVALUE=$MYLISTVALUE:c'
t.Processes.Default.Streams.All = "gold/passing-co.gold"
t.ReturnCode = 0
