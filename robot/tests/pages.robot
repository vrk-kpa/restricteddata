*** Settings ***
Documentation     A CMS test suite.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Create A Header Nav Page
    Log In As Administrator
    Open URL Path  /pages_edit
    Fill Pages Form With Test Data
    Select From List By Value  submenu_order  1
    Submit Form  css:.pages-form
    URL Path Should Be  /pages/test
    Element Should Contain  css:h1.page-heading  Title fi
    Log Out

    Go To Front Page
    Reload Page  # CKAN cache shows old front page without this
    Element Should Contain  css:header .navbar  Title fi

    Click Element  id:language-select-dropdown
    Click Element  partial link:(EN)
    Element Should Contain  css:header .navbar  Title en

    Click Element  id:language-select-dropdown
    Click Element  partial link:(SV)
    Element Should Contain  css:header .navbar  Title sv

    Element Should Not Contain  css:.footer-links  Title

Create A Footer Nav Page
    Log In As Administrator
    Open URL Path  /pages_edit
    Fill Pages Form With Test Data
    Select From List By Index  order  1
    Submit Form  css:.pages-form
    URL Path Should Be  /pages/test
    Element Should Contain  css:h1.page-heading  Title fi
    Log Out

    Go To Front Page
    Reload Page  # CKAN cache shows old front page without this
    Element Should Contain  css:.footer-links  Title fi

    Click Element  id:language-select-dropdown
    Click Element  partial link:(EN)
    Element Should Contain  css:.footer-links  Title en

    Click Element  id:language-select-dropdown
    Click Element  partial link:(SV)
    Element Should Contain  css:.footer-links  Title sv

    Element Should Not Contain  css:header .navbar  Title

*** Keywords ***
Fill Pages Form With Test Data
    Input Text  title  Test
    Input Text  publish_date  2024-06-25
    Input Text  title_fi  Title fi
    Input Text  title_sv  Title sv
    Input Text  title_en  Title en
    Input Text  content_fi  Content fi
    Input Text  content_sv  Content sv
    Input Text  content_en  Content en
    Select From List By Index  submenu_order  0
    Select From List By Value  private  False
    Select From List By Index  order  0
 
