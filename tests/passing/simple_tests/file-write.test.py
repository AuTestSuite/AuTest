# The finding of this test shows we find .test.py

Test.Summary = "Test the existance, size and content of a file"

t = Test.AddTestRun("stdout")

t.Disk.File("hello.txt", exists=True, id="logfile")
t.Disk.logfile.Content = "gold/hello.gold"
t.Disk.logfile.WriteOn('''Hello 
''')
t.Disk.File("sub/hello.txt", exists=True, id="logfile")
t.Disk.logfile.Content = "gold/hello.gold"
t.Disk.logfile.WriteOn('''Hello 
''')
t.Command = 'echo Hello'
