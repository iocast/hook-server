# hook-server

hook-server is a Python server which updates a git repository triggered by a post hook comming from [GitHub](https://developer.github.com/webhooks/) or [Bitbucket](https://confluence.atlassian.com/display/BITBUCKET/Manage+Bitbucket+hooks).

## installation

For both methods described below you could use a virtual environment. So lets first create a ```virtualenv``` and install the necessary dependencies:

	virtualenv /opt/virtualenv/hook-server-hook
	source /opt/virtualenv/hook-server/bin/activate
	pip install bottle
	deactivate


### standalone

A script is provided to run this server in standalone mode.

	sudo -u www-data python hook-server_standalone.py --port 8080 --host localhost --virtualenv /opt/virtualenv/hook-server


### nginx, uwsgi

In the ```hook-server_nginx_site.conf``` change the ```server_name```, ```root``` which is your home directory of the application, as well as the ```listen``` parameter.

Now change i nthe ```hook-server_uwsgi_vassal.xml``` the path to your virtual environement which is the key ```virtualenv``` and if necessary the path to the log ```daemonize```.

In my environment I use ```upstart``` to control my services. For uwsgi I have craeted a ```uwsgi.conf``` in ```/etc/init``` with the following content


	# uWSGI - manage uWSGI application server
	#
	
	description     "uWSGI Emperor"
	
	start on (filesystem and net-device-up IFACE=lo)
	stop on runlevel [!2345]
	
	respawn
	
	env LOGTO=/var/log/uwsgi/uwsgi.log
	env BINPATH=/usr/bin/uwsgi
	
	pre-start script
		mkdir -p -m0755 /var/run/uwsgi
	end script
	
	exec $BINPATH --emperor /opt/www/vassals/ --pidfile /var/run/uwsgi/emperor.pid --stats 127.0.0.1:9191 --logto $LOGTO


that creates a ```/var/run/uwsgi``` folder for the ```pid``` files and starts the applications using the configuration file in ```/opt/www/vassals/```.

In this case, create a link of the **nginx site configuration** to the nginxs' site directory and a link of the **vassal** file to the emperor directory.

	ln -s /opt/www/hook-server_nginx_site.conf /etc/nginx/sites-available/hook-server
	ln -s /etc/nginx/sites-available/hook-server /etc/nginx/sites-enabled/
	ln -s /opt/www/hook-server_uwsgi_vassal.xml /opt/www/vassals/hook-server.xml


## configuration

The configuration for the repositories to which this sever need to listen to, are configured in the ```hook-server.json``` file. First you need to define your **SMTP mail server** and the sender address. When an update of a repository was triggered by the Git hook, then server will update the specific branch and sending out a mail as notification using the global template or the one from the repository. Thus, inside ```repos``` you define for each repository to listen at

* your repository name as key,
* a comma seperated list of notifiers (```notification```),
* optionally a ```template``` to be used, which should be stored in the **views** subfolder,
* and all your ```branches``` you want to listen to.

For each each branch you define

* the branch name as ```key```,
* the location where it is (```local```) and
* optinally you can define a postprocessing script (```post-script```).

Here is a example

	{
		"mailer": {
			"sender": "support@example.com",
			"smtp": "starttls://user:password@mail.example.com:587"
		},
		"template": "pull_report.tpl",
		"repos": {
			"hook-server": {
				"notification": "iocast@me.com",
				"branches": {
					"master": {
						"local": "/opt/repos/hook-server"
					}
				}
			},
			"repo2": {
				"notification": "support@example.com",
				"template": "repo2_report.tpl",
				"branches": {
					"master": {
						"local": "/opt/repos/repo2-master",
						"post-script": "scripts/post-processing.sh"
					},
					"develop": {
						"local": "/opt/repos/repo2-develop",
						"post-script": "scripts/post-processing.sh"
					}
				}
			}
		}
	}



## FAQ

> How do I add a private repository?

Simply clone your private repository over **https** and add the password to the password to the remote url. E.g.:

	git clone https://user@github.com/user/test-repo.git
	cd test-repo
	git config remote.origin.url https://user:password@github.com/user/test-repo.git


## Problems

### getting error `commit your changes or stash them`

**error**

    From https://bitbucket.org/<user>/<repo>
      * branch            master     -> FETCH_HEAD
        0a26dcf..97ed7c0  master     -> origin/master
    error: Your local changes to the following files would be overwritten by merge:
     destination/file.md
    Please, commit your changes or stash them before you can merge.
    Aborting


**resolution**

1. first check on the local repository that everything is commited and pushed.
2. check if erverything is on the server repository (on GitHub or Bitbucket)
3. now login to the server and solve the conflicts by running the below commands

**commands to proceed on the server**

    cd /to/your/repo/

do a `git pull` to check if problem still occurs

    sudo git pull
    > Updating ac52482..97ed7c0
    > error: Your local changes to the following files would be overwritten by merge:
    >         destination/file.md
    > Please, commit your changes or stash them before you can merge.
    > Aborting

do a revert to the latest `HEAD`

    sudo git reset --hard HEAD
    > HEAD is now at ac52482 no message
    sudo git pull
    > Updating ac52482..97ed7c0
    > Fast-forward
    > ...           |   7 ++++---
    > ...           | Bin 2870 -> 85890 bytes
    > 2 files changed, 4 insertions(+), 3 deletions(-)

and change the permissions back

    sudo chown -R www-data:www-data .

and depending on your server security also the permissions

    sudo chmod -R 775 .
