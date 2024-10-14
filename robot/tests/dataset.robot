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
    Fill Resource Form With Minimal Test Data
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto
    Page Should Contain  Testiaineiston kuvaus
    Page Should Contain  Teemu Testaaja
    Page Should Contain  teemu.testaaja@example.com
        
    Click Link  link:Testiresurssi
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
    Fill Dataset Form With Full Test Data
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
    Input Text  id:field-title_translated-fi  Testiaineisto (muokattu)
    Input Text Into CKEditor  field-notes_translated-fi  Testiaineiston kuvaus (muokattu)
    Remove Suomi.fi Tag  keywords  fi  Testi
    Input Tag Into Select2   field-keywords-fi  Muokattu
    Select Suomi.fi Radio Button  private  True
    Select Suomi.fi Radio Button  highvalue  True
    Select Suomi.fi Checkbox  highvalue_category  meteorological
    Scroll Element Into View  name:access_rights
    Select Suomi.fi Radio Button  access_rights  restricted
    Input Text Into CKEditor  field-rights_translated-fi  Testiaineiston käyttöoikeudet (muokattu)
    Input Text  id:field-external_urls-1  https://example.com/3
    Select From List By Value  id:field-update_frequency  weekly
    Input Text  id:field-valid_from  02/03/2024
    Input Text  id:field-valid_till  02/03/2034
    Input Text  id:field-maintainer  Tea Testaaja
    Input Text  id:field-maintainer_email-1  tea.testaaja@example.com
    Input Text  id:field-maintainer_website  https://example.com/service
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

    Scroll Element Into View  css:.form-actions
    Click Link  link:Poista
    Wait Until Element Is Visible  css:.modal .btn-primary
    Click Button  Vahvista
    URL Path Should Be  /dataset/
    Page Should Contain  Ei löytynyt yhtään tietoaineistoa

*** Keywords ***
Dataset Test Setup
    Reset Data And Open Front Page
    Create Test Organisation
    Create Test User
    Add Test User To Test Organisation
    Go To Front Page
    
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
