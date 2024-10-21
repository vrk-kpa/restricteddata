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
    Fill Resource Form With Full Test Data  name fi=Testiresurssin nimi
    ...                                     description fi=Testiresurssin kuvausteksti
    ...                                     format=XHTML
    ...                                     size=1024
    ...                                     rights fi=Testiresurssin oikeudet
    ...                                     endpoint url=http://example.com/api/2.0
    ...                                     position info=WGS99
    ...                                     temporal granularity fi=Vuosi
    ...                                     temporal coverage from=01/02/2024
    ...                                     temporal coverage till=05/06/2034
    ...                                     geographical accuracy=123
    Submit Primary Form

    URL Path Should Be  /dataset/testiaineisto
    Click Link  Testiresurssin nimi
    
    Page Should Contain  Testiresurssin nimi
    Page Should Contain  Testiresurssin kuvausteksti
    Page Should Contain  XHTML
    Page Should Contain  1024
    Page Should Contain  Testiresurssin oikeudet
    Page Should Contain  http://example.com/api/2.0
    Page Should Contain  Voimassa
    Page Should Contain  WGS99
    Page Should Contain  Vuosi
    Page Should Contain  2024-01-02
    Page Should Contain  2034-05-06
    Page Should Contain  123

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

    Fill Resource Form With Full Test Data  name fi=Testiresurssi (muokattu)
    ...                                     url=http://example.com/modified
    ...                                     format=HTMX
    ...                                     size=1234
    ...                                     description fi=Testiresurssin kuvaus (muokattu)
    ...                                     rights fi=Testiresurssin käyttöoikeuksien kuvaus (muokattu)
    ...                                     temporal granularity fi=Vuosi
    ...                                     endpoint url=http://example.com/api/2.0
    ...                                     position info=WGS99
    ...                                     temporal coverage from=05/06/2024
    ...                                     temporal coverage till=07/08/2044
    ...                                     geographical accuracy=314
    Remove Suomi.fi Tag  temporal_granularity  fi  Kuukausi
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

    Scroll To Form Actions
    Click Link  link:Poista
    Click Suomi.fi Dialog Button  Vahvista
    URL Path Should Be  /dataset/testiaineisto
    Page Should Contain  Tietoaineistoon ei ole lisätty dataa

*** Keywords ***
Distribution Test Setup
    Reset Data And Open Front Page
    Log In As Administrator
    Create Test Organisation
    Create Test User
    Add Test User To Test Organisation
    Log Out
    Go To Front Page
