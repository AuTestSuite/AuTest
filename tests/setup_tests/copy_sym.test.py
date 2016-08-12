test.Summary="Test the setup of Setup Copy logic"


Setup.Copy.FromDirectory("data",try_link=True)
Setup.Copy("data","data",try_link=True)

t=Test.AddTestRun("Test file existance")
t.Command='echo "do nothing"'

t.Disk.Directory("data",exists=True)
t.Disk.Directory("sub1").Exists=True

