test.Summary = "Test the setup of Setup Copy logic"


Setup.Copy.FromDirectory("data")
Setup.Copy("data", "data")
Setup.Copy("data", "data2")
Setup.CopyAs("data/a.txt", name="a1.txt")
Setup.CopyAs("data/a.txt", "sub", "a.txt")

t = Test.AddTestRun("Test file existence")
t.Command = 'echo "do nothing"'

t.Disk.File("a1.txt", exists=True)
t.Disk.File("sub/a.txt", exists=True)

t.Disk.Directory("data", exists=True)
t.Disk.Directory("data2", exists=True)
t.Disk.Directory("sub1").Exists = True
