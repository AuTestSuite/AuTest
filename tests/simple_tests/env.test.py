test.Summary="Test that the enviroment logic works"

Test.Env={'a':'a','b':'b','c':'c'}

t=Test.AddTestRun("Test file existance")
t.Env['a']="testrun"
t.Env['a1']="testrun1"

if Condition.IsPlatform('win32'):
    t.Processes.Default.Command='echo %a% %a1% %b% %b1% %c%'
else:
    t.Processes.Default.Command='echo $a $a1 $b $b1 $c'

t.Processes.Default.Streams.stdout="gold/env.gold"
t.Processes.Default.Env['b']="process"
t.Processes.Default.Env['b1']="process1"