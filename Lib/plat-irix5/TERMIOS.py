# Generated by h2py from /usr/include/termios.h

# Included from sys/termios.h

# Included from sys/ttydev.h
B0 = 0
B50 = 0000001
B75 = 0000002
B110 = 0000003
B134 = 0000004
B150 = 0000005
B200 = 0000006
B300 = 0000007
B600 = 0000010
B1200 = 0000011
B1800 = 0000012
B2400 = 0000013
B4800 = 0000014
B9600 = 0000015
B19200 = 0000016
EXTA = 0000016
B38400 = 0000017
EXTB = 0000017

# Included from sys/types.h

# Included from sgidefs.h
_MIPS_ISA_MIPS1 = 1
_MIPS_ISA_MIPS2 = 2
_MIPS_ISA_MIPS3 = 3
_MIPS_ISA_MIPS4 = 4
_MIPS_SIM_ABI32 = 1
_MIPS_SIM_ABI64 = 2
P_MYID = (-1)
P_MYHOSTID = (-1)

# Included from sys/bsd_types.h

# Included from sys/mkdev.h
ONBITSMAJOR = 7
ONBITSMINOR = 8
OMAXMAJ = 0x7f
OMAXMIN = 0xff
NBITSMAJOR = 14
NBITSMINOR = 18
MAXMAJ = 0xff
MAXMIN = 0x3ffff
OLDDEV = 0
NEWDEV = 1
MKDEV_VER = NEWDEV
def major(dev): return __major(MKDEV_VER, dev)

def minor(dev): return __minor(MKDEV_VER, dev)


# Included from sys/select.h
FD_SETSIZE = 1024
NBBY = 8
_POSIX_VDISABLE = 0
def CTRL(c): return ((c)&037)

IBSHIFT = 16
NCC = 8
NCCS = 23
VINTR = 0
VQUIT = 1
VERASE = 2
VKILL = 3
VEOF = 4
VEOL = 5
VEOL2 = 6
VMIN = 4
VTIME = 5
VSWTCH = 7
VSTART = 8
VSTOP = 9
VSUSP = 10
VDSUSP = 11
VREPRINT = 12
VDISCARD = 13
VWERASE = 14
VLNEXT = 15
VRPRNT = VREPRINT
VFLUSHO = VDISCARD
VCEOF = NCC
VCEOL = (NCC + 1)
CNUL = 0
CDEL = 0377
CESC = ord('\\')
CINTR = 0177
CQUIT = 034
CERASE = CTRL(ord('H'))
CKILL = CTRL(ord('U'))
CEOL = 0
CEOL2 = 0
CEOF = CTRL(ord('d'))
CEOT = CEOF
CSTART = CTRL(ord('q'))
CSTOP = CTRL(ord('s'))
CSWTCH = CTRL(ord('z'))
CNSWTCH = 0
CSUSP = CSWTCH
CLNEXT = CTRL(ord('v'))
CWERASE = CTRL(ord('w'))
CFLUSHO = CTRL(ord('o'))
CFLUSH = CFLUSHO
CRPRNT = CTRL(ord('r'))
CDSUSP = CTRL(ord('y'))
CBRK = 0377
IGNBRK = 0000001
BRKINT = 0000002
IGNPAR = 0000004
PARMRK = 0000010
INPCK = 0000020
ISTRIP = 0000040
INLCR = 0000100
IGNCR = 0000200
ICRNL = 0000400
IUCLC = 0001000
IXON = 0002000
IXANY = 0004000
IXOFF = 0010000
IMAXBEL = 0020000
IBLKMD = 0040000
OPOST = 0000001
OLCUC = 0000002
ONLCR = 0000004
OCRNL = 0000010
ONOCR = 0000020
ONLRET = 0000040
OFILL = 0000100
OFDEL = 0000200
NLDLY = 0000400
NL0 = 0
NL1 = 0000400
CRDLY = 0003000
CR0 = 0
CR1 = 0001000
CR2 = 0002000
CR3 = 0003000
TABDLY = 0014000
TAB0 = 0
TAB1 = 0004000
TAB2 = 0010000
TAB3 = 0014000
XTABS = 0014000
BSDLY = 0020000
BS0 = 0
BS1 = 0020000
VTDLY = 0040000
VT0 = 0
VT1 = 0040000
FFDLY = 0100000
FF0 = 0
FF1 = 0100000
PAGEOUT = 0200000
WRAP = 0400000
CBAUD = 000000017
CSIZE = 000000060
CS5 = 0
CS6 = 000000020
CS7 = 000000040
CS8 = 000000060
CSTOPB = 000000100
CREAD = 000000200
PARENB = 000000400
PARODD = 000001000
HUPCL = 000002000
CLOCAL = 000004000
RCV1EN = 000010000
XMT1EN = 000020000
LOBLK = 000040000
XCLUDE = 000100000
CIBAUD = 003600000
PAREXT = 004000000
CNEW_RTSCTS = 010000000
ISIG = 0000001
ICANON = 0000002
XCASE = 0000004
ECHO = 0000010
ECHOE = 0000020
ECHOK = 0000040
ECHONL = 0000100
NOFLSH = 0000200
IEXTEN = 0000400
ITOSTOP = 0100000
TOSTOP = ITOSTOP
ECHOCTL = 0001000
ECHOPRT = 0002000
ECHOKE = 0004000
DEFECHO = 0010000
FLUSHO = 0020000
PENDIN = 0040000
TIOC = (ord('T')<<8)
TCGETA = (TIOC|1)
TCSETA = (TIOC|2)
TCSETAW = (TIOC|3)
TCSETAF = (TIOC|4)
TCSBRK = (TIOC|5)
TCXONC = (TIOC|6)
TCFLSH = (TIOC|7)

