@echo off
rem 一键生成并打开 Allure 报告（无需配置 PATH）
rem 用法：python -m pytest --alluredir=report/results 之后，运行本脚本
cd /d "%~dp0"

set ALLURE=C:\Users\admin\AppData\Roaming\npm\allure.cmd

"%ALLURE%" generate report/results -o report/html --clean
if errorlevel 1 goto :err
"%ALLURE%" open report/html
goto :eof

:err
echo.
echo 生成报告失败。先确认已经跑过：
echo   python -m pytest --alluredir=report/results
pause