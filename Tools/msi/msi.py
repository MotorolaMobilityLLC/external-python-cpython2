# Python MSI Generator
# (C) 2003 Martin v. Loewis
# See "FOO" in comments refers to MSDN sections with the title FOO.
import msilib, schema, sequence, os, glob, time
from msilib import Feature, CAB, Directory, Dialog, Binary, add_data
import uisample
from win32com.client import constants

# Settings can be overridden in config.py below
# 1 for Itanium build
msilib.Win64 = 0
# 0 for official python.org releases
# 1 for intermediate releases by anybody, with
# a new product code for every package.
snapshot = 1
# 1 means that file extension is px, not py,
# and binaries start with x
testpackage = 0
# Location of build tree
srcdir = os.path.abspath("../..")
# Text to be displayed as the version in dialogs etc.
# goes into file name and ProductCode. Defaults to
# current_version.day for Snapshot, current_version otherwise
full_current_version = None

try:
    from config import *
except ImportError:
    pass

# Extract current version from Include/patchlevel.h
lines = open(srcdir + "/Include/patchlevel.h").readlines()
major = minor = micro = level = serial = None
levels = {
    'PY_RELEASE_LEVEL_ALPHA':0xA,
    'PY_RELEASE_LEVEL_BETA': 0xB,
    'PY_RELEASE_LEVEL_GAMMA':0xC,
    'PY_RELEASE_LEVEL_FINAL':0xF
    }
for l in lines:
    if not l.startswith("#define"):
        continue
    l = l.split()
    if len(l) != 3:
        continue
    _, name, value = l
    if name == 'PY_MAJOR_VERSION': major = value
    if name == 'PY_MINOR_VERSION': minor = value
    if name == 'PY_MICRO_VERSION': micro = value
    if name == 'PY_RELEASE_LEVEL': level = levels[value]
    if name == 'PY_RELEASE_SERIAL': serial = value

short_version = major+"."+minor
# See PC/make_versioninfo.c
FIELD3 = 1000*int(micro) + 10*level + int(serial)
current_version = "%s.%d" % (short_version, FIELD3)

# This should never change. The UpgradeCode of this package can be
# used in the Upgrade table of future packages to make the future
# package replace this one. See "UpgradeCode Property".
upgrade_code_snapshot='{92A24481-3ECB-40FC-8836-04B7966EC0D5}'
upgrade_code='{65E6DE48-A358-434D-AA4F-4AF72DB4718F}'

# This should be extended for each Python release.
# The product code must change whenever the name of the MSI file
# changes, and when new component codes are issued for existing
# components. See "Changing the Product Code". As we change the
# component codes with every build, we need a new product code
# each time. For intermediate (snapshot) releases, they are automatically
# generated. For official releases, we record the product codes,
# so people can refer to them.
product_codes = {
    '2.4.101': '{0e9b4d8e-6cda-446e-a208-7b92f3ddffa0}', # 2.4a1, released as a snapshot
    '2.4.102': '{1b998745-4901-4edb-bc52-213689e1b922}', # 2.4a2
    '2.4.103': '{33fc8bd2-1e8f-4add-a40a-ade2728d5942}', # 2.4a3
    '2.4.111': '{51a7e2a8-2025-4ef0-86ff-e6aab742d1fa}', # 2.4b1
    '2.4.112': '{4a5e7c1d-c659-4fe3-b8c9-7c65bd9c95a5}', # 2.4b2
    '2.4.121': '{75508821-a8e9-40a8-95bd-dbe6033ddbea}', # 2.4c1
    '2.4.122': '{83a9118b-4bdd-473b-afc3-bcb142feca9e}', # 2.4c2
    '2.4.150': '{82d9302e-f209-4805-b548-52087047483a}', # 2.4.0
}

if snapshot:
    current_version = "%s.%s.%s" % (major, minor, int(time.time()/3600/24))
    product_code = msilib.gen_uuid()
else:
    product_code = product_codes[current_version]

if full_current_version is None:
    full_current_version = current_version

extensions = [
    'bz2.pyd',
    'pyexpat.pyd',
    'select.pyd',
    'unicodedata.pyd',
    'winsound.pyd',
    'zlib.pyd',
    '_bsddb.pyd',
    '_socket.pyd',
    '_ssl.pyd',
    '_testcapi.pyd',
    '_tkinter.pyd',
]

if major+minor <= "23":
    extensions.extend([
    '_csv.pyd',
    '_sre.pyd',
    '_symtable.pyd',
    '_winreg.pyd',
    'datetime.pyd'
    'mmap.pyd',
    'parser.pyd',    
    ])

if testpackage:
    ext = 'px'
    testprefix = 'x'
else:
    ext = 'py'
    testprefix = ''

if msilib.Win64:
    SystemFolderName = "[SystemFolder64]"
else:
    SystemFolderName = "[SystemFolder]"

msilib.reset()

# condition in which to install pythonxy.dll in system32:
# a) it is Windows 9x or
# b) it is NT, the user is privileged, and has chosen per-machine installation
sys32cond = "(Windows9x or (Privileged and ALLUSERS))"

# Install extensions if the feature goes into
# INSTALLSTATE_ADVERTISED or INSTALLSTATE_LOCAL
want_extensions = "(&Extensions = 1) or (&Extensions = 3)"

def build_database():
    """Generate an empty database, with just the schema and the
    Summary information stream."""
    if snapshot:
        uc = upgrade_code_snapshot
    else:
        uc = upgrade_code
    # schema represents the installer 2.0 database schema.
    # sequence is the set of standard sequences
    # (ui/execute, admin/advt/install)
    if msilib.Win64:
        w64 = ".ia64"
    else:
        w64 = ""
    db = msilib.init_database("python-%s%s.msi" % (full_current_version, w64), 
                  schema, ProductName="Python "+full_current_version,
                  ProductCode=product_code,
                  ProductVersion=current_version,
                  Manufacturer=u"Martin v. L\xf6wis")
    # The default sequencing of the RemoveExistingProducts action causes
    # removal of files that got just installed. Place it after
    # InstallInitialize, so we first uninstall everything, but still roll
    # back in case the installation is interrupted
    msilib.change_sequence(sequence.InstallExecuteSequence,
                           "RemoveExistingProducts", 1510)
    # Conditionalize Extension information
    msilib.change_sequence(sequence.InstallExecuteSequence,
                            "RegisterClassInfo", cond=want_extensions)
    msilib.change_sequence(sequence.InstallExecuteSequence,
                            "RegisterExtensionInfo", cond=want_extensions)
    msilib.change_sequence(sequence.InstallExecuteSequence,
                            "RegisterProgIdInfo", cond=want_extensions)
    msilib.change_sequence(sequence.InstallExecuteSequence,
                            "RegisterMIMEInfo", cond=want_extensions)
    msilib.add_tables(db, sequence)
    # We cannot set ALLUSERS in the property table, as this cannot be
    # reset if the user choses a per-user installation. Instead, we
    # maintain WhichUsers, which can be "ALL" or "JUSTME". The UI manages
    # this property, and when the execution starts, ALLUSERS is set
    # accordingly.
    add_data(db, "Property", [("UpgradeCode", uc),
                              ("WhichUsers", "ALL"),
                             ])
    db.Commit()
    return db

