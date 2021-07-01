from looper import Looper
import subprocess
from git import Repo, cmd
from datetime import datetime
import os


class GitLogic(Looper):
    """This class is the main class of the GitUploader program that updates
    the selected program from Github to the local git script.

    Attributes:
        DELAY               Sets how many time of delay should pass between loops (seconds, minutes, hours, days)
        REMOTE_REPO         Name of the remote Github project
        BRANCH              Branch where the program should listen to update
        LOCAL_REPO          Path to the local git project
        COMMANDS_BEFORE     Commands the system will do BEFORE the project do the git pull from origin
        COMMANDS_AFTER      Commands the system will do AFTER the project do the git pull from origin
    """

    def __init__(self, delay = '', remote_repo = '', branch = '', local_repo = '', cmd_before = '', cmd_after = '') -> None:
        self.DELAY = delay if delay != '' else (10, 0, 0, 0) # (seconds, minutes, hours, days)
        self.REMOTE_REPO = remote_repo if remote_repo != '' else 'https://github.com/example/repo.git'
        self.BRANCH = branch if branch != '' else 'main'
        self.LOCAL_REPO = local_repo if local_repo != '' else '/path/to/repo.git'
        self.COMMANDS_BEFORE = cmd_before if cmd_before != '' else ['echo commands before']
        self.COMMANDS_AFTER = cmd_after if cmd_after != '' else ['echo commands after']
        super().__init__(self.DELAY)

    @staticmethod
    def test_remote_repo(remote_repo, branch):
        repo = Repo.clone_from(remote_repo, f'/tmp/temporal/')
        try:
            assert 'origin/{}'.format(branch) in repo.references, "The remote repo don't own a branch called '{}'".format(branch)
        except:
            raise AssertionError("The remote repo don't own a branch called '{}'".format(branch))
        finally:
            for root, dirs, files in os.walk(f'/tmp/temporal/', topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(os.path.join(f'/tmp/temporal/'))
    
    @staticmethod
    def test_local_repo(local_repo):
        Repo(local_repo)

    @staticmethod
    def clone_remote(remote, path):
        repo = Repo.clone_from(remote, path+'/')
        

    def get_local_commit(self):
        repo = Repo(self.LOCAL_REPO)
        return repo.head.commit.hexsha

    def get_remote_commit(self):
        remote_refs = {}
        g = cmd.Git()
        for ref in g.ls_remote(self.REMOTE_REPO).split('\n'):
            hash_ref_list = ref.split('\t')
            remote_refs[hash_ref_list[1]] = hash_ref_list[0]
        return str(remote_refs['HEAD'])

    def git_pull(self):
        repo = Repo(self.LOCAL_REPO)
        origin = repo.remote()
        origin.pull()

    def execute(self, commands):
        try:
            for cmd in commands:
                ret = subprocess.run(cmd.split())
                ret.check_returncode()
        except Exception as e:
            print(e)

    def get_now(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def init(self) -> None:
        print('Start: {}'.format(self.get_now()))

    def loop(self) -> None:
        actual_commit = self.get_local_commit()
        remote_commit = self.get_remote_commit()
        
        if actual_commit != remote_commit:
            print('Updating repo: {}'.format(self.get_now()))
            self.execute(self.COMMANDS_BEFORE)
            self.git_pull()
            self.execute(self.COMMANDS_AFTER)
            print('Updated repo!')
