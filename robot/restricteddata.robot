*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.

Library           SeleniumLibrary
Library           CkanLibrary.py  admin_username=${ADMIN_USERNAME}  admin_password=${ADMIN_PASSWORD}

*** Variables ***
${SERVER}          localhost
${ROOT_URL}        http://${SERVER}
${BROWSER}         headlesschrome
${DELAY}           0
${ADMIN_USERNAME}  admin
${ADMIN_PASSWORD}  administrator
${TEST_USER_USERNAME}  test-user
${TEST_USER_PASSWORD}  test-user
${LOGIN URL}       ${ROOT_URL}/user/login
${DASHBOARD URL}   ${ROOT_URL}/dashboard/datasets
${INDEX URL}       ${ROOT_URL}/

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

Go To Front Page
    Go To    ${INDEX URL}
    Front Page Should Be Open

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

URL Path Should be
    [Arguments]    ${path}
    Location Should Be  ${ROOT_URL}${path}

Open URL Path
    [Arguments]    ${path}
    Go To  ${ROOT_URL}${path}

Input Username
    [Arguments]    ${username}
    Input Text    id:field-login    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    id:field-password  ${password}

Submit Primary Form
    Scroll Element Into View   css:.primary form button[type=submit]
    Click Button   css:.primary form button.btn-primary[type=submit]

Log In As Administrator
    Go To Login Page
    Input Username  ${ADMIN_USERNAME}
    Input Password  ${ADMIN_PASSWORD}
    Submit Primary Form
    URL Path Should Be  /dashboard/datasets

Create Test User
    Create CKAN User  ${TEST_USER_USERNAME}  ${TEST_USER_USERNAME}@example.com  ${TEST_USER_PASSWORD}

Log In As Test User
    Go To Login Page
    Input Username  ${TEST_USER_USERNAME}
    Input Password  ${TEST_USER_PASSWORD}
    Submit Primary Form
    URL Path Should Be  /dashboard/datasets
    
Log Out
    Open URL Path  /user/_logout
    URL Path Should Be  /user/logged_out_redirect
    Page Should Contain  Kirjaudu sisään
    Delete All Cookies

Dashboard Page Should Be Open
    Location Should Be    ${DASHBOARD URL}

Open Browser To Front Page
    Open Chromium
    Front Page Should Be Open

Front Page Should Be Open
    Location Should Be  ${INDEX URL}
    Title Should Be  Tervetuloa - Suojattudata

Dataset List Should Be Open
    Title Should Be  Tietoaineisto - Suojattudata
    URL Path Should Be  /dataset/


Reset Data And Open Front Page
    Reset CKAN
    Open Browser To Front Page


Create Test Organisation
    Log In As Administrator
    Go To  ${ROOT_URL}/organization/
    Click Link  link:Lisää organisaatio
    Input Text  id:field-title_translated-fi  Testiorganisaatio
    Input Text  id:field-title_translated-sv  Test organisation
    Submit Primary Form
    URL Path Should Be  /organization/testiorganisaatio

Add Test User To Test Organisation
    Open URL Path  /organization/members/testiorganisaatio
    Click Link  link:Lisää jäsen
    Input Text Into Select2  username  ${TEST_USER_USERNAME}
    Submit Primary Form
    Log Out
    

Input Text Into CKEditor
    [Arguments]  ${id}  ${text}
    Wait Until Page Contains Element  id:${id}
    Scroll Element Into View  css:#${id} + .ck-editor .ck-editor__editable
    Click Element  css:#${id} + .ck-editor .ck-editor__editable
    Press Keys     None  ${text}
    
Input Tag Into Select2
    [Arguments]  ${id}  ${text}
    Wait Until Page Contains Element  id:s2id_${id}
    Scroll Element Into View  id:s2id_${id}
    Click Element  id:s2id_${id}
    Press Keys     None  ${text}
    Wait Until Element Is Visible  css:.select2-result-label[data-value="${text}"]
    Press Keys     None  \n
    Element Should Be Visible  css:[data-container-id="${id}"][data-tag-id="${text}"]

Input Text Into Select2
    [Arguments]  ${id}  ${text}
    Wait Until Page Contains Element  id:s2id_${id}
    Scroll Element Into View  id:s2id_${id}
    Click Element  id:s2id_${id}
    Press Keys     None  ${text}
    Wait Until Element Is Visible  css:.select2-result-label[data-value="${text}"]
    Press Keys     None  \n
    Textfield Value Should Be  name:${id}  ${text}

Select Suomi.fi Radio Button
    [Arguments]  ${name}  ${value}
    Scroll Element Into View  css:#field-${name}-${value} + .check
    Click Element  css:#field-${name}-${value} + .check

Select Suomi.fi Checkbox
    [Arguments]  ${name}  ${value}
    Scroll Element Into View  css:#field-${name}-${value} + .custom-checkbox
    Click Element  css:#field-${name}-${value} + .custom-checkbox

Remove Suomi.fi Tag
    [Arguments]  ${name}  ${language}  ${value}
    Scroll Element Into View  css:[data-container-id=field-${name}-${language}][data-tag-id=${value}] i
    Click Element  css:[data-container-id=field-${name}-${language}][data-tag-id=${value}] i

Fill Dataset Form With Minimal Test Data
    Input Text  id:field-title_translated-fi  Testiaineisto
    Input Text  id:field-title_translated-sv  Test dataset
    Input Text Into CKEditor  field-notes_translated-fi  Testiaineiston kuvaus
    Input Text Into CKEditor  field-notes_translated-sv  Test dataset beskrivning
    Input Tag Into Select2   field-keywords-fi  Testi
    Input Tag Into Select2   field-keywords-sv  Test
    Input Text  id:field-maintainer  Teemu Testaaja
    Input Text  id:field-maintainer_email  teemu.testaaja@example.com

Fill Dataset Form With Full Test Data
    Fill Dataset Form With Minimal Test Data
    Input Text  id:field-title_translated-en  Test dataset
    Input Text Into CKEditor  field-notes_translated-en  Test dataset description
    Input Tag Into Select2   field-keywords-en  Test
    Input Text Into CKEditor  field-rights_translated-fi  Testiaineiston käyttöoikeudet
    Input Text Into CKEditor  field-rights_translated-sv  Test dataset behörigheter
    Input Text Into CKEditor  field-rights_translated-en  Test dataset rights
    Input Text  id:field-external_urls  https://example.com/2
    Scroll Element Into View  css:label[for="field-external_urls"] + .controls button
    Click Button  Lisää linkki
    Input Text  css:[name=external_urls]:not(#field-external_urls)  https://example.com
    Select From List By Value  id:field-update_frequency  annual
    Input Text  id:field-valid_from  01/01/2023
    Input Text  id:field-valid_till  01/01/2033
    Scroll Element Into View  css:label[for="field-maintainer_email"] + .controls button
    Click Button  Lisää sähköposti
    Input Text  css:[name=maintainer_email]:not(#field-maintainer_email)  teuvo.testaaja@example.com
    Input Text  id:field-maintainer_website  https://example.com/maintenance
    

Fill Resource Form With Minimal Test Data
    Input Text  id:field-name_translated-fi  Testiresurssi
    Input Text  id:field-name_translated-sv  Test resurs
    Click Button  id:resource-link-button
    Input Text  id:field-resource-url  http://example.com
    Input Tag Into Select2  field-format  HTML
    Input Text  id:field-size  12345
    Input Text Into CKEditor  field-rights_translated-fi  Testiresurssin käyttöoikeuksien kuvaus
    Input Text Into CKEditor  field-rights_translated-sv  Test resurs användningsrättigheter

Fill Resource Form With Full Test Data
    Fill Resource Form With Minimal Test Data
    Input Text  id:field-name_translated-en  Test resource
    Input Text Into CKEditor  field-description_translated-fi  Testiresurssin kuvaus
    Input Text Into CKEditor  field-description_translated-sv  Test resurs beskrivning
    Input Text Into CKEditor  field-description_translated-en  Test resource description
    Input Text Into CKEditor  field-rights_translated-en  Test resource rights
    Input Tag Into Select2   field-temporal_granularity-fi  Kuukausi
    Input Tag Into Select2   field-temporal_granularity-sv  Månad
    Input Tag Into Select2   field-temporal_granularity-en  Month
    Input Text  id:field-endpoint_url  http://example.com/api
    Input Text  id:field-position_info  WGS84
    Input Text  id:field-temporal_coverage_from  01/02/2023
    Input Text  id:field-temporal_coverage_till  03/04/2034
    Input Text  id:field-geographical_accuracy  42
    
