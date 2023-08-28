test.Summary = "Test the setup of git logic"

Test.SkipUnless(
    Condition.HasProgram(
        "git",
        "git needs to be install and on the path"
    )
)

Setup.Git.ImportDirectory("mygit", "data", "test")


t = Test.AddTestRun("git clone")
t.RawCommand = 'git clone "$MYGIT_GIT_PATH" myco'
t.ReturnCode = 0
t.Disk.Directory("myco/test/sub1", exists=True)
t.Disk.File("myco/test/sub1/a.txt").Exists = True
