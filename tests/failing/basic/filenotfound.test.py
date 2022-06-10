Test.Summary="Test that we error when file is not found"

# boring test to do nothing
t=Test.AddTestRun("setup")
t.Command="python --version > version.txt"
t.ReturnCode=0
# test that this fails because it should exist ( bug in old code where the test nevered happened )
t.Disk.File("version.txt", exists=False, id="logfile")