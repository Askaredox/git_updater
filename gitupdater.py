import click
import os
from git.exc import InvalidGitRepositoryError, NoSuchPathError
from gitlogic import GitLogic
from pathlib import Path

OPTIONS = {
    'delay': (0, 10, 0, 0),
    'remote_repo': 'https://github.com/example/repo.git',
    'remote_branch': 'main',
    'local_repo': '.',
    'commands_before': [
        'echo commands before',
    ],
    'commands_after': [
        'echo commands after',
    ],
}

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo('')
    click.echo('Version: 0.1.0')
    ctx.exit()

def get_delay(delay:str):
    delay_str_list = delay.replace(' ', '').split(',')
    assert len(delay_str_list) == 4 ,'Delay time not set correctly should have 4 numbers separated by comas'
    
    num_list = []
    for string in delay_str_list:
        assert string.isnumeric(), 'All entries should be integer numbers'
        num_list.append(int(string))
    
    global OPTIONS
    OPTIONS['delay'] = tuple(num_list)

def get_remote_repo(remote_repo:str, remote_branch:str):
    GitLogic.test_remote_repo(remote_repo, remote_branch)
    global OPTIONS
    OPTIONS['remote_repo'] = remote_repo

def get_local_repo(local_repo:str, remote_repo:str):
    global OPTIONS
    try:
        path_local_repo = os.path.abspath(local_repo)
        GitLogic.test_local_repo(path_local_repo)
    except InvalidGitRepositoryError:
        path_local_repo = os.path.abspath(local_repo)
        if click.confirm('The directory dont have any local repo, do you want to clone the remote repo in "{}"?'.format(path_local_repo)):
            
            GitLogic.clone_remote(remote_repo, path_local_repo)
            OPTIONS['local_repo'] = path_local_repo
    except NoSuchPathError:
        path_local_repo = os.path.abspath(local_repo)
        if click.confirm('The directory dont exists, do you want to clone the remote repo in "{}"?'.format(path_local_repo)):
            Path(path_local_repo).mkdir(parents=True, exist_ok=True)
            GitLogic.clone_remote(remote_repo, path_local_repo)
            OPTIONS['local_repo'] = path_local_repo
        
    OPTIONS['local_repo'] = path_local_repo


@click.group()
@click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True, help='Get version of the program.')
def main():
    """Program to automaticaly update from github"""
    pass


@click.command()
def start():
    delay = click.prompt('Please enter the time between each check to the remote repo (seconds,minutes,hours,days)',
                         default='{}'.format(str(OPTIONS['delay'])[1:-1]), type=str)
    get_delay(delay)
    remote_repo = click.prompt('Please enter the address of the remote repo',
                               default='{}'.format(str(OPTIONS['remote_repo'])), type=str)
    
    remote_branch = click.prompt('Please enter the name of the branch to check', 
                                 default='{}'.format(str(OPTIONS['remote_branch'])), type=str)
    get_remote_repo(remote_repo, remote_branch)
    local_repo = click.prompt('Please enter the path to the local repo directory',
                              default='{}'.format(str(OPTIONS['local_repo'])), type=str)
    get_local_repo(local_repo, remote_repo)

    
    GitLogic(OPTIONS['delay'],OPTIONS['remote_repo'],OPTIONS['remote_branch'],OPTIONS['local_repo'],OPTIONS['commands_before'],OPTIONS['commands_after'])
    



main.add_command(start)
if __name__ == "__main__":
    main()
