"""An object-oriented interface to .netrc files."""

# Module and documentation by Eric S. Raymond, 21 Dec 1998

import os, shlex

__all__ = ["netrc", "NetrcParseError"]


class NetrcParseError(Exception):
    """Exception raised on syntax errors in the .netrc file."""
    def __init__(self, msg, filename=None, lineno=None):
        self.filename = filename
        self.lineno = lineno
        self.msg = msg
        Exception.__init__(self, msg)

    def __str__(self):
        return "%s (%s, line %s)" % (self.msg, self.filename, self.lineno)


class netrc:
    def __init__(self, file=None):
        if not file:
            file = os.path.join(os.environ['HOME'], ".netrc")
        fp = open(file)
        self.hosts = {}
        self.macros = {}
        lexer = shlex.shlex(fp)
        # Allows @ in hostnames.  Not a big deal...
        lexer.wordchars = lexer.wordchars + '.-@'
        while 1:
            # Look for a machine, default, or macdef top-level keyword
            toplevel = tt = lexer.get_token()
            if not tt:
                break
            elif tt == 'machine':
                entryname = lexer.get_token()
            elif tt == 'default':
                entryname = 'default'
            elif tt == 'macdef':                # Just skip to end of macdefs
                entryname = lexer.get_token()
                self.macros[entryname] = []
                lexer.whitepace = ' \t'
                while 1:
                    line = lexer.instream.readline()
                    if not line or line == '\012' and tt == '\012':
                        lexer.whitepace = ' \t\r\n'
                        break
                    tt = line
                    self.macros[entryname].append(line)
            else:
                raise NetrcParseError(
                    "bad toplevel token %r" % tt, file, lexer.lineno)

            # We're looking at start of an entry for a named machine or default.
            if toplevel == 'machine':
                login = account = password = None
                self.hosts[entryname] = {}
            while 1:
                tt = lexer.get_token()
                if tt=='' or tt == 'machine' or tt == 'default' or tt == 'macdef':
                    if toplevel == 'macdef':
                        break
                    elif login and password:
                        self.hosts[entryname] = (login, account, password)
                        lexer.push_token(tt)
                        break
                    else:
                        raise NetrcParseError(
                            "malformed %s entry %s terminated by %s"
                            % (toplevel, entryname, repr(tt)),
                            file, lexer.lineno)
                elif tt == 'login' or tt == 'user':
                    login = lexer.get_token()
                elif tt == 'account':
                    account = lexer.get_token()
                elif tt == 'password':
                    password = lexer.get_token()
                else:
                    raise NetrcParseError("bad follower token %r" % tt,
                                          file, lexer.lineno)

    def authenticators(self, host):
        """Return a (user, account, password) tuple for given host."""
        if self.hosts.has_key(host):
            return self.hosts[host]
        elif self.hosts.has_key('default'):
            return self.hosts['default']
        else:
            return None

    def __repr__(self):
        """Dump the class data in the format of a .netrc file."""
        rep = ""
        for host in self.hosts.keys():
            attrs = self.hosts[host]
            rep = rep + "machine "+ host + "\n\tlogin " + repr(attrs[0]) + "\n"
            if attrs[1]:
                rep = rep + "account " + repr(attrs[1])
            rep = rep + "\tpassword " + repr(attrs[2]) + "\n"
        for macro in self.macros.keys():
            rep = rep + "macdef " + macro + "\n"
            for line in self.macros[macro]:
                rep = rep + line
            rep = rep + "\n"
        return rep

if __name__ == '__main__':
    print netrc()
