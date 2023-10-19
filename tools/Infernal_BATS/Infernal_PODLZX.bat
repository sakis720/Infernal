set mypath=%cd%
echo %mypath% tools\PODLZX_Sample
start /WAIT tools\QuickBMS\quickbms.exe  -G -d "tools\PODLZX\PODLZX.bms" tools/PODLZX/PODLZX_Sample/{}.podlzx tools/PODLZX/PODLZX_POD/
start %SystemRoot%\explorer.exe "%mypath%"