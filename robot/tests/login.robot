*** Settings ***
Documentation     A test suite with a single test for valid login.
Resource          ../restricteddata.robot

*** Test Cases ***
Administrator Login
    Open Browser To Login Page
    Input Username    admin
    Input Password    administrator
    Submit Credentials
    Dashboard Page Should Be Open
    [Teardown]    Close Chromium
