*** Settings ***
Documentation     A distribution test suite.
Resource          ../restricteddata.robot
Test Setup        Distribution Test Setup
Test Teardown     Close Chromium

*** Test Cases ***
Create Distribution With All Fields
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Full Test Data
    Submit Primary Form

    URL Path Should Be  /dataset/testiaineisto
    Click Link  Testiresurssi
    
    Page Should Contain  Testiresurssi

Display Distribution Metadata
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Full Test Data
    Submit Primary Form

    URL Path Should Be  /dataset/testiaineisto
    Click Link  Testiresurssi
    
    Page Should Contain  Testiresurssi
    Page Should Contain  Testiresurssin kuvaus
    Page Should Contain  HTML
    Page Should Contain  12345
    Page Should Contain  Testiresurssin käyttöoikeuksien kuvaus
    Page Should Contain  http://example.com/api
    Page Should Contain  Voimassa
    Page Should Contain  WGS84
    Page Should Contain  Kuukausi
    Page Should Contain  2023-01-02
    Page Should Contain  2034-03-04
    Page Should Contain  42

Edit Distribution
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Full Test Data
    Submit Primary Form

    URL Path Should Be  /dataset/testiaineisto
    Click Link  Testiresurssi
    Click Link  Muokkaa 

    Input Text  id:field-name_translated-fi  Testiresurssi (muokattu)
    Input Text  id:field-resource-url  http://example.com/modified
    Input Tag Into Select2  field-format  HTMX
    Input Text  id:field-size  1234
    Input Text Into CKEditor  field-description_translated-fi  Testiresurssin kuvaus (muokattu)
    Input Text Into CKEditor  field-rights_translated-fi  Testiresurssin käyttöoikeuksien kuvaus (muokattu)
    Remove Suomi.fi Tag  temporal_granularity  fi  Kuukausi
    Input Tag Into Select2   field-temporal_granularity-fi  Vuosi
    Input Text  id:field-endpoint_url  http://example.com/api/2.0
    Input Text  id:field-position_info  WGS99
    Input Text  id:field-temporal_coverage_from  05/06/2024
    Input Text  id:field-temporal_coverage_till  07/08/2044
    Input Text  id:field-geographical_accuracy  314
    Submit Primary Form

    Page Should Contain  Testiresurssi (muokattu)
    Page Should Contain  Testiresurssin kuvaus (muokattu)
    Page Should Contain  HTMX
    Page Should Contain  1234
    Page Should Contain  Testiresurssin käyttöoikeuksien kuvaus (muokattu)
    Page Should Contain  http://example.com/api/2.0
    Page Should Contain  Voimassa
    Page Should Contain  WGS99
    Page Should Contain  Vuosi
    Page Should Contain  2024-05-06
    Page Should Contain  2044-07-08
    Page Should Contain  314
    

Remove Distribution
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Minimal Test Data
    Submit Primary Form

    URL Path Should Be  /dataset/testiaineisto
    Click Link  Testiresurssi
    Click Link  Muokkaa 

    Scroll Element Into View  css:.form-actions
    Click Link  link:Poista
    Wait Until Element Is Visible  css:.modal .btn-primary
    Click Button  Vahvista
    URL Path Should Be  /dataset/testiaineisto
    Page Should Contain  Tietoaineistoon ei ole lisätty dataa

*** Keywords ***
Distribution Test Setup
    Reset Data And Open Front Page
    Create Test Organisation
    Create Test User
    Add Test User To Test Organisation

    Go To Front Page
