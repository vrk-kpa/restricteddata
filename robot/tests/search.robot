*** Settings ***
Documentation     A search test suite.
Resource          ../restricteddata.robot
Test Setup        Search Test Setup
Test Teardown     Close Chromium

*** Test Cases ***
Dataset Search With Filters
    Log In As Test User

    Go To Dataset List
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Full Test Data
    Submit Primary Form
    Fill Resource Form With Minimal Test Data
    Submit Primary Form

    Go To Dataset List
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Full Test Data  title fi=Toinen testiaineisto  keyword fi=Toinen
    Submit Primary Form
    Fill Resource Form With Minimal Test Data  format=CSV
    Submit Primary Form

    Go To Dataset List
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Full Test Data  title fi=Kolmas testiaineisto
    ...                                    highvalue=True  highvalue category=meteorological
    Submit Primary Form
    Fill Resource Form With Minimal Test Data  format=XML
    Submit Primary Form

    Log Out

    Log In As Administrator
    Go To Dataset List
    Click Link  Testiaineisto
    Click Link  Muokkaa kategorioita
    Select Suomi.fi Checkbox  kategoria
    Submit Primary Form
    Log Out

    Go To Dataset List
    Page Should Contain  Löytyi 3 tietoaineistoa

    Click Link  partial link:testi
    Page Should Contain  Löytyi 2 tietoaineistoa

    Click Link  partial link:XML
    Page Should Contain  Löytyi 1 tietoaineisto

    Click Link  partial link:Säätiedot
    Page Should Contain  Löytyi 1 tietoaineisto

    Click Link  partial link:XML
    Click Link  partial link:testi
    Page Should Contain  Löytyi 1 tietoaineisto

*** Keywords ***
Search Test Setup
    Reset Data And Open Front Page
    Log In As Administrator
    Create Test Organisation
    Create Test User
    Add Test User To Test Organisation

    Go To Group List
    Click Link  Lisää kategoria
    Fill Group Form With Full Test Data  title fi=Kategoria
    Submit Primary Form

    Log Out
    Go To Front Page
