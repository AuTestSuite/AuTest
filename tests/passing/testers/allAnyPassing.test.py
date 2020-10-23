Test.Summary = "Test the All/Any containers"

Test.ContinueOnFail = True

if Condition.IsPlatform('win32'):
    cmd = 'echo Hello'
else:
    cmd = 'echo "Hello"'

t = Test.AddTestRun("Any Both True")
t.Command = cmd
t.Streams.All = Any("gold/hello1.gold", "gold/hello2.gold")
t.ReturnCode = 0

t = Test.AddTestRun("Any One True")
t.Command = cmd
t.Streams.All = Any("gold/gold_file_dir_exist.gold", "gold/hello1.gold")
t.ReturnCode = 0

t = Test.AddTestRun("All")
t.Command = cmd
t.Streams.All = All("gold/hello1.gold", "gold/hello2.gold")
t.ReturnCode = 0