def remove_old_versions(db):
    "Fill the upgrade table."
    start = "%s.%s.0" % (major, minor)
    # This requests that feature selection states of an older
    # installation should be forwarded into this one. Upgrading
    # requires that both the old and the new installation are
    # either both per-machine or per-user.
    migrate_features = 1
    # See "Upgrade Table". We remove releases with the same major and
    # minor version. For an snapshot, we remove all earlier snapshots. For
    # a release, we remove all snapshots, and all earlier releases.
    if snapshot:
        add_data(db, "Upgrade",
            [(upgrade_code_snapshot, start,  
              current_version,
              None,                     # Ignore language
              migrate_features, 
              None,                     # Migrate ALL features
              "REMOVEOLDSNAPSHOT")])
        props = "REMOVEOLDSNAPSHOT"
    else:
        add_data(db, "Upgrade",
            [(upgrade_code, start, current_version,
              None, migrate_features, None, "REMOVEOLDVERSION"),
             (upgrade_code_snapshot, start, "%s.%d.0" % (major, int(minor)+1),
              None, migrate_features, None, "REMOVEOLDSNAPSHOT")])
        props = "REMOVEOLDSNAPSHOT;REMOVEOLDVERSION"
    # Installer collects the product codes of the earlier releases in
    # these properties. In order to allow modification of the properties,
    # they must be declared as secure. See "SecureCustomProperties Property"
    add_data(db, "Property", [("SecureCustomProperties", props)])

class PyDialog(Dialog):
    """Dialog class with a fixed layout: controls at the top, then a ruler,
    then a list of buttons: back, next, cancel. Optionally a bitmap at the
    left."""
    def __init__(self, *args, **kw):
        """Dialog(database, name, x, y, w, h, attributes, title, first,
        default, cancel, bitmap=true)"""
        Dialog.__init__(self, *args)
        ruler = self.h - 36
        bmwidth = 152*ruler/328
        if kw.get("bitmap", True):
            self.bitmap("Bitmap", 0, 0, bmwidth, ruler, "PythonWin")
        self.line("BottomLine", 0, ruler, self.w, 0)

    def title(self, title):
        "Set the title text of the dialog at the top."
        # name, x, y, w, h, flags=Visible|Enabled|Transparent|NoPrefix,
        # text, in VerdanaBold10
        self.text("Title", 135, 10, 220, 60, 0x30003,
                  r"{\VerdanaBold10}%s" % title)

    def back(self, title, next, name = "Back", active = 1):
        """Add a back button with a given title, the tab-next button,
        its name in the Control table, possibly initially disabled.

        Return the button, so that events can be associated"""
        if active:
            flags = 3 # Visible|Enabled
        else:
            flags = 1 # Visible
        return self.pushbutton(name, 180, self.h-27 , 56, 17, flags, title, next)

    def cancel(self, title, next, name = "Cancel", active = 1):
        """Add a cancel button with a given title, the tab-next button,
        its name in the Control table, possibly initially disabled.

        Return the button, so that events can be associated"""
        if active:
            flags = 3 # Visible|Enabled
        else:
            flags = 1 # Visible
        return self.pushbutton(name, 304, self.h-27, 56, 17, flags, title, next)

    def next(self, title, next, name = "Next", active = 1):
        """Add a Next button with a given title, the tab-next button,
        its name in the Control table, possibly initially disabled.

        Return the button, so that events can be associated"""
        if active:
            flags = 3 # Visible|Enabled
        else:
            flags = 1 # Visible
        return self.pushbutton(name, 236, self.h-27, 56, 17, flags, title, next)

    def xbutton(self, name, title, next, xpos):
        """Add a button with a given title, the tab-next button,
        its name in the Control table, giving its x position; the
        y-position is aligned with the other buttons.

        Return the button, so that events can be associated"""
        return self.pushbutton(name, int(self.w*xpos - 28), self.h-27, 56, 17, 3, title, next)