# Included from sys/ioctl.h
IOCTYPE = 0xff00
LIOC = (ord('l')<<8)
LIOCGETP = (LIOC|1)
LIOCSETP = (LIOC|2)
LIOCGETS = (LIOC|5)
LIOCSETS = (LIOC|6)
DIOC = (ord('d')<<8)
DIOCGETC = (DIOC|1)
DIOCGETB = (DIOC|2)
DIOCSETE = (DIOC|3)

# Included from sys/ioccom.h
IOCPARM_MASK = 0xff
IOC_VOID = 0x20000000
IOC_OUT = 0x40000000
IOC_IN = 0x80000000
IOC_INOUT = (IOC_IN|IOC_OUT)

# Included from net/soioctl.h

# Included from sys/termio.h
CLNEXT = CTRL(ord('v'))
CWERASE = CTRL(ord('w'))
CFLUSHO = CTRL(ord('o'))
CFLUSH = CFLUSHO
CRPRNT = CTRL(ord('r'))
CDSUSP = CTRL(ord('y'))
SSPEED = B9600
TERM_NONE = 0
TERM_TEC = 1
TERM_V61 = 2
TERM_V10 = 3
TERM_TEX = 4
TERM_D40 = 5
TERM_H45 = 6
TERM_D42 = 7
TM_NONE = 0000
TM_SNL = 0001
TM_ANL = 0002
TM_LCF = 0004
TM_CECHO = 0010
TM_CINVIS = 0020
TM_SET = 0200
LDISC0 = 0
LDISC1 = 1
NTTYDISC = LDISC1
TIOCFLUSH = (TIOC|12)
TCSETLABEL = (TIOC|13)
TCDSET = (TIOC|32)
TCBLKMD = (TIOC|33)
TIOCPKT = (TIOC|112)
TIOCPKT_DATA = 0x00
TIOCPKT_FLUSHREAD = 0x01
TIOCPKT_FLUSHWRITE = 0x02
TIOCPKT_NOSTOP = 0x10
TIOCPKT_DOSTOP = 0x20
TIOCPKT_IOCTL = 0x40
TIOCNOTTY = (TIOC|113)
TIOCSTI = (TIOC|114)
TFIOC = (ord('F')<<8)
oFIONREAD = (TFIOC|127)
TO_STOP = LOBLK
IOCTYPE = 0xff00
TCGETS = (TIOC|13)
TCSETS = (TIOC|14)
TCSETSW = (TIOC|15)
TCSETSF = (TIOC|16)
TCSANOW = ((ord('T')<<8)|14)
TCSADRAIN = ((ord('T')<<8)|15)
TCSAFLUSH = ((ord('T')<<8)|16)
TCIFLUSH = 0
TCOFLUSH = 1
TCIOFLUSH = 2
TCOOFF = 0
TCOON = 1
TCIOFF = 2
TCION = 3
tIOC = (ord('t')<<8)
TIOCGETD = (tIOC|0)
TIOCSETD = (tIOC|1)
TIOCHPCL = (tIOC|2)
TIOCGETP = (tIOC|8)
TIOCSETP = (tIOC|9)
TIOCSETN = (tIOC|10)
TIOCEXCL = (tIOC|13)
TIOCNXCL = (tIOC|14)
TIOCSETC = (tIOC|17)
TIOCGETC = (tIOC|18)
TIOCLBIS = (tIOC|127)
TIOCLBIC = (tIOC|126)
TIOCLSET = (tIOC|125)
TIOCLGET = (tIOC|124)
TIOCSBRK = (tIOC|123)
TIOCCBRK = (tIOC|122)
TIOCSDTR = (tIOC|121)
TIOCCDTR = (tIOC|120)
TIOCSLTC = (tIOC|117)
TIOCGLTC = (tIOC|116)
TIOCOUTQ = (tIOC|115)
TIOCSTOP = (tIOC|111)
TIOCSTART = (tIOC|110)
TIOCGSID = (tIOC|22)
TIOCSSID = (tIOC|24)
TIOCMSET = (tIOC|26)
TIOCMBIS = (tIOC|27)
TIOCMBIC = (tIOC|28)
TIOCMGET = (tIOC|29)
TIOCM_LE = 0001
TIOCM_DTR = 0002
TIOCM_RTS = 0004
TIOCM_ST = 0010
TIOCM_SR = 0020
TIOCM_CTS = 0040
TIOCM_CAR = 0100
TIOCM_CD = TIOCM_CAR
TIOCM_RNG = 0200
TIOCM_RI = TIOCM_RNG
TIOCM_DSR = 0400
TIOCREMOTE = (tIOC|30)
TIOCSIGNAL = (tIOC|31)
ISPTM = ((ord('P')<<8)|1)
UNLKPT = ((ord('P')<<8)|2)
SVR4SOPEN = ((ord('P')<<8)|100)
LDIOC = (ord('D')<<8)
LDOPEN = (LDIOC|0)
LDCLOSE = (LDIOC|1)
LDCHG = (LDIOC|2)
LDGETT = (LDIOC|8)
LDSETT = (LDIOC|9)
LDSMAP = (LDIOC|10)
LDGMAP = (LDIOC|11)
LDNMAP = (LDIOC|12)
DIOC = (ord('d')<<8)
DIOCGETP = (DIOC|8)
DIOCSETP = (DIOC|9)
FIORDCHK = ((ord('f')<<8)|3)
