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

Go To Organisation List
    Open URL Path  /organization

Go To Group List
    Open URL Path  /group

Go To Dataset List
    Open URL Path  /dataset

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
    Go To Front Page
    Click Link  link:KIRJAUDU ULOS
    URL Path Should Be  /user/logged_out_redirect
    Wait Until Page Contains  Kirjaudu sisään

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
    Create Organization  Testiorganisaatio  Test organisation  testiorganisaatio
    Open URL Path  /organization/testiorganisaatio
    Page Should Contain  Testiorganisaatio

Add Test User To Test Organisation
    Open URL Path  /organization/members/testiorganisaatio
    Click Link  link:Lisää jäsen
    Input Text Into Select2  username  ${TEST_USER_USERNAME}
    Submit Primary Form

Input Text Into CKEditor
    [Arguments]  ${id}  ${text}
    Wait Until Page Contains Element  css:#${id} + .ck-editor .ck-editor__editable
    Scroll Element Into View  css:#${id} + .ck-editor .ck-editor__editable
    Click Element  css:#${id} + .ck-editor .ck-editor__editable
    Press Keys     None  ${text}

Input Tag Into Select2
    [Arguments]  ${id}  ${text}
    Wait Until Page Contains Element  id:s2id_${id}
    Scroll Element Into View  id:s2id_${id}
    Click Element  id:s2id_${id}
    Press Keys     None  ${text}
    Wait Until Page Contains Element  css:.select2-result-label[data-value="${text}"]
    Press Keys     None  RETURN+ESCAPE
    Wait Until Element Is Not Visible  css:.select2-drop-mask
    Scroll Element Into View  css:[data-container-id="${id}"][data-tag-id="${text}"]
    Element Should Be Visible  css:[data-container-id="${id}"][data-tag-id="${text}"]

Input Text Into Select2
    [Arguments]  ${id}  ${text}
    Wait Until Page Contains Element  id:s2id_${id}
    Scroll Element Into View  id:s2id_${id}
    Click Element  id:s2id_${id}
    Press Keys     None  ${text}
    Wait Until Page Contains Element  css:.select2-result-label[data-value="${text}"]
    Scroll Element Into View  css:.select2-result-label[data-value="${text}"]
    Press Keys     None  RETURN+ESCAPE
    Wait Until Element Is Not Visible  id:select2-drop-mask
    Textfield Value Should Be  name:${id}  ${text}

Wait Until URL Slug Input Is Not Visible
    Wait Until Element Is Not Visible  css:input[data-module=slug-preview-slug]

Select Suomi.fi Radio Button
    [Arguments]  ${name}  ${value}
    Scroll Element Into View  css:#field-${name}-${value} + .check
    Click Element  css:#field-${name}-${value} + .check

Select Suomi.fi Checkbox
    [Arguments]  ${name}  ${value}=
    IF  len($value) > 0
        Scroll Element Into View  css:#field-${name}-${value} + .custom-checkbox
        Click Element  css:#field-${name}-${value} + .custom-checkbox
    ELSE
        Scroll Element Into View  css:#field-${name} + .custom-checkbox
        Click Element  css:#field-${name} + .custom-checkbox
    END

Remove Suomi.fi Tag
    [Arguments]  ${name}  ${language}  ${value}
    Scroll Element Into View  css:[data-container-id=field-${name}-${language}][data-tag-id=${value}] i
    Click Element  css:[data-container-id=field-${name}-${language}][data-tag-id=${value}] i

Scroll To Form Actions
    Wait Until Element Is Visible  css:.form-actions
    Scroll Element Into View  css:.form-actions

Click Suomi.fi Dialog Button
    [Arguments]  ${locator}
    Wait Until Element Is Visible  css:.modal .btn-primary
    Click Button  ${locator}

Fill Organisation Form With Full Test Data
    [Arguments]  ${description fi}=Testiorganisaation kuvaus
    ...          ${description sv}=Test organisation beskrivning
    ...          ${description en}=Test organisation description
    ...          ${vat number}=1234567-0
    ...          ${homepage}=http://example.com
    ...          ${image url}=http://localhost/test-image-url.png
    Wait Until URL Slug Input Is Not Visible
    Input Text Into CKEditor  field-description_translated-fi  ${description fi}
    Input Text Into CKEditor  field-description_translated-sv  ${description sv}
    Input Text Into CKEditor  field-description_translated-en  ${description en}
    Input Text  id:field-vat_number  ${vat number}
    Input Text  id:field-homepage  ${homepage}
    Input Text  id:field-image-url  ${image url}

