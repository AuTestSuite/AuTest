from __future__ import absolute_import, division, print_function
import autest.core.streamwriter as streamwriter
import autest.common.process
import hosts.output as host
import autest.common.disk

import subprocess
import string
import shutil
import os

# base class for any Setup task extension
# contains basic API that maybe useful in defining a given task.


class SetupItem(object):

    def __init__(self, itemname=None, taskname=None):
        if itemname:
            self.__itemname = itemname
        elif taskname:
            self.__itemname = taskname
        else:
            host.WriteError("itemname is not provided")
        self.__test = None
        self.cnt = 0
    # basic properties values we need

    @property
    def ItemName(self):
        # name of the task
        return self.__itemname

    @ItemName.setter
    def ItemName(self, val):
        # name of the task
        self.__itemname = val

    @property
    def SandBoxDir(self):
        # directory we run the test in
        return self.__test.RunDirectory

    @property
    def TestRootDir(self):
        # the directory location given to scan for files for all the tests
        return self.__test.TestRoot

    @property
    def TestFileDir(self):
        # the directory the test file was defined in
        return self.__test.TestDirectory

    # useful util functions
    def RunCommand(self, cmd):
        # TODO.. try to pull the logic out in to some reusable process object
        ###########
        # create a StreamWriter which will write out the stream data of the run
        # to sorted files
        output = streamwriter.StreamWriter(os.path.join(
            self.__test.RunDirectory, "_setup_tmp_{0}_{1}".format(self.ItemName.replace(" ", "_"), self.cnt)), cmd)
        self.cnt += 1
        # the command line we will run. We add the RunDirectory to the start of the command
        # to avoid having to deal with cwddir() issues
        command_line = "cd {0} && {1}".format(self.__test.RunDirectory, cmd)
        # subsitute the value of the string via the template engine
        # as this provide a safe cross platform $subst model.
        template = string.Template(command_line)
        command_line = template.substitute(self.__test.Env)

        proc = autest.common.process.Popen(
            command_line,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.__test.Env)

        # get the output stream from the process we created and redirect to
        # files
        stdout = streamwriter.PipeRedirector(proc.stdout, output.WriteStdOut)
        stderr = streamwriter.PipeRedirector(proc.stderr, output.WriteStdErr)

        proc.wait()

        output.Close()

        # clean up redirectory objects for this run
        stdout.close()
        stderr.close()

        return proc.returncode

    def Copy(self, source, target=None, try_link=False):
        source, target = self._copy_setup(source, target)
        if try_link:
            try:
                self._smartLink(source, target)
                return
            except:
                pass
        host.WriteVerbose("setup", "Copying {0} to {1}".format(source, target))
        if os.path.isfile(source):
            shutil.copy2(source, target)
        else:
            autest.common.disk.copy_tree(source, target)

    def _copy_setup(self, source, target=None):
        # check to see if this is absolute path or not
        if not os.path.isabs(source):
            # if not we assume that the directory is based on our
            # Sandbox directory
            source = os.path.join(self.TestFileDir, source)
        if target:
            if not os.path.isabs(target):
                # this is an error
                pass
            target = os.path.join(self.SandBoxDir, target)
        else:
            # given that target is None we assume that we want to copy it
            # the sandbox directory with the same name as the source
            target = os.path.join(self.SandBoxDir, os.path.basename(source))
        return (source, target)

    def SymLink(self, source, target):
        os.symlink(source,target)

    def HardLink(self, source, target):
        os.link(source,target)

    def _smartLink(self, source, target):
        '''
        Tires to make a Hard link then a SymLink then do a copy
        ToDo: look at making this overidable in what logic is used
        such as hard_copy or soft_copy as some tests might want to
        control how this smart logic is handled
        '''
        if os.path.isfile(source):
            try:
                host.WriteVerbose("setup", "Hardlinking {0} to {1}".format(source, target))
                self.HardLink(source,target)
                return
            except:
                host.WriteVerbose("setup", "Hardlinking - Failed! Trying..")
        if self.SandBoxDir == target:
            files = os.listdir(source)
            for x in files:
                fullsrc = os.path.join(source, x)
                fulldest = os.path.join(target, x)
                self.Copy(fullsrc,fulldest,try_link=True)
        else:
            try:
                host.WriteVerbose("setup", "Symlinking {0} to {1}".format(source, target))
                self.SymLink(source,target)
            except:
                host.WriteVerbose("setup", "Symlinking - Failed! Trying..")
                raise            
            

    def _bind(self, test):
        '''
        Allow us to bind the Test information with the setup item
        This is done before we try to execute the setup logic
        '''
        self.__test = test

    def cleanup(self):
        pass

    @property
    def Env(self):
        return self.__test.Env
