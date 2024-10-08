*** Settings ***
Documentation     A dataset test suite.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Navigate To The Dataset Page
    Click Link  link:Tietoaineistot
    Dataset List Should Be Open

Create Minimal Dataset And Resource
    Create Test Organisation
    Create Test User
    Add Test User To Test Organisation

    Log In As Test User
    Click Link  link:Tietoaineistot
    Click Link  link:Lisää tietoaineisto
    Input Text  id:field-title_translated-fi  Testiaineisto
    Input Text  id:field-title_translated-sv  Test dataset
    Input Text Into CKEditor  field-notes_translated-fi  Testiaineiston kuvaus
    Input Text Into CKEditor  field-notes_translated-sv  Test dataset beskrivning
    Input Tag Into Select2   field-keywords-fi  Testi
    Input Tag Into Select2   field-keywords-sv  Test
    Input Text  id:field-maintainer  Teemu Testaaja
    Input Text  id:field-maintainer_email  teemu.testaaja@example.com
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto/resource/new
    Input Text  id:field-name_translated-fi  Testiresurssi
    Input Text  id:field-name_translated-sv  Test resurs
    Click Button  id:resource-link-button
    Input Text  id:field-resource-url  http://example.com
    Input Tag Into Select2  field-format  HTML
    Input Text  id:field-size  12345
    Input Text Into CKEditor  field-rights_translated-fi  Testiresurssin käyttöoikeuksien kuvaus
    Input Text Into CKEditor  field-rights_translated-sv  Test resurs användningsrättigheter
    Submit Primary Form
    
    URL Path Should Be  /dataset/testiaineisto
    Page Should Contain  Testiaineiston kuvaus
    Page Should Contain  Teemu Testaaja
    Page Should Contain  teemu.testaaja@example.com
        
    Click Link  link:Testiresurssi
    Page Should Contain  12345
    Page Should Contain  Testiresurssin käyttöoikeuksien kuvaus
    
    
Create Dataset With All Fields
    Fail  Not implemented

Display Dataset Metadata
    Fail  Not implemented

Edit Dataset
    Fail  Not implemented

Remove Dataset
    Fail  Not implemented