Fill Dataset Form With Minimal Test Data
    [Arguments]  ${title fi}=Testiaineisto
    ...          ${title sv}=Test dataset
    ...          ${notes fi}=Testiaineiston kuvaus
    ...          ${notes sv}=Test dataset beskrivning
    ...          ${keyword fi}=Testi
    ...          ${keyword sv}=Test
    ...          ${private}=False
    ...          ${highvalue}=False
    ...          ${highvalue category}=meteorological
    ...          ${access rights}=non-public
    ...          ${maintainer}=Teemu Testaaja
    ...          ${maintainer email}=teemu.testaaja@example.com
    Wait Until URL Slug Input Is Not Visible
    Input Text  id:field-title_translated-fi  ${title fi}
    Input Text  id:field-title_translated-sv  ${title sv}
    Input Text Into CKEditor  field-notes_translated-fi  ${notes fi}
    Input Text Into CKEditor  field-notes_translated-sv  ${notes sv}
    Input Tag Into Select2   field-keywords-fi  ${keyword fi}
    Input Tag Into Select2   field-keywords-sv  ${keyword sv}
    Select Suomi.fi Radio Button  private  ${private}
    Select Suomi.fi Radio Button  highvalue  ${highvalue}
    IF  ${highvalue}
        Select Suomi.fi Checkbox  highvalue_category  ${highvalue category}
    END
    Select Suomi.fi Radio Button  access_rights  ${access rights}
    Input Text  id:field-maintainer  ${maintainer}
    TRY
        Input Text  id:field-maintainer_email  ${maintainer email}
    EXCEPT
        Input Text  id:field-maintainer_email-1  ${maintainer email}
    END