def add_ui(db):
    x = y = 50
    w = 370
    h = 300
    title = "[ProductName] Setup"

    # see "Dialog Style Bits"
    modal = 3      # visible | modal
    modeless = 1   # visible
    track_disk_space = 32

    add_data(db, 'ActionText', uisample.ActionText)
    add_data(db, 'UIText', uisample.UIText)

    # Bitmaps
    if not os.path.exists(srcdir+r"\PC\python_icon.exe"):
        raise "Run icons.mak in PC directory"
    add_data(db, "Binary",
             [("PythonWin", msilib.Binary(srcdir+r"\PCbuild\installer.bmp")), # 152x328 pixels
              ("py.ico",msilib.Binary(srcdir+r"\PC\py.ico")),
             ])
    add_data(db, "Icon",
             [("python_icon.exe", msilib.Binary(srcdir+r"\PC\python_icon.exe"))])

    # Scripts
    open("inst.vbs","w").write("""
    Function CheckDir()
      Set FSO = CreateObject("Scripting.FileSystemObject")
      if FSO.FolderExists(Session.Property("TARGETDIR")) then
        Session.Property("TargetExists") = "1"
      else
        Session.Property("TargetExists") = "0"
      end if
    End Function
    """)
    add_data(db, "Binary", [("Script", msilib.Binary("inst.vbs"))])
    # See "Custom Action Type 6"
    add_data(db, "CustomAction", [("CheckDir", 6, "Script", "CheckDir")])
    os.unlink("inst.vbs")


    # UI customization properties
    add_data(db, "Property",
             # See "DefaultUIFont Property"
             [("DefaultUIFont", "DlgFont8"),
              # See "ErrorDialog Style Bit"
              ("ErrorDialog", "ErrorDlg"),
              ("Progress1", "Install"),   # modified in maintenance type dlg
              ("Progress2", "installs"),
              ("MaintenanceForm_Action", "Repair")])

    # Fonts, see "TextStyle Table"
    add_data(db, "TextStyle",
             [("DlgFont8", "Tahoma", 9, None, 0),
              ("DlgFontBold8", "Tahoma", 8, None, 1), #bold
              ("VerdanaBold10", "Verdana", 10, None, 1),
             ])

    # See "CustomAction Table"
    add_data(db, "CustomAction", [
        # msidbCustomActionTypeFirstSequence + msidbCustomActionTypeTextData + msidbCustomActionTypeProperty
        # See "Custom Action Type 51",
        # "Custom Action Execution Scheduling Options"
        ("InitialTargetDir", 307, "TARGETDIR",
         "[WindowsVolume]Python%s%s" % (major, minor)),
        ("SetDLLDirToTarget", 307, "DLLDIR", "[TARGETDIR]"),
        ("SetDLLDirToSystem32", 307, "DLLDIR", SystemFolderName),
        # msidbCustomActionTypeExe + msidbCustomActionTypeSourceFile
        # See "Custom Action Type 18"
        ("CompilePyc", 18, "python.exe", r"[TARGETDIR]Lib\compileall.py [TARGETDIR]Lib"),
        ("CompilePyo", 18, "python.exe", r"-O [TARGETDIR]Lib\compileall.py [TARGETDIR]Lib")
        ])

    # UI Sequences, see "InstallUISequence Table", "Using a Sequence Table"
    # Numbers indicate sequence; see sequence.py for how these action integrate
    add_data(db, "InstallUISequence",
             [("PrepareDlg", "Not Privileged or Windows9x or Installed", 140),
              ("WhichUsersDlg", "Privileged and not Windows9x and not Installed", 141),
              ("InitialTargetDir", 'TARGETDIR=""', 750),
              # In the user interface, assume all-users installation if privileged.
              ("SetDLLDirToSystem32", 'DLLDIR="" and ' + sys32cond, 751),
              ("SetDLLDirToTarget", 'DLLDIR="" and not ' + sys32cond, 752),
              ("SelectDirectoryDlg", "Not Installed", 1230),
              # XXX no support for resume installations yet
              #("ResumeDlg", "Installed AND (RESUME OR Preselected)", 1240),
              ("MaintenanceTypeDlg", "Installed AND NOT RESUME AND NOT Preselected", 1250),
              ("ProgressDlg", None, 1280)])
    add_data(db, "AdminUISequence",
             [("InitialTargetDir", 'TARGETDIR=""', 750),
              ("SetDLLDirToTarget", 'DLLDIR=""', 751),
             ])

    # Execute Sequences
    add_data(db, "InstallExecuteSequence",
            [("InitialTargetDir", 'TARGETDIR=""', 750),
             ("SetDLLDirToSystem32", 'DLLDIR="" and ' + sys32cond, 751),
             ("SetDLLDirToTarget", 'DLLDIR="" and not ' + sys32cond, 752),
             ("CompilePyc", "COMPILEALL", 6800),
             ("CompilePyo", "COMPILEALL", 6801),
            ])
    add_data(db, "AdminExecuteSequence",
            [("InitialTargetDir", 'TARGETDIR=""', 750),
             ("SetDLLDirToTarget", 'DLLDIR=""', 751),
             ("CompilePyc", "COMPILEALL", 6800),
             ("CompilePyo", "COMPILEALL", 6801),
            ])

    #####################################################################
    # Standard dialogs: FatalError, UserExit, ExitDialog
    fatal=PyDialog(db, "FatalError", x, y, w, h, modal, title,
                 "Finish", "Finish", "Finish")
    fatal.title("[ProductName] Installer ended prematurely")
    fatal.back("< Back", "Finish", active = 0)
    fatal.cancel("Cancel", "Back", active = 0)
    fatal.text("Description1", 135, 70, 220, 80, 0x30003,
               "[ProductName] setup ended prematurely because of an error.  Your system has not been modified.  To install this program at a later time, please run the installation again.")
    fatal.text("Description2", 135, 155, 220, 20, 0x30003,
               "Click the Finish button to exit the Installer.")
    c=fatal.next("Finish", "Cancel", name="Finish")
    # See "ControlEvent Table". Parameters are the event, the parameter
    # to the action, and optionally the condition for the event, and the order
    # of events.
    c.event("EndDialog", "Exit")
    
    user_exit=PyDialog(db, "UserExit", x, y, w, h, modal, title,
                 "Finish", "Finish", "Finish")
    user_exit.title("[ProductName] Installer was interrupted")
    user_exit.back("< Back", "Finish", active = 0)
    user_exit.cancel("Cancel", "Back", active = 0)
    user_exit.text("Description1", 135, 70, 220, 80, 0x30003,
               "[ProductName] setup was interrupted.  Your system has not been modified.  "
               "To install this program at a later time, please run the installation again.")
    user_exit.text("Description2", 135, 155, 220, 20, 0x30003,
               "Click the Finish button to exit the Installer.")
    c = user_exit.next("Finish", "Cancel", name="Finish")
    c.event("EndDialog", "Exit")
    
    exit_dialog = PyDialog(db, "ExitDialog", x, y, w, h, modal, title,
                         "Finish", "Finish", "Finish")
    exit_dialog.title("Completing the [ProductName] Installer")
    exit_dialog.back("< Back", "Finish", active = 0)
    exit_dialog.cancel("Cancel", "Back", active = 0)
    exit_dialog.text("Description", 135, 115, 220, 20, 0x30003,
               "Click the Finish button to exit the Installer.")
    c = exit_dialog.next("Finish", "Cancel", name="Finish")
    c.event("EndDialog", "Return")

    #####################################################################
    # Required dialog: FilesInUse, ErrorDlg
    inuse = PyDialog(db, "FilesInUse",
                     x, y, w, h,
                     19,                # KeepModeless|Modal|Visible
                     title,
                     "Retry", "Retry", "Retry", bitmap=False)
    inuse.text("Title", 15, 6, 200, 15, 0x30003,
               r"{\DlgFontBold8}Files in Use")
    inuse.text("Description", 20, 23, 280, 20, 0x30003,
               "Some files that need to be updated are currently in use.")
    inuse.text("Text", 20, 55, 330, 50, 3,
               "The following applications are using files that need to be updated by this setup. Close these applications and then click Retry to continue the installation or Cancel to exit it.")
    inuse.control("List", "ListBox", 20, 107, 330, 130, 7, "FileInUseProcess",
                  None, None, None)
    c=inuse.back("Exit", "Ignore", name="Exit")
    c.event("EndDialog", "Exit")
    c=inuse.next("Ignore", "Retry", name="Ignore")
    c.event("EndDialog", "Ignore")
    c=inuse.cancel("Retry", "Exit", name="Retry")
    c.event("EndDialog","Retry")


    # See "Error Dialog". See "ICE20" for the required names of the controls.
    error = Dialog(db, "ErrorDlg",
                   50, 10, 330, 101,
                   65543,       # Error|Minimize|Modal|Visible
                   title,
                   "ErrorText", None, None)
    error.text("ErrorText", 50,9,280,48,3, "")
    error.control("ErrorIcon", "Icon", 15, 9, 24, 24, 5242881, None, "py.ico", None, None)
    error.pushbutton("N",120,72,81,21,3,"No",None).event("EndDialog","ErrorNo")
    error.pushbutton("Y",240,72,81,21,3,"Yes",None).event("EndDialog","ErrorYes")
    error.pushbutton("A",0,72,81,21,3,"Abort",None).event("EndDialog","ErrorAbort")
    error.pushbutton("C",42,72,81,21,3,"Cancel",None).event("EndDialog","ErrorCancel")
    error.pushbutton("I",81,72,81,21,3,"Ignore",None).event("EndDialog","ErrorIgnore")
    error.pushbutton("O",159,72,81,21,3,"Ok",None).event("EndDialog","ErrorOk")
    error.pushbutton("R",198,72,81,21,3,"Retry",None).event("EndDialog","ErrorRetry")

    #####################################################################
    # Global "Query Cancel" dialog
    cancel = Dialog(db, "CancelDlg", 50, 10, 260, 85, 3, title,
                    "No", "No", "No")
    cancel.text("Text", 48, 15, 194, 30, 3, 
                "Are you sure you want to cancel [ProductName] installation?")
    cancel.control("Icon", "Icon", 15, 15, 24, 24, 5242881, None,
                   "py.ico", None, None)
    c=cancel.pushbutton("Yes", 72, 57, 56, 17, 3, "Yes", "No")
    c.event("EndDialog", "Exit")
    
    c=cancel.pushbutton("No", 132, 57, 56, 17, 3, "No", "Yes")
    c.event("EndDialog", "Return")

    #####################################################################
    # Global "Wait for costing" dialog
    costing = Dialog(db, "WaitForCostingDlg", 50, 10, 260, 85, modal, title,
                     "Return", "Return", "Return")
    costing.text("Text", 48, 15, 194, 30, 3,
                 "Please wait while the installer finishes determining your disk space requirements.")
    costing.control("Icon", "Icon", 15, 15, 24, 24, 5242881, None,
                    "py.ico", None, None)
    c = costing.pushbutton("Return", 102, 57, 56, 17, 3, "Return", None)
    c.event("EndDialog", "Exit")

    #####################################################################
    # Preparation dialog: no user input except cancellation
    prep = PyDialog(db, "PrepareDlg", x, y, w, h, modeless, title,
                    "Cancel", "Cancel", "Cancel")
    prep.text("Description", 135, 70, 220, 40, 0x30003,
              "Please wait while the Installer prepares to guide you through the installation.")
    prep.title("Welcome to the [ProductName] Installer")
    c=prep.text("ActionText", 135, 110, 220, 20, 0x30003, "Pondering...")
    c.mapping("ActionText", "Text")
    c=prep.text("ActionData", 135, 135, 220, 30, 0x30003, None)
    c.mapping("ActionData", "Text")
    prep.back("Back", None, active=0)
    prep.next("Next", None, active=0)
    c=prep.cancel("Cancel", None)
    c.event("SpawnDialog", "CancelDlg")

    #####################################################################
    # Target directory selection
    seldlg = PyDialog(db, "SelectDirectoryDlg", x, y, w, h, modal, title,
                    "Next", "Next", "Cancel")
    seldlg.title("Select Destination Directory")
    seldlg.text("Description", 135, 50, 220, 40, 0x30003,
               "Please select a directory for the [ProductName] files.")

    seldlg.back("< Back", None, active=0)
    c = seldlg.next("Next >", "Cancel")
    c.event("DoAction", "CheckDir", "TargetExistsOk<>1", order=1)
    # If the target exists, but we found that we are going to remove old versions, don't bother
    # confirming that the target directory exists. Strictly speaking, we should determine that
    # the target directory is indeed the target of the product that we are going to remove, but
    # I don't know how to do that.
    c.event("SpawnDialog", "ExistingDirectoryDlg", 'TargetExists=1 and REMOVEOLDVERSION="" and REMOVEOLDSNAPSHOT=""', 2)
    c.event("SetTargetPath", "TARGETDIR", 'TargetExists=0 or REMOVEOLDVERSION<>"" or REMOVEOLDSNAPSHOT<>""', 3)
    c.event("SpawnWaitDialog", "WaitForCostingDlg", "CostingComplete=1", 4)
    c.event("NewDialog", "SelectFeaturesDlg", 'TargetExists=0 or REMOVEOLDVERSION<>"" or REMOVEOLDSNAPSHOT<>""', 5)

    c = seldlg.cancel("Cancel", "DirectoryCombo")
    c.event("SpawnDialog", "CancelDlg")

    seldlg.control("DirectoryCombo", "DirectoryCombo", 135, 70, 172, 80, 393219,
                   "TARGETDIR", None, "DirectoryList", None)
    seldlg.control("DirectoryList", "DirectoryList", 135, 90, 208, 136, 3, "TARGETDIR",
                   None, "PathEdit", None)
    seldlg.control("PathEdit", "PathEdit", 135, 230, 206, 16, 3, "TARGETDIR", None, "Next", None)
    c = seldlg.pushbutton("Up", 306, 70, 18, 18, 3, "Up", None)
    c.event("DirectoryListUp", "0")
    c = seldlg.pushbutton("NewDir", 324, 70, 30, 18, 3, "New", None)
    c.event("DirectoryListNew", "0")

    #####################################################################
    # SelectFeaturesDlg
    features = PyDialog(db, "SelectFeaturesDlg", x, y, w, h, modal|track_disk_space,
                        title, "Tree", "Next", "Cancel")
    features.title("Customize [ProductName]")
    features.text("Description", 135, 35, 220, 15, 0x30003,
                  "Select the way you want features to be installed.")
    features.text("Text", 135,45,220,30, 3,
                  "Click on the icons in the tree below to change the way features will be installed.")

    c=features.back("< Back", "Next")
    c.event("NewDialog", "SelectDirectoryDlg")

    c=features.next("Next >", "Cancel")
    c.mapping("SelectionNoItems", "Enabled")
    c.event("SpawnDialog", "DiskCostDlg", "OutOfDiskSpace=1", order=1)
    c.event("EndDialog", "Return", "OutOfDiskSpace<>1", order=2)

    c=features.cancel("Cancel", "Tree")
    c.event("SpawnDialog", "CancelDlg")

    # The browse property is not used, since we have only a single target path (selected already)    
    features.control("Tree", "SelectionTree", 135, 75, 220, 95, 7, "_BrowseProperty",
                     "Tree of selections", "Back", None)

    #c=features.pushbutton("Reset", 42, 243, 56, 17, 3, "Reset", "DiskCost")
    #c.mapping("SelectionNoItems", "Enabled")
    #c.event("Reset", "0")
    
    features.control("Box", "GroupBox", 135, 170, 225, 90, 1, None, None, None, None)

    c=features.xbutton("DiskCost", "Disk &Usage", None, 0.10)
    c.mapping("SelectionNoItems","Enabled")
    c.event("SpawnDialog", "DiskCostDlg")

    c=features.xbutton("Advanced", "Advanced", None, 0.30)
    c.event("SpawnDialog", "AdvancedDlg")

    c=features.text("ItemDescription", 140, 180, 210, 30, 3,
                  "Multiline description of the currently selected item.")
    c.mapping("SelectionDescription","Text")
    
    c=features.text("ItemSize", 140, 210, 210, 45, 3,
                    "The size of the currently selected item.")
    c.mapping("SelectionSize", "Text")

    #####################################################################
    # Disk cost
    cost = PyDialog(db, "DiskCostDlg", x, y, w, h, modal, title,
                    "OK", "OK", "OK", bitmap=False)
    cost.text("Title", 15, 6, 200, 15, 0x30003,
              "{\DlgFontBold8}Disk Space Requirements")
    cost.text("Description", 20, 20, 280, 20, 0x30003,
              "The disk space required for the installation of the selected features.")
    cost.text("Text", 20, 53, 330, 60, 3,
              "The highlighted volumes (if any) do not have enough disk space "
              "available for the currently selected features.  You can either "
              "remove some files from the highlighted volumes, or choose to "
              "install less features onto local drive(s), or select different "
              "destination drive(s).")
    cost.control("VolumeList", "VolumeCostList", 20, 100, 330, 150, 393223,
                 None, "{120}{70}{70}{70}{70}", None, None)
    cost.xbutton("OK", "Ok", None, 0.5).event("EndDialog", "Return")

    #####################################################################
    # WhichUsers Dialog. Only available on NT, and for privileged users.
    # This must be run before FindRelatedProducts, because that will
    # take into account whether the previous installation was per-user
    # or per-machine. We currently don't support going back to this
    # dialog after "Next" was selected; to support this, we would need to
    # find how to reset the ALLUSERS property, and how to re-run
    # FindRelatedProducts.
    # On Windows9x, the ALLUSERS property is ignored on the command line
    # and in the Property table, but installer fails according to the documentation
    # if a dialog attempts to set ALLUSERS.
    whichusers = PyDialog(db, "WhichUsersDlg", x, y, w, h, modal, title,
                        "AdminInstall", "Next", "Cancel")
    whichusers.title("Select whether to install [ProductName] for all users of this computer.")
    # A radio group with two options: allusers, justme
    g = whichusers.radiogroup("AdminInstall", 135, 60, 160, 50, 3,
                              "WhichUsers", "", "Next")
    g.add("ALL", 0, 5, 150, 20, "Install for all users")
    g.add("JUSTME", 0, 25, 150, 20, "Install just for me")

    whichusers.back("Back", None, active=0)    

    c = whichusers.next("Next >", "Cancel")
    c.event("[ALLUSERS]", "1", 'WhichUsers="ALL"', 1)
    c.event("EndDialog", "Return", order = 2)

    c = whichusers.cancel("Cancel", "AdminInstall")
    c.event("SpawnDialog", "CancelDlg")
                        
    #####################################################################
    # Advanced Dialog.
    advanced = PyDialog(db, "AdvancedDlg", x, y, w, h, modal, title,
                        "CompilePyc", "Next", "Cancel")
    advanced.title("Advanced Options for [ProductName]")
    # A radio group with two options: allusers, justme
    advanced.checkbox("CompilePyc", 135, 60, 230, 50, 3,
                      "COMPILEALL", "Compile .py files to byte code after installation", "Next")

    c = advanced.next("Finish", "Cancel")
    c.event("EndDialog", "Return")

    c = advanced.cancel("Cancel", "CompilePyc")
    c.event("SpawnDialog", "CancelDlg")
                        
    #####################################################################
    # Existing Directory dialog 
    dlg = Dialog(db, "ExistingDirectoryDlg", 50, 30, 200, 80, modal, title,
                   "No", "No", "No")
    dlg.text("Title", 10, 20, 180, 40, 3,
             "[TARGETDIR] exists. Are you sure you want to overwrite existing files?")
    c=dlg.pushbutton("Yes", 30, 60, 55, 17, 3, "Yes", "No")
    c.event("[TargetExists]", "0", order=1)
    c.event("[TargetExistsOk]", "1", order=2)
    c.event("EndDialog", "Return", order=3)
    c=dlg.pushbutton("No", 115, 60, 55, 17, 3, "No", "Yes")
    c.event("EndDialog", "Return")

    #####################################################################
    # Installation Progress dialog (modeless)
    progress = PyDialog(db, "ProgressDlg", x, y, w, h, modeless, title,
                        "Cancel", "Cancel", "Cancel", bitmap=False)
    progress.text("Title", 20, 15, 200, 15, 0x30003,
                  "{\DlgFontBold8}[Progress1] [ProductName]")
    progress.text("Text", 35, 65, 300, 30, 3,
                  "Please wait while the Installer [Progress2] [ProductName]. "
                  "This may take several minutes.")
    progress.text("StatusLabel", 35, 100, 35, 20, 3, "Status:")

    c=progress.text("ActionText", 70, 100, w-70, 20, 3, "Pondering...")
    c.mapping("ActionText", "Text")

    #c=progress.text("ActionData", 35, 140, 300, 20, 3, None)
    #c.mapping("ActionData", "Text")

    c=progress.control("ProgressBar", "ProgressBar", 35, 120, 300, 10, 65537,
                       None, "Progress done", None, None)
    c.mapping("SetProgress", "Progress")

    progress.back("< Back", "Next", active=False)
    progress.next("Next >", "Cancel", active=False)
    progress.cancel("Cancel", "Back").event("SpawnDialog", "CancelDlg")

    # Maintenance type: repair/uninstall
    maint = PyDialog(db, "MaintenanceTypeDlg", x, y, w, h, modal, title,
                     "Next", "Next", "Cancel")
    maint.title("Welcome to the [ProductName] Setup Wizard")
    maint.text("BodyText", 135, 63, 230, 42, 3,
               "Select whether you want to repair or remove [ProductName].")
    g=maint.radiogroup("RepairRadioGroup", 135, 108, 230, 60, 3,
                        "MaintenanceForm_Action", "", "Next")
    g.add("Change", 0, 0, 200, 17, "&Change [ProductName]")
    g.add("Repair", 0, 18, 200, 17, "&Repair [ProductName]")
    g.add("Remove", 0, 36, 200, 17, "Re&move [ProductName]")
    
    maint.back("< Back", None, active=False)
    c=maint.next("Finish", "Cancel")
    # Change installation: Change progress dialog to "Change", then ask
    # for feature selection
    c.event("[Progress1]", "Change", 'MaintenanceForm_Action="Change"', 1)
    c.event("[Progress2]", "changes", 'MaintenanceForm_Action="Change"', 2)

    # Reinstall: Change progress dialog to "Repair", then invoke reinstall
    # Also set list of reinstalled features to "ALL"
    c.event("[REINSTALL]", "ALL", 'MaintenanceForm_Action="Repair"', 5)
    c.event("[Progress1]", "Repairing", 'MaintenanceForm_Action="Repair"', 6)
    c.event("[Progress2]", "repaires", 'MaintenanceForm_Action="Repair"', 7)
    c.event("Reinstall", "ALL", 'MaintenanceForm_Action="Repair"', 8)

    # Uninstall: Change progress to "Remove", then invoke uninstall
    # Also set list of removed features to "ALL"
    c.event("[REMOVE]", "ALL", 'MaintenanceForm_Action="Remove"', 11)
    c.event("[Progress1]", "Removing", 'MaintenanceForm_Action="Remove"', 12)
    c.event("[Progress2]", "removes", 'MaintenanceForm_Action="Remove"', 13)
    c.event("Remove", "ALL", 'MaintenanceForm_Action="Remove"', 14)

    # Close dialog when maintenance action scheduled    
    c.event("EndDialog", "Return", 'MaintenanceForm_Action<>"Change"', 20)
    c.event("NewDialog", "SelectFeaturesDlg", 'MaintenanceForm_Action="Change"', 21)
            
    maint.cancel("Cancel", "RepairRadioGroup").event("SpawnDialog", "CancelDlg")
    

