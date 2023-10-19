set mypath=%cd%
echo %mypath% tools\PKG_Sample
start /WAIT tools\QuickBMS\quickbms.exe  -G -d "tools\PKG\PKG.bms" tools/PKG/PKG_Sample/{}.pkg tools/PKG/PKG_Extract/
start %SystemRoot%\explorer.exe "%mypath%"