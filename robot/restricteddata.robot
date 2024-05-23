*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.

Library           SeleniumLibrary

*** Variables ***
${SERVER}          localhost
${BROWSER}         headlesschrome
${DELAY}           0
${LOGIN URL}       http://${SERVER}/user/login
${DASHBOARD URL}   http://${SERVER}/dashboard/datasets
${INDEX URL}       http://${SERVER}/

*** Keywords ***

# Helper for configuring chromium
Open Chromium
    ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
    Call Method  ${options}  add_argument  --disable-notifications
    Call Method  ${options}  add_argument  --disable-infobars
    Call Method  ${options}  add_argument  --disable-extensions
    Call Method  ${options}  add_argument  --no-sandbox
    Call Method  ${options}  add_argument  --headless\=new
    Call Method  ${options}  add_argument  --disable-dev-shm-usage
    Call Method  ${options}  add_argument  --remote-debugging-port\=9222
    Open Browser  ${INDEX URL}  Chrome  options=${options}
    Set Window Size    1920    1080

Close Chromium
    Close Browser

Open Browser To Login Page
    Open Chromium
    Go To  ${LOGIN URL}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Kirjaudu - Suojattudata

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    id:field-login    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    id:field-password  ${password}

Submit Credentials
    Click Button  class:btn-primary

Dashboard Page Should Be Open
    Location Should Be    ${DASHBOARD URL}

Open Browser To Front Page
    Open Chromium
    Front Page Should Be Open

Front Page Should Be Open
    Location Should Be  ${INDEX URL}
    Title Should Be  Tervetuloa - Suojattudata
