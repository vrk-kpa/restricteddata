*** Settings ***
Documentation     A dataset test suite.
Resource          ../restricteddata.robot
Test Setup        Dataset Test Setup
Test Teardown     Close Chromium

*** Test Cases ***
Navigate To The Dataset Page
    Click Link  link:Tietoaineistot
    Dataset List Should Be Open

Create Minimal Dataset And Resource
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Minimal Test Data  url=http://example.com/test-resource
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto
    Page Should Contain  Testiaineiston kuvaus
    Page Should Contain  Teemu Testaaja
    Page Should Contain  teemu.testaaja@example.com
        
    Click Link  http://example.com/test-resource
    Page Should Contain  12345
    Page Should Contain  Testiresurssin käyttöoikeuksien kuvaus
    
    
Create Dataset With All Fields
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Full Test Data
    Submit Primary Form
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Minimal Test Data
    Submit Primary Form

Display Dataset Metadata
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Full Test Data  title fi=Testiaineisto
    ...                                    notes fi=Testiaineiston kuvaus
    ...                                    rights fi=Testiaineiston käyttöoikeudet
    ...                                    keyword fi=Testi
    ...                                    external url=https://example.com
    ...                                    second external url=https://example.com/2
    ...                                    update frequency=annual
    ...                                    valid from=01/01/2023
    ...                                    valid till=01/01/2033
    ...                                    maintainer=Teemu Testaaja
    ...                                    maintainer email=teemu.testaaja@example.com
    ...                                    second maintainer email=teuvo.testaaja@example.com
    ...                                    maintenance website=https://example.com/maintenance
    Submit Primary Form
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Minimal Test Data
    Submit Primary Form
    URL Path Should Be  /dataset/testiaineisto
    Page Should Contain  Testiaineisto
    Page Should Contain Link  /dataset/?vocab_keywords_fi=testi
    Page Should Contain  Testiaineiston kuvaus
    Page Should Contain  Ei-julkinen
    Page Should Contain  Testiaineiston käyttöoikeudet
    Page Should Contain Link  https://example.com
    Page Should Contain Link  https://example.com/2
    Page Should Contain  Vuotuinen
    Page Should Contain  2023-01-01
    Page Should Contain  2033-01-01
    Page Should Contain  Teemu Testaaja
    Page Should Contain Link  teemu.testaaja@example.com
    Page Should Contain Link  teuvo.testaaja@example.com
    Page Should Contain Link  https://example.com/maintenance

Edit Dataset
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Full Test Data
    Submit Primary Form
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Minimal Test Data
    Submit Primary Form
    URL Path Should Be  /dataset/testiaineisto
    Click Link  Muokkaa tietoaineistoa
    Fill Dataset Form With Full Test Data  title fi=Testiaineisto (muokattu)
    ...                                    notes fi=Testiaineiston kuvaus (muokattu)
    ...                                    rights fi=Testiaineiston käyttöoikeudet (muokattu)
    ...                                    keyword fi=Muokattu
    ...                                    private=True
    ...                                    highvalue=True
    ...                                    highvalue category=meteorological
    ...                                    access rights=restricted
    ...                                    external url=https://example.com/3
    ...                                    update frequency=weekly
    ...                                    valid from=02/03/2024
    ...                                    valid till=02/03/2034
    ...                                    maintainer=Tea Testaaja
    ...                                    maintainer email=tea.testaaja@example.com
    ...                                    maintenance website=https://example.com/service
    Submit Primary Form
    Page Should Contain  Yksityinen
    Page Should Contain  Testiaineisto (muokattu)
    Page Should Contain Link  /dataset/?vocab_keywords_fi=muokattu
    Page Should Contain  Testiaineiston kuvaus (muokattu)
    Page Should Contain  Rajattu
    Page Should Contain Link  /dataset/?vocab_highvalue_category=meteorological
    Page Should Contain  Testiaineiston käyttöoikeudet (muokattu)
    Page Should Contain Link  https://example.com/3
    Page Should Contain  Viikoittainen
    Page Should Contain  2024-02-03
    Page Should Contain  2034-02-03
    Page Should Contain  Tea Testaaja
    Page Should Contain Link  tea.testaaja@example.com
    Page Should Contain Link  https://example.com/service
    
Remove Dataset
    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Fill Dataset Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Fill Resource Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto
    Click Link  Muokkaa tietoaineistoa

    Scroll To Form Actions
    Click Link  link:Poista
    Click Suomi.fi Dialog Button  Vahvista
    URL Path Should Be  /dataset/
    Page Should Contain  Ei löytynyt yhtään tietoaineistoa

*** Keywords ***
Dataset Test Setup
    Reset Data And Open Front Page
    Log In As Administrator
    Create Test Organisation
    Create Test User
    Add Test User To Test Organisation
    Log Out
    Go To Front Page
