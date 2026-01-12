@echo off
REM Change directory to the location of this batch file
cd /d "%~dp0"

REM Build a standalone executable. Not SDK needed.
dotnet publish -c Release -r win-x64 --self-contained true
@REM dotnet build -c Release