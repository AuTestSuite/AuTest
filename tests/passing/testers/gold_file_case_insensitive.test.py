# This test validates correct case-insensitive behavior of Testers.GoldFile.

Test.Summary="Verify GoldFile case_insensitive parameter behavior"
t=Test.AddTestRun("case_insensitive")
if Condition.IsPlatform('win32'):
    t.Command='echo HEllO WOrld'
else:
    t.Command='echo "HEllO WOrld"'
t.Streams.stdout= Testers.GoldFile("gold/hello_lower.gold", case_insensitive=True)
t.ReturnCode=0
