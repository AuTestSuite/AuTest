Test.Summary = "Test the All/Any containers"

Test.ContinueOnFail = True

t = Test.AddTestRun("Any")
if Condition.IsPlatform('win32'):
    t.Command='echo HEllO WOrld'
else:
    t.Command='echo "HEllO WOrld"'
t.Streams.All = Any("gold/hello.gold", "gold/multiline.gold")
t.ReturnCode = 0

t = Test.AddTestRun("All")
if Condition.IsPlatform('win32'):
    t.Command='echo HEllO WOrld'
else:
    t.Command='echo "HEllO WOrld"'
t.Streams.All = All("gold/hello.gold", "gold/multiline.gold")
t.ReturnCode = 0
