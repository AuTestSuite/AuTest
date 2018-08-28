Test.Summary="Test the All/Any containers"

Test.ContinueOnFail = True

t=Test.AddTestRun("Any Both True")
t.Command='echo "Hello"'
t.Streams.All = Any("gold/hello1.gold", "gold/hello2.gold")
t.ReturnCode=0

t=Test.AddTestRun("Any One True")
t.Command='echo "Hello"'
t.Streams.All = Any("gold/gold_file_dir_exist.gold", "gold/hello1.gold")
t.ReturnCode=0

t=Test.AddTestRun("All")
t.Command='echo "Hello"'
t.Streams.All = All("gold/hello1.gold", "gold/hello2.gold")
t.ReturnCode=0
