import bottle, json, subprocess, re


class Puller(object):
    def __init__(self, mailer):
        self._mailer = mailer
        self._threads = []
    
    def branch(self, repo, branch):
        thread = Thread(target=self._pull_branch, args=(repo, branch, app.config.mailer))
        thread.start()
        self._threads.append(thread)
    
    def _pull_branch(self, repo, branch):
        p = subprocess.Popen(['git', 'pull'], cwd=repo["branches"][branch][local], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print "------------"
        print ""
        print out
        print "------------"
        print err
        print ""
        print "------------"
        msgtext = out + "<br/>" + err
        self._mailer.send_email(repo["notification"].split(","), "abc", msgtext)
    
    
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
        
        log.debug("Sending email using %s" % self._conf['fqdn'])
        thread = Thread(target=self._send, args=(email_addrs, msg.as_string()))
        thread.start()
        self._threads.append(thread)
    
    def _send(self, email_addrs, msg):
        proto = self._conf['proto']
        assert proto in ('smtp', 'starttls', 'ssl'), \
            "Incorrect protocol: %s" % proto
        
        try:
            if proto == 'ssl':
                log.debug("Setting up SSL")
                session = SMTP_SSL(self._conf['fqdn'], self._conf['port'])
            else:
                session = SMTP(self._conf['fqdn'], self._conf['port'])
            
            if proto == 'starttls':
                log.debug('Sending EHLO and STARTTLS')
                session.ehlo()
                session.starttls()
                session.ehlo()
            
            if self._conf['user'] is not None:
                log.debug('Performing login')
                session.login(self._conf['user'], self._conf['pass'])
            
            log.debug('Sending')
            session.sendmail(self.sender, email_addrs, msg)
            session.quit()
            log.info('Email sent')
        
        except Exception as e:  # pragma: no cover
            log.error("Error sending email: %s" % e, exc_info=True)
    
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

@app.post('/pull')
def pull():
    branch = ""
    repo = None
    data = None
    
    if bottle.request.json:
        data = bottle.request.json
    elif bottle.request.forms.get('payload', None):
        data = json.loads(abc)

    print data

    if data:
        if "ref" in data:
            branch = data["ref"].split('/')[-1]

        if "repository" in data:
            if "name" in data["repository"]:
                if data["repository"]["name"] in config["repos"]:
                    repo = config["repos"][data["repository"]["name"]]
                    if branch in repo["branches"]:
                        print "ok"
                    #app.config.puller.branch(repo, branch)

