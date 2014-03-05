import bottle, json, re, subprocess, datetime
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL

class Puller(object):
    def __init__(self, mailer):
        self._mailer = mailer
        self._threads = []
    
    def branch(self, repo, name, branch, tmpl):
        thread = Thread(target=self._pull_branch, args=(repo, name, branch, tmpl))
        thread.start()
        self._threads.append(thread)
    
    def _pull_branch(self, repo, name, branch, tmpl):
        now = datetime.datetime.now()
        
        output = []
        error = []
        
        out, err = subprocess.Popen(['git', 'pull', repo["remote"]], cwd=repo["branches"][branch]["local"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        output.extend(out.splitlines())
        error.extend(err.splitlines())
        
        if "post-script" in repo["branches"][branch]:
            out, err = subprocess.Popen([repo["branches"][branch]["post-script"]], cwd=repo["branches"][branch]["local"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            output.extend(out.splitlines())
            error.extend(err.splitlines())
        
        if "template" in repo:
            tmpl = repo["template"]
        email_text = bottle.template(tmpl, repository=repo, name=name, branch=branch, output=output, error=error, now=now)
        self._mailer.send_email(repo["notification"].split(","), "Did a git pull for {repo} on {branch}".format(repo = name, branch = branch), email_text)
    
    
    def join(self):
        return [t.join(self.join_timeout) for t in self._threads]
    
    def __del__(self):
        self.join()



class Mailer(object):
    def __init__(self, sender, smtp_url, join_timeout=5):
        self.sender = sender
        self.join_timeout = join_timeout
        self._threads = []
        self._conf = self._parse_smtp_url(smtp_url)
    
    def _parse_smtp_url(self, url):
        """Parse SMTP URL"""
        match = re.match(r"""
            (                                   # Optional protocol
            (?P<proto>smtp|starttls|ssl)    # Protocol name
            ://
            )?
            (                                   # Optional user:pass@
            (?P<user>[^:]*)                 # Match every char except ':'
            (: (?P<pass>.*) )? @            # Optional :pass
            )?
            (?P<fqdn>                           # Required FQDN on IP address
            ()|                             # Empty string
            (                               # FQDN
            [a-zA-Z_\-]                 # First character cannot be a number
            [a-zA-Z0-9_\-\.]{,254}
            )
            |(                              # IPv4
            ([0-9]{1,3}\.){3}
            [0-9]{1,3}
            )
            |(                              # IPv6
            \[                          # Square brackets
            ([0-9a-f]{,4}:){1,8}
            [0-9a-f]{,4}
            \]
            )
            )
            (                                   # Optional :port
            :
            (?P<port>[0-9]{,5})             # Up to 5-digits port
            )?
            [/]?
            $
            """, url, re.VERBOSE)
        
        if not match:
            raise RuntimeError("SMTP URL seems incorrect")
        
        d = match.groupdict()
        if d['proto'] is None:
            d['proto'] = 'smtp'
        
        if d['port'] is None:
            d['port'] = 25
        else:
            d['port'] = int(d['port'])
        
        if not 0 < d['port'] < 65536:
            raise RuntimeError("Incorrect SMTP port")
        
        return d
    
    def send_email(self, email_addrs, subject, email_text):
        if not (self._conf['fqdn'] and self.sender):
            raise NameError("SMTP server or sender not set")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ", ".join(email_addrs)
        part = MIMEText(email_text, 'html')
        msg.attach(part)
        
        thread = Thread(target=self._send, args=(email_addrs, msg.as_string()))
        thread.start()
        self._threads.append(thread)
    
    def _send(self, email_addrs, msg):
        proto = self._conf['proto']
        assert proto in ('smtp', 'starttls', 'ssl'), \
            "Incorrect protocol: %s" % proto
        
        try:
            if proto == 'ssl':
                session = SMTP_SSL(self._conf['fqdn'], self._conf['port'])
            else:
                session = SMTP(self._conf['fqdn'], self._conf['port'])
            
            if proto == 'starttls':
                session.ehlo()
                session.starttls()
                session.ehlo()
            
            if self._conf['user'] is not None:
                session.login(self._conf['user'], self._conf['pass'])
            
            session.sendmail(self.sender, email_addrs, msg)
            session.quit()

        except Exception as e:  # pragma: no cover
            ''' '''
            print str(e)

    def join(self):
        """Flush email queue by waiting the completion of the existing threads
            
            :returns: None
            """
        return [t.join(self.join_timeout) for t in self._threads]
    
    def __del__(self):
        """Class destructor: wait for threads to terminate within a timeout"""
        self.join()





config = json.load(open('./iocast-hook-server.json'))
app = bottle.Bottle()
app.config.mailer = Mailer(config["mailer"]["sender"], config["mailer"]["smtp"])
app.config.puller = Puller(app.config.mailer)

@app.post('/push')
def pull():
    branch = None
    repo = None
    data = None
    
    if bottle.request.json:
        data = bottle.request.json
    elif bottle.request.forms.get('payload', None):
        data = json.loads(bottle.request.forms.get('payload'))
    
    print data

    if data:
        if "ref" in data:
            branch = data["ref"].split('/')[-1]
        elif "commits" in data and len(data["commits"]) > 0:
            branch = data["commits"][0]["branch"]

        if branch and "repository" in data:
            if "name" in data["repository"]:
                if data["repository"]["name"] in config["repos"]:
                    repo = config["repos"][data["repository"]["name"]]
                    if branch in repo["branches"]:
                        app.config.puller.branch(repo, data["repository"]["name"], branch, config["template"])



@app.route('/')
@bottle.view('repo_overview.tpl')
def index():
    return dict(config = config)

