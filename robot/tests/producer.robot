*** Settings ***
Documentation     A producer test suite.
Resource          ../restricteddata.robot
Test Setup        Producer Test Setup
Test Teardown     Close Chromium

*** Test Cases ***
Display Producer Metadata
    Log In As Test User
    Open URL Path  /organization/testiorganisaatio
    Click Link  Hallinnoi
    URL Path Should Be  /organization/edit/testiorganisaatio
    Fill Organisation Form With Full Test Data
    Submit Primary Form

    URL Path Should Be  /organization/testiorganisaatio
    Page Should Contain  Testiorganisaatio

    Go To Organisation List
    Page Should Contain  Testiorganisaatio
    Page Should Contain  Testiorganisaation kuvaus

Edit Producer
    Log In As Test User
    Open URL Path  /organization/testiorganisaatio
    Click Link  Hallinnoi
    Fill Organisation Form With Full Test Data
    Submit Primary Form

Remove Producer
    Log In As Administrator
    Open URL Path  /organization/testiorganisaatio
    Click Link  Hallinnoi

    Scroll To Form Actions
    Click Link  link:Poista
    Click Suomi.fi Dialog Button  Vahvista
    URL Path Should Be  /organization/

*** Keywords ***
Producer Test Setup
    Reset Data And Open Front Page
    Log In As Administrator
    Create Test Organisation
    Create Test User
    Add Test User To Test Organisation
    Log out
    Go To Front Page
