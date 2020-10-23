Test.Summary = "Test the All/Any containers"

Test.ContinueOnFail = True

t = Test.AddTestRun("Any")
t.Command = 'echo "Hello World"'
t.Streams.All = Any("gold/hello.gold", "gold/multiline.gold")
t.ReturnCode = 0

t = Test.AddTestRun("All")
t.Command = 'echo "Hello World"'
t.Streams.All = All("gold/hello.gold", "gold/multiline.gold")
t.ReturnCode = 0