# See "Feature Table". The feature level is 1 for all features,
# and the feature attributes are 0 for the DefaultFeature, and
# FollowParent for all other features. The numbers are the Display
# column.
def add_features(db):
    # feature attributes:
    # msidbFeatureAttributesFollowParent == 2
    # msidbFeatureAttributesDisallowAdvertise == 8
    # Features that need to be installed with together with the main feature
    # (i.e. additional Python libraries) need to follow the parent feature.
    # Features that have no advertisement trigger (e.g. the test suite)
    # must not support advertisement
    global default_feature, tcltk, htmlfiles, tools, testsuite, ext_feature
    default_feature = Feature(db, "DefaultFeature", "Python",
                              "Python Interpreter and Libraries",
                              1, directory = "TARGETDIR")
    # The extensions feature is tricky wrt. advertisement and follow parent.
    # The following combinations must be supported:
    # default feature         extensions                       effect on extensions
    # locally/from source     locally/from source              registered
    # advertised              advertised/locally/from source   advertised
    # locally/from source     not installed                    not installed
    # advertised              not installed                    not advertised
    #                                                          (only shortcuts are)
    # The following combination might be considered meaningless, but cannot be excluded
    # locally/from source     advertised                       registered
    ext_feature = Feature(db, "Extensions", "Register Extensions",
                          "Make this Python installation the default Python installation", 3,
                         parent = default_feature)
    tcltk = Feature(db, "TclTk", "Tcl/Tk", "Tkinter, IDLE, pydoc", 5,
                    parent = default_feature, attributes=2)
    htmlfiles = Feature(db, "Documentation", "Documentation",
                        "Python HTMLHelp File", 7, parent = default_feature)
    tools = Feature(db, "Tools", "Utility Scripts",
                    "Python utility scripts (Tools/", 9, 
                    parent = default_feature, attributes=2)
    testsuite = Feature(db, "Testsuite", "Test suite",
                        "Python test suite (Lib/test/)", 11,
                        parent = default_feature, attributes=2|8)
    

