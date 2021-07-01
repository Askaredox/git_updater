# Git Updater

## Steps

### Step 1 (Preparations)

Make sure python3 is installed in your system by checking the version in console:

```bash
python3 --version
```

if its not installed please check this page: https://projects.raspberrypi.org/en/projects/generic-python-install-python3



Make sure pip is installed in your system by checking the version in console:

```bash
pip3 --version
```

if its not installed please check this page: https://pimylifeup.com/ubuntu-install-pip/



### Step 2 (Instalation)

The program is made from 5 files:

- `gitlogic.py` (All the commands needed to make all git commands)
- `gitupdater.py` (The prompt manager and input of information)
- `looper.py` (The loop manager to make the program running)
- `requirements.txt` (All the requirements that are going to be installed)
- `README.md` (This file)

You need to put a directory with this 5 files beside the directory that are going to update like this:

```
directory
|   app_to_update
|	│   all_files
|	└── .git
└── git_uploader
 	|   gitlogic.py
 	|   gitupdater.py
 	|   looper.py
 	|   requirements.txt
 	└── README.md
```

Then let's go to the `git_uploader` directory:

```
~/.../directory/git_uploader$ 
```

and install all requirements:

```
~/.../directory/git_uploader$ pip3 install -r requirements.txt
```



### Step 3 (Configurations)

Then you need to edit the python file `gitupdater.py` in lines 13 and 16

```python
'commands_before': [
    'echo commands before', # this
],
'commands_after': [
     'echo commands after', # and this
],
```

edit this lines to all the commands you use to shutdown the server and to turn up again the server i.e.

```python
'commands_before': [
    'cd /etc/dir/to/server',
    'sudo systemctl shutdown', #only an example, please use the commands you use to start server
],
'commands_after': [
    'cd /etc/dir/to/server',
    'sudo systemctl start', #only an example, please use the commands you use to start server
],
```

**Note**: if you want you can also edit the previous lines to already set the settings i.e.

```python
OPTIONS = {
    'delay': (0, 10, 0, 0), #(seconds, minutes, hours, days)
    'remote_repo': 'https://github.com/example/repo.git', #remote repo https address
    'remote_branch': 'main', #branch to fetch data
    'local_repo': '.', #path to the local repo in the device
    'commands_before': [
        'echo commands before', # commands to do before the repo updates
    ],
    'commands_after': [
        'echo commands after', # commands to do after the repo updates
    ],
}
```



### Step 4 (Running)

Now the program is ready to be executed by running this command:

```bash
~/.../directory/git_uploader$ python3 gitupdater.py start
Please enter the time between each check to the remote repo (seconds,minutes,hours,days) [0, 10, 0, 0]: 0,30,0,0

Please enter the address of the remote repo [https://github.com/example/repo.git]: https://github.com/Askaredox/git_uploader_test.git

Please enter the name of the branch to check [main]: 

Please enter the path to the local repo directory [.]: ../app_to_update

Start: 30/06/2021 11:48:33
```

The program will prompt the next line `Please enter the time between each check to the remote repo` , the above example will be of 0 seconds, 30 minutes, 0 hours, 0 days, which means the program will fetch every 30 minutes for any update in the remote repo.

The program then will ask for the https address of the remote repo use the same address you use in `git clone`.

The program next will ask for the branch to fetch, could be main or master or any other branch git use.

Finally the program will ask for the place to git pull the repo in the example will go up 1 file and find the `app_to_update` directory.

If all the information is correct then the program will start running waiting for any update in the repo. 

### Step 5 (Monitoring)

Please be aware that if the commands you set in the commands before and after the updating are wrong or have an error, the program will show the error, so give a test for a short time like 1 minute and make a modification to the repo so you can see if everything is all right.



If you have any issue, fell free to ask me any question or contacting me.