Fill Dataset Form With Full Test Data
    [Arguments]  ${title fi}=Testiaineisto
    ...          ${title sv}=Test dataset
    ...          ${title en}=Test dataset
    ...          ${notes fi}=Testiaineiston kuvaus
    ...          ${notes sv}=Test dataset beskrivning
    ...          ${notes en}=Test dataset description
    ...          ${rights fi}=Testiaineiston käyttöoikeudet
    ...          ${rights sv}=Test dataset behörigheter
    ...          ${rights en}=Test dataset rights
    ...          ${keyword fi}=Testi
    ...          ${keyword sv}=Test
    ...          ${keyword en}=Test
    ...          ${private}=False
    ...          ${highvalue}=False
    ...          ${highvalue category}=meteorological
    ...          ${access rights}=non-public
    ...          ${external url}=https://example.com
    ...          ${second external url}=https://example.com/2
    ...          ${update frequency}=annual
    ...          ${valid from}=01/01/2023
    ...          ${valid till}=01/01/2033
    ...          ${maintainer}=Teemu Testaaja
    ...          ${maintainer email}=teemu.testaaja@example.com
    ...          ${second maintainer email}=teuvo.testaaja@example.com
    ...          ${maintenance website}=https://example.com/maintenance
    Fill Dataset Form With Minimal Test Data  title fi=${title fi}  title sv=${title sv}
    ...                                       notes fi=${notes fi}  notes sv=${notes sv}
    ...                                       keyword fi=${keyword fi}  keyword sv=${keyword sv}
    ...                                       private=${private}  highvalue=${highvalue}
    ...                                       highvalue category=${highvalue category}
    ...                                       access rights=${access rights}
    ...                                       maintainer=${maintainer}  maintainer email=${maintainer email}
    Input Text  id:field-title_translated-en  ${title en}
    Input Text Into CKEditor  field-notes_translated-en  ${notes en}
    Input Tag Into Select2   field-keywords-en  ${keyword en}
    Input Text Into CKEditor  field-rights_translated-fi  ${rights fi}
    Input Text Into CKEditor  field-rights_translated-sv  ${rights sv}
    Input Text Into CKEditor  field-rights_translated-en  ${rights en}
    Scroll Element Into View  css:label[for="field-external_urls"] + .controls > button
    TRY
        Input Text  id:field-external_urls-1  ${external url}
        Input Text  id:field-external_urls-2  ${second external url}
    EXCEPT
        Input Text  id:field-external_urls  ${external url}
        Click Button  Lisää linkki
        Input Text  css:[name=external_urls]:not(#field-external_urls)  ${second external url}
    END

    Select From List By Value  id:field-update_frequency  ${update frequency}
    Input Text  id:field-valid_from  ${valid from}
    Input Text  id:field-valid_till  ${valid till}

    Scroll Element Into View  css:label[for="field-maintainer_email"] + .controls > button
    TRY
        Input Text  id:field-maintainer_email-1  ${maintainer email}
        Input Text  id:field-maintainer_email-2  ${second maintainer_email}
    EXCEPT
        Input Text  id:field-maintainer_email  ${maintainer email}
        Click Button  Lisää sähköposti
        Input Text  css:[name=maintainer_email]:not(#field-maintainer_email)  ${second maintainer email}
    END

    Input Text  id:field-maintainer_website  ${maintenance website}

Fill Resource Form With Minimal Test Data
    [Arguments]  ${description fi}=Testiresurssin kuvaus
    ...          ${description sv}=Test resurs beskrivning
    ...          ${url}=https://example.com
    ...          ${format}=HTML
    ...          ${size}=12345
    ...          ${rights fi}=Testiresurssin käyttöoikeuksien kuvaus
    ...          ${rights sv}=Test resurs användningsrättigheter
    TRY
        Click Button  id:resource-link-button
    EXCEPT
        No Operation
    END
    Input Text  id:field-resource-url  ${url}
    Input Tag Into Select2  field-format  ${format}
    Input Text  id:field-size  ${size}
    Input Text Into CKEditor  field-rights_translated-fi  ${rights fi}
    Input Text Into CKEditor  field-rights_translated-sv  ${rights sv}

Fill Resource Form With Full Test Data
    [Arguments]  ${name fi}=Testiresurssi
    ...          ${name sv}=Test resurs
    ...          ${name en}=Test resource
    ...          ${description fi}=Testiresurssin kuvaus
    ...          ${description sv}=Test resurs beskrivning
    ...          ${description en}=Test resource description
    ...          ${url}=https://example.com
    ...          ${format}=HTML
    ...          ${size}=12345
    ...          ${rights fi}=Testiresurssin käyttöoikeudet
    ...          ${rights sv}=Test resurs behörigheter
    ...          ${rights en}=Test resource rights
    ...          ${temporal granularity fi}=Kuukausi
    ...          ${temporal granularity sv}=Månad
    ...          ${temporal granularity en}=Month
    ...          ${endpoint url}=https://example.com/2
    ...          ${position info}=WGS84
    ...          ${temporal coverage from}=01/02/2023
    ...          ${temporal coverage till}=03/04/2033
    ...          ${geographical accuracy}=42
    Fill Resource Form With Minimal Test Data  description fi=${description fi}  description sv=${description sv}
    ...                                        url=${url}  format=${format}  size=${size}
    ...                                        rights fi=${rights fi}  rights sv=${rights sv}
    Input Text  id:field-name_translated-fi  ${name fi}
    Input Text  id:field-name_translated-sv  ${name sv}
    Input Text  id:field-name_translated-en  Test resource
    Input Text Into CKEditor  field-description_translated-fi  ${description fi}
    Input Text Into CKEditor  field-description_translated-sv  ${description sv}
    Input Text Into CKEditor  field-description_translated-en  ${description en}
    Input Text Into CKEditor  field-rights_translated-en  ${rights en}
    Input Tag Into Select2   field-temporal_granularity-fi  ${temporal granularity fi}
    Input Tag Into Select2   field-temporal_granularity-sv  ${temporal granularity sv}
    Input Tag Into Select2   field-temporal_granularity-en  ${temporal granularity en}
    Input Text  id:field-endpoint_url  ${endpoint url}
    Input Text  id:field-position_info  ${position info}
    Input Text  id:field-temporal_coverage_from  ${temporal coverage from}
    Input Text  id:field-temporal_coverage_till  ${temporal coverage till}
    Input Text  id:field-geographical_accuracy  ${geographical accuracy}

Fill Group Form With Minimal Test Data
    [Arguments]  ${title fi}=Testikategoria
    ...          ${title sv}=Test kategori
    Wait Until URL Slug Input Is Not Visible
    Input Text  id:field-title_translated-fi  ${title fi}
    Input Text  id:field-title_translated-sv  ${title sv}

Fill Group Form With Full Test Data
    [Arguments]  ${title fi}=Testikategoria
    ...          ${title sv}=Test kategori
    ...          ${title en}=Test category
    ...          ${description fi}=Testikategorian kuvaus
    ...          ${description sv}=Test kategori beskrivning
    ...          ${description en}=Test category description
    ...          ${image url}=http://localhost/test-image-url.png
    Fill Group Form With Minimal Test Data  title fi=${title fi}  title sv=${title sv}
    Input Text  id:field-title_translated-en  ${title en}
    Input Text Into CKEditor  field-description_translated-fi  ${description fi}
    Input Text Into CKEditor  field-description_translated-sv  ${description sv}
    Input Text Into CKEditor  field-description_translated-en  ${description en}
    Input Text  id:field-image-url  ${image url}
