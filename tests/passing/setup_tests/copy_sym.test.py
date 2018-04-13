test.Summary="Test the setup of Setup Copy logic"

# copy

# this makes an empty link on purpose for the test
Setup.Copy("a.txt","a.link.txt",copy_logic=CopyLogic.Soft)

Setup.Copy.FromDirectory("data",copy_logic=CopyLogic.SoftFiles)

Setup.Copy("data","data",copy_logic=CopyLogic.Hard)

t=Test.AddTestRun("Test file existance")
t.Command='echo "do nothing"'


t.Disk.Directory("data",exists=True)
t.Disk.Directory("sub1").Exists=True

