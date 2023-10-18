set mypath=%cd%
echo %mypath% tools\PODLZX_Sample
start /WAIT tools\quickbms.exe  -G -d "tools\PODLZX.bms" tools/PODLZX_Sample/{}.podlzx tools/PODLZX_POD/
start %SystemRoot%\explorer.exe "%mypath%"