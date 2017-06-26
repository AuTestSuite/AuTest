test.Summary="Test the setup of Setup Copy logic"


Setup.Copy.FromDirectory("data")
Setup.Copy("data","data")

t=Test.AddTestRun("Test file existance")
t.Command='echo "do nothing"'
t.ReturnCode=9
t.Disk.Directory("data",exists=True)
t.Disk.Directory("sub1").Exists=True


