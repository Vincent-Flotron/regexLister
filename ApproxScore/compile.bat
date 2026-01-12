
REM Build a standalone executable. Not SDK needed.
dotnet publish -c Release -r win-x64 --self-contained true
@REM dotnet build -c Release