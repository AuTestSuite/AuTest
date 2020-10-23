Test.Summary = "Delay start logic"


tr = Test.AddTestRun("Create a time")
tr.Processes.Default.Command = 'python -c "import time; print(time.time())"'
time1 = tr.Processes.Default.Streams.All.AbsPath

tr = Test.AddTestRun("Wait 1 second before testing difference")
tr.DelayStart = 1
tr.Processes.Default.Command = 'python diff.py'
tr.Processes.Default.ReturnCode = 0

py = Test.Disk.File("diff.py")
py.WriteOn(
    '''
import sys,time
start=float(open(r'{0}').read())    
end= time.time()
diff = end - start
print(diff)
if (end - start > 1) and (end - start < 2):
    sys.exit(0)
else:
    sys.exit(1)
'''.format(time1)
)