def extract_msvcr71():
    import _winreg
    # Find the location of the merge modules
    k = _winreg.OpenKey(
        _winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\VisualStudio\7.1\Setup\VS")
    dir = _winreg.QueryValueEx(k, "MSMDir")[0]
    _winreg.CloseKey(k)
    files = glob.glob1(dir, "*CRT71*")
    assert len(files) == 1
    file = os.path.join(dir, files[0])
    # Extract msvcr71.dll
    m = msilib.MakeMerge2()
    m.OpenModule(file, 0)
    m.ExtractFiles(".")
    m.CloseModule()
    # Find the version/language of msvcr71.dll
    installer = msilib.MakeInstaller()
    return installer.FileVersion("msvcr71.dll", 0), \
           installer.FileVersion("msvcr71.dll", 1)

class PyDirectory(Directory):
    """By default, all components in the Python installer
    can run from source."""
    def __init__(self, *args, **kw):
        if not kw.has_key("componentflags"):
            kw['componentflags'] = 2 #msidbComponentAttributesOptional
        Directory.__init__(self, *args, **kw)

# See "File Table", "Component Table", "Directory Table",
# "FeatureComponents Table"
def add_files(db):
    cab = CAB("python")
    tmpfiles = []
    # Add all executables, icons, text files into the TARGETDIR component
    root = PyDirectory(db, cab, None, srcdir, "TARGETDIR", "SourceDir")
    default_feature.set_current()
    root.add_file("PCBuild/w9xpopen.exe")
    root.add_file("PC/py.ico")
    root.add_file("PC/pyc.ico")
    root.add_file("README.txt", src="README")
    root.add_file("NEWS.txt", src="Misc/NEWS")
    root.add_file("LICENSE.txt", src="LICENSE")
    root.start_component("python.exe", keyfile="python.exe")
    root.add_file("PCBuild/python.exe")
    root.start_component("pythonw.exe", keyfile="pythonw.exe")
    root.add_file("PCBuild/pythonw.exe")

    # msidbComponentAttributesSharedDllRefCount = 8, see "Component Table"
    dlldir = PyDirectory(db, cab, root, srcdir, "DLLDIR", ".")
    pydll = "python%s%s.dll" % (major, minor)
    pydllsrc = srcdir + "/PCBuild/" + pydll
    dlldir.start_component("DLLDIR", flags = 8, keyfile = pydll)
    installer = msilib.MakeInstaller()
    pyversion = installer.FileVersion(pydllsrc, 0)
    if not snapshot:
        # For releases, the Python DLL has the same version as the
        # installer package.
        assert pyversion.split(".")[:3] == current_version.split(".")
    dlldir.add_file("PCBuild/python%s%s.dll" % (major, minor),
                    version=pyversion,
                    language=installer.FileVersion(pydllsrc, 1))
    # XXX determine dependencies
    version, lang = extract_msvcr71()
    dlldir.start_component("msvcr71", flags=8, keyfile="msvcr71.dll")
    dlldir.add_file("msvcr71.dll", src=os.path.abspath("msvcr71.dll"),
                    version=version, language=lang)
    tmpfiles.append("msvcr71.dll")
    
    # Add all .py files in Lib, except lib-tk, test
    dirs={}
    pydirs = [(root,"Lib")]
    while pydirs:
        parent, dir = pydirs.pop()
        if dir == "CVS" or dir.startswith("plat-"):
            continue
        elif dir in ["lib-tk", "idlelib", "Icons"]:
            tcltk.set_current()
        elif dir in ['test', 'output']:
            testsuite.set_current()
        else:
            default_feature.set_current()
        lib = PyDirectory(db, cab, parent, dir, dir, "%s|%s" % (parent.make_short(dir), dir))
        # Add additional files
        dirs[dir]=lib
        lib.glob("*.txt")
        if dir=='site-packages':
            continue
        files = lib.glob("*.py")
        files += lib.glob("*.pyw")
        if files:
            # Add an entry to the RemoveFile table to remove bytecode files.
            lib.remove_pyc()
        if dir=='test' and parent.physical=='Lib':
            lib.add_file("185test.db")
            lib.add_file("audiotest.au")
            lib.add_file("cfgparser.1")
            lib.add_file("test.xml")
            lib.add_file("test.xml.out")
            lib.add_file("testtar.tar")
            lib.glob("*.uue")
            lib.add_file("readme.txt", src="README")
        if dir=='decimaltestdata':
            lib.glob("*.decTest")
        if dir=='output':
            lib.glob("test_*")
        if dir=='idlelib':
            lib.glob("*.def")
            lib.add_file("idle.bat")
        if dir=="Icons":
            lib.glob("*.gif")
            lib.add_file("idle.icns")
        if dir=="command":
            lib.add_file("wininst-6.exe")
            lib.add_file("wininst-7.1.exe")
        if dir=="data" and parent.physical=="test" and parent.basedir.physical=="email":
            # This should contain all non-CVS files listed in CVS
            for f in os.listdir(lib.absolute):
                if f.endswith(".txt") or f=="CVS":continue
                if f.endswith(".au") or f.endswith(".gif"):
                    lib.add_file(f)
                else:
                    print "WARNING: New file %s in email/test/data" % f
        for f in os.listdir(lib.absolute):
            if os.path.isdir(os.path.join(lib.absolute, f)):
                pydirs.append((lib, f))
    # Add DLLs
    default_feature.set_current()
    lib = PyDirectory(db, cab, root, srcdir+"/PCBuild", "DLLs", "DLLS|DLLs")
    dlls = []
    tclfiles = []
    for f in extensions:
        if f=="_tkinter.pyd":
            continue
        if not os.path.exists(srcdir+"/PCBuild/"+f):
            print "WARNING: Missing extension", f
            continue
        dlls.append(f)
        lib.add_file(f)
    if not os.path.exists(srcdir+"/PCBuild/_tkinter.pyd"):
        print "WARNING: Missing _tkinter.pyd"
    else:
        lib.start_component("TkDLLs", tcltk)
        lib.add_file("_tkinter.pyd")
        dlls.append("_tkinter.pyd")
        tcldir = os.path.normpath(srcdir+"/../tcl84/bin")
        for f in glob.glob1(tcldir, "*.dll"):
            lib.add_file(f, src=os.path.join(tcldir, f))
    # check whether there are any unknown extensions
    for f in glob.glob1(srcdir+"/PCBuild", "*.pyd"):
        if f.endswith("_d.pyd"): continue # debug version
        if f in dlls: continue
        print "WARNING: Unknown extension", f
    
    # Add headers
    default_feature.set_current()
    lib = PyDirectory(db, cab, root, "include", "include", "INCLUDE|include")
    lib.glob("*.h")
    lib.add_file("pyconfig.h", src="../PC/pyconfig.h")
    # Add import libraries
    lib = PyDirectory(db, cab, root, "PCBuild", "libs", "LIBS|libs")
    for f in dlls:
        lib.add_file(f.replace('pyd','lib'))
    lib.add_file('python%s%s.lib' % (major, minor))
    # Add Tcl/Tk
    tcldirs = [(root, '../tcl84/lib', 'tcl')]
    tcltk.set_current()
    while tcldirs:
        parent, phys, dir = tcldirs.pop()
        lib = PyDirectory(db, cab, parent, phys, dir, "%s|%s" % (parent.make_short(dir), dir))
        if not os.path.exists(lib.absolute):
            continue
        for f in os.listdir(lib.absolute):
            if os.path.isdir(os.path.join(lib.absolute, f)):
                tcldirs.append((lib, f, f))
            else:
                lib.add_file(f)
    # Add tools
    tools.set_current()
    tooldir = PyDirectory(db, cab, root, "Tools", "Tools", "TOOLS|Tools")
    for f in ['i18n', 'pynche', 'Scripts', 'versioncheck', 'webchecker']:
        lib = PyDirectory(db, cab, tooldir, f, f, "%s|%s" % (tooldir.make_short(f), f))
        lib.glob("*.py")
        lib.glob("*.pyw", exclude=['pydocgui.pyw'])
        lib.remove_pyc()
        lib.glob("*.txt")
        if f == "pynche":
            x = PyDirectory(db, cab, lib, "X", "X", "X|X")
            x.glob("*.txt")
        if f == 'Scripts':
            lib.add_file("README.txt", src="README")
            lib.start_component("pydocgui.pyw", tcltk, keyfile="pydocgui.pyw")
            lib.add_file("pydocgui.pyw")
    # Add documentation
    htmlfiles.set_current()
    lib = PyDirectory(db, cab, root, "Doc", "Doc", "DOC|Doc")
    lib.start_component("documentation", keyfile="Python%s%s.chm" % (major,minor))
    lib.add_file("Python%s%s.chm" % (major, minor))

    cab.commit(db)

    for f in tmpfiles:
        os.unlink(f)

# See "Registry Table", "Component Table"
def add_registry(db):
    # File extensions, associated with the REGISTRY.def component
    # IDLE verbs depend on the tcltk feature.
    # msidbComponentAttributesRegistryKeyPath = 4
    # -1 for Root specifies "dependent on ALLUSERS property"
    add_data(db, "Component",
             # msidbComponentAttributesRegistryKeyPath = 4
             [("REGISTRY", msilib.gen_uuid(), "TARGETDIR", 4, None,
               "InstallPath"),
              ("REGISTRY.def", msilib.gen_uuid(), "TARGETDIR", 4,
               None, None),
              ("REGISTRY.tcl", msilib.gen_uuid(), "TARGETDIR", 4,
               "&%s <> 2" % ext_feature.id, "py.IDLE")])
    # See "FeatureComponents Table".
    # The association between TclTk and pythonw.exe is necessary to make ICE59
    # happy, because the installer otherwise believes that the IDLE and PyDoc
    # shortcuts might get installed without pythonw.exe being install. This
    # is not true, since installing TclTk will install the default feature, which
    # will cause pythonw.exe to be installed.
    add_data(db, "FeatureComponents",
             [(default_feature.id, "REGISTRY"),
              (ext_feature.id, "REGISTRY.def"),
              (tcltk.id, "REGISTRY.tcl"),
              (tcltk.id, "pythonw.exe")])

    pat = r"Software\Classes\%sPython.%sFile\shell\%s\command"
    ewi = "Edit with IDLE"
    pat2 = r"Software\Classes\%sPython.%sFile\DefaultIcon"
    pat3 = r"Software\Classes\%sPython.%sFile"
    # Advertised extensions
    add_data(db, "Extension",
            [("py", "python.exe", "Python.File", None, default_feature.id),
            ("pyw", "pythonw.exe", "Python.NoConFile", None, default_feature.id),
            ("pyc", "python.exe", "Python.CompiledFile", None, default_feature.id),
            ("pyo", "python.exe", "Python.CompiledFile", None, default_feature.id)])
    # add_data(db, "MIME") XXX
    add_data(db, "Verb",
            [("py", "open", 1, None, r'-n -e "%1"'),
            ("pyw", "open", 1, None, r'-n -e "%1"'),
            ("pyc", "open", 1, None, r'-n -e "%1"'),
            ("pyo", "open", 1, None, r'-n -e "%1"')])
    add_data(db, "ProgId",
            [("Python.File", None, None, "Python File", "python_icon.exe", 0),
             ("Python.NoConFile", None, None, "Python File (no console)", "python_icon.exe", 0),
             ("Python.CompiledFile", None, None, "Compiled Python File", "python_icon.exe", 1)])
    
    # Non-advertised verbs: for advertised verbs, we would need to invoke the same
    # executable for both open and "Edit with IDLE". This cannot work, as we want
    # to use pythonw.exe in either case
    add_data(db, "Registry",
            [#Verbs
             ("py.IDLE", -1, pat % (testprefix, "", ewi), "",
              r'"[TARGETDIR]pythonw.exe" "[TARGETDIR]Lib\idlelib\idle.pyw" -n -e "%1"',
              "REGISTRY.tcl"),
             ("pyw.IDLE", -1, pat % (testprefix, "NoCon", ewi), "",
              r'"[TARGETDIR]pythonw.exe" "[TARGETDIR]Lib\idlelib\idle.pyw" -n -e "%1"',
              "REGISTRY.tcl"),
            ])
    
    # Registry keys
    prefix = r"Software\%sPython\PythonCore\%s" % (testprefix, short_version)
    add_data(db, "Registry",
             [("InstallPath", -1, prefix+r"\InstallPath", "", "[TARGETDIR]", "REGISTRY"),
              ("InstallGroup", -1, prefix+r"\InstallPath\InstallGroup", "",
               "Python %s" % short_version, "REGISTRY"),
              ("PythonPath", -1, prefix+r"\PythonPath", "",
               "[TARGETDIR]Lib;[TARGETDIR]DLLs;[TARGETDIR]lib-tk", "REGISTRY"),
              ("Documentation", -1, prefix+r"\Help\Main Python Documentation", "",
               r"[TARGETDIR]Doc\Python%s%s.chm" % (major, minor), "REGISTRY"),
              ("Modules", -1, prefix+r"\Modules", "+", None, "REGISTRY"),
              ("AppPaths", -1, r"Software\Microsoft\Windows\CurrentVersion\App Paths\Python.exe",
               "", r"[TARGETDIR]Python.exe", "REGISTRY.def")
              ])
    # Shortcuts, see "Shortcut Table"
    add_data(db, "Directory",
             [("ProgramMenuFolder", "TARGETDIR", "."),
              ("MenuDir", "ProgramMenuFolder", "PY%s%s|%sPython %s.%s" % (major,minor,testprefix,major,minor))])
    add_data(db, "RemoveFile",
             [("MenuDir", "TARGETDIR", None, "MenuDir", 2)])
    add_data(db, "Shortcut",
             [# Advertised shortcuts: targets are features, not files
              ("IDLE", "MenuDir", "IDLE|IDLE (Python GUI)", "pythonw.exe",
               tcltk.id, r"[TARGETDIR]Lib\idlelib\idle.pyw", None, None, "python_icon.exe", 0, None, "TARGETDIR"),
              ("PyDoc", "MenuDir", "MODDOCS|Module Docs", "pythonw.exe",
               tcltk.id, r"[TARGETDIR]Tools\scripts\pydocgui.pyw", None, None, "python_icon.exe", 0, None, "TARGETDIR"),
              ("Python", "MenuDir", "PYTHON|Python (command line)", "python.exe",
               default_feature.id, None, None, None, "python_icon.exe", 2, None, "TARGETDIR"),
              ("Manual", "MenuDir", "MANUAL|Python Manuals", "documentation",
               htmlfiles.id, None, None, None, None, None, None, None),
              ## Non-advertised shortcuts: must be associated with a registry component
              ("Uninstall", "MenuDir", "UNINST|Uninstall Python", "REGISTRY",
               SystemFolderName+"msiexec",  "/x%s" % product_code,
               None, None, None, None, None, None),
              ])
    db.Commit()

db = build_database()
try:
    add_features(db)
    add_ui(db)
    add_files(db)
    add_registry(db)
    remove_old_versions(db)
    db.Commit()
finally:
    del db
