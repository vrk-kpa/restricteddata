*** Settings ***
Documentation     A category test suite.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Create Category With All Fields
    Log In As Administrator
    Go To Group List
    Click Link  Lisää kategoria
    Fill Group Form With Full Test Data
    Submit Primary Form
    URL path should be  /group/testikategoria

Display Category Metadata
    Log In As Administrator
    Go To Group List
    Click Link  Lisää kategoria
    Fill Group Form With Full Test Data  title fi=Testikategorian nimi
    ...                                  description fi=Testikategorian kuvausteksti
    ...                                  image url=http://localhost/new-test-image-url.png
    Submit Primary Form
    URL path should be  /group/testikategorian-nimi

    Page Should Contain  Testikategorian nimi
    Page Should Contain  Testikategorian kuvausteksti
    Page Should Contain Image  http://localhost/new-test-image-url.png

Edit Category
    Log In As Administrator
    Go To Group List
    Click Link  Lisää kategoria
    Fill Group Form With Full Test Data
    Submit Primary Form
    URL path should be  /group/testikategoria

    Click Link  Hallinnoi
    Fill Group Form With Full Test Data  title fi=Testikategoria (muokattu)
    ...                                  description fi=Testikategorian kuvaus (muokattu)
    ...                                  image url=http://localhost/new-test-image-url.png
    Submit Primary Form

    URL path should be  /group/testikategoria
    Page Should Contain  Testikategoria (muokattu)
    Page Should Contain  Testikategorian kuvaus (muokattu)
    Page Should Contain Image  http://localhost/new-test-image-url.png

Remove Category
    Log In As Administrator
    Go To Group List
    Click Link  Lisää kategoria
    Fill Group Form With Minimal Test Data
    Submit Primary Form
    URL path should be  /group/testikategoria

    Click Link  Hallinnoi
    Scroll To Form Actions
    Click Link  link:Poista
    Click Suomi.fi Dialog Button  Vahvista
    Wait Until URL Path Is  /group/
