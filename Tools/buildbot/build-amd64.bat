@rem Used by the buildbot "compile" step.
cmd /c Tools\buildbot\external-amd64.bat
call "%VS90COMNTOOLS%\..\..\VC\vcvarsall.bat" x86_amd64
cmd /c Tools\buildbot\clean-amd64.bat
vcbuild PCbuild\pcbuild.sln "Debug|x64"
