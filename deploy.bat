@echo off
REM Fission Core - One-Click Deploy Script (Windows)
REM Usage: deploy.bat <function-name> <github-url> [entrypoint]

set FUNCTION_NAME=%1
set GITHUB_URL=%2
set ENTRY_POINT=%3
if "%ENTRY_POINT%"=="" set ENTRY_POINT=server.js

if "%FUNCTION_NAME%"=="" (
    echo ❌ Usage: deploy.bat ^<function-name^> ^<github-url^> [entrypoint]
    echo 📝 Example: deploy.bat my-api https://github.com/user/repo
    exit /b 1
)

if "%GITHUB_URL%"=="" (
    echo ❌ Usage: deploy.bat ^<function-name^> ^<github-url^> [entrypoint]
    echo 📝 Example: deploy.bat my-api https://github.com/user/repo
    exit /b 1
)

echo 🚀 Deploying %FUNCTION_NAME% from %GITHUB_URL%...

REM Delete existing function if exists
echo 🗑️  Cleaning up existing function...
fission function delete --name %FUNCTION_NAME% 2>nul

REM Create function
echo 📦 Creating function...
fission function create --name %FUNCTION_NAME% --env nodejs --sourcearchive %GITHUB_URL%/archive/main.zip --entrypoint express-wrapper.js

REM Create HTTP trigger
echo 🌐 Creating HTTP trigger...
fission route create --name %FUNCTION_NAME%-route --function %FUNCTION_NAME% --url /%FUNCTION_NAME% --method GET

echo ✅ Deploy completed!
echo 🔗 API URL: http://localhost:8080/%FUNCTION_NAME%
echo 📊 Check status: kubectl get functions -n default
