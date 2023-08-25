import os

from autest.core.setupitem import SetupItem
from autest.exceptions.setuperror import SetupError
import autest.api as api

class CreateRepository(SetupItem):
    def __init__(self, name):
        super(CreateRepository, self).__init__(itemname="CreateRepository")
        self._name = name
        self.Description = f"Create git repository {self._name}"

    def setup(self):
        repo_path = os.path.abspath(
            os.path.join(self.SandBoxDir, self._name)).replace('\\', '/')
        self.Env['{0}_GIT_PATH'.format(self._name.upper(
        ))] = repo_path

        if os.path.exists(repo_path):
            raise SetupError('Repository at "%s" already exists' % repo_path)

        # create Repo
        cmd_str = 'git init "{0}"'.format(repo_path)
        if self.RunCommand(cmd_str):
            raise SetupError('Setup command "{0}" Failed'.format(cmd_str))

    def cleanup(self):
        pass


class ImportDirectory(SetupItem):
    def __init__(self, name:str, dir_to_add:str, sub_dir:str=''):
        super(ImportDirectory, self).__init__(itemname="ImportDirectory")
        self._name = name
        self._dir_to_add = dir_to_add
        self._sub_dir = sub_dir
        self.Description = f"Import Directory {sub_dir} to git repository {self._name}"

    def setup(self):
        path_to_add = os.path.abspath(
            os.path.join(self.TestFileDir, self._dir_to_add))
        try:
            repo_path = self.Env['{0}_GIT_PATH'.format(self._name.upper())]
        except KeyboardInterrupt:
            raise
        except:
            # error if we don't have a value for this.. meaning they did not
            # create or define a repository
            raise SetupError(
                'git repository "{0}" does not exist for importing'.format(
                    self.ItemName))

        repo_path = os.path.normpath(os.path.join(repo_path , self._sub_dir))
        # add directory to repo
        
        # copy to git repo
        self.Copy(path_to_add, repo_path)

        # add newly copied directory
        cmd_str = f'cd "{os.path.join(self._name, self._sub_dir)}" && git add .'
        if self.RunCommand(cmd_str):
            raise SetupError('Setup command "{0}" Failed'.format(cmd_str))
        
        # commit newly copied directory
        cmd_str = f'cd "{self._name}" && git commit -m "Import dir"'
        if self.RunCommand(cmd_str):
            raise SetupError('Setup command "{0}" Failed'.format(cmd_str))

    def cleanup(self):
        pass


# class CheckOut(autest.setup.SetupTask):
# class DefineRepository(autest.setup.SetupTask):

api.AddSetupItem(CreateRepository, ns="Git")
api.AddSetupItem(ImportDirectory, ns="Git")
