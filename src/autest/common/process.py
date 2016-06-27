'''
Module overrides Popen and introduces killtree function
'''

from __future__ import absolute_import, division, print_function

import subprocess
import os
import signal

import ctypes
import time

if os.name == 'nt':
    from . import win32
    def killtree( self ):
        '''
        Kills a process with all its children
        '''
        print("kill....")
        os.kill(self.pid, signal.CTRL_C_EVENT ) 
        time.sleep(15)
        print("finished")
        win32.TerminateJobObject(self._job, -1) #pylint: disable=protected-access

    def waitTimeOut(process, timeout):
        # WaitForSingleObject expects timeout in milliseconds, so we convert it
        win32.WaitForSingleObject(int_to_handle(process._handle), int(timeout * 1000))
        return (process.poll() is None)

    def int_to_handle( value ):
        '''
        Casts Python integer to ctypes.wintypes.HANDLE
        '''
        return ctypes.cast(ctypes.pointer(ctypes.c_size_t(value)),
            ctypes.POINTER(ctypes.wintypes.HANDLE)).contents

    def Popen( *args, **kw ): #pylint: disable=invalid-name
        '''
        Keep args description in the comment for reference:
        args, bufsize=None, stdin=None, stdout=None, stderr=None,
        preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None,
        universal_newlines=None, startupinfo=None, creationflags=None, **kw
        '''

        job = win32.CreateJobObject(None, "")
        extended_info = win32.JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        if not win32.QueryInformationJobObject(job,
                win32.JobObjectExtendedLimitInformation,
                ctypes.byref(extended_info),
                ctypes.sizeof(win32.JOBOBJECT_EXTENDED_LIMIT_INFORMATION),
                None):
            raise ctypes.WinError()
        extended_info.BasicLimitInformation.LimitFlags = (win32.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE)
        if not win32.SetInformationJobObject(job,
                win32.JobObjectExtendedLimitInformation,
                ctypes.byref(extended_info),
                ctypes.sizeof(win32.JOBOBJECT_EXTENDED_LIMIT_INFORMATION)):
            raise ctypes.WinError()

        # this is to deal with anything new
        args = list(args)
        kw = dict(kw)
        kw['creationflags']=kw.get('creationflags',0)|subprocess.CREATE_NEW_PROCESS_GROUP
        # In the case of windows we want to make a job object for the given
        # process
        # on windows we want to start the process suspended so we can apply job
        # object correctly
        # I have to yet to do this....  so there is a small race that can
        # happen
        process = subprocess.Popen(*args, **kw)

        #pylint: disable=protected-access,no-member
        win32.AssignProcessToJobObject(job, int_to_handle(process._handle))
        process._job = job  #pylint: disable=protected-access
        return process
else:
    def killtree( self ):
        '''
        Terminates a process and all its children
        '''
        #pylint: disable=no-member
        # try to kill group with a ctrl-C
        pgid=os.getpgid(self.pid)
        os.killpg(pgid, signal.SIGINT)
        time.sleep(1)
        try:
            os.killpg(pgid, signal.SIGKILL)
        except OSError as e:
            #If this a 3 (no such process) error we ignore it
            if e.errno != 3:
                raise

    
    def waitTimeOut(process, timeout):
        startTime = time.time()
        endTime = startTime + timeout
        while (time.time() < endTime) and (process.poll() is None):
            #This sleep the thread it is called in
            time.sleep(0.1)
        return (process.poll() is None)

    #pylint: disable=invalid-name
    def Popen( *args, **kw ):
        '''
        Wraps subprocess.Popen
        '''
        # this is to deal with anything new
        args = list(args)
        kw = dict(kw)
        if 'preexec_fn' in kw:
            preexec_fn = kw['preexec_fn']
            def wrapper( *lst, **kw ):
                '''
                Calls setsid before preexec_fn
                '''
                os.setsid() #pylint: disable=no-member
                return preexec_fn(*lst, **kw)
            kw['preexec_fn'] = wrapper
        else:
            kw['preexec_fn'] = os.setsid #pylint: disable=no-member
        return subprocess.Popen(*args, **kw)

# add killtree function
subprocess.Popen.killtree = killtree
subprocess.Popen.waitTimeOut = waitTimeOut

