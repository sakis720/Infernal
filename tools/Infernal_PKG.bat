set mypath=%cd%
echo %mypath% tools\PKG_Sample
start /WAIT tools\quickbms.exe  -G -d "tools\PKG.bms" tools/PKG_Sample/{}.pkg tools/PKG_Extract/
start %SystemRoot%\explorer.exe "%mypath%"