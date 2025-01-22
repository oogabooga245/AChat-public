prompt AChat-Relay: 
@echo off
setlocal enabledelayedexpansion
for /f "tokens=2 delims=: " %%A in ('nslookup myip.opendns.com. resolver1.opendns.com ^| find "Address" ^| findstr /R "[0-9]"') do (
    set "public_ip=%%A"
)
set "public_ip=!public_ip: =!"
cls
echo 0.0.0.0 = {!public_ip!}

python3 Relay.py
pause
cls
goto :1