*** Settings ***
Documentation     A test suite with a single test for valid login.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Administrator Login
    Go To Login Page
    Input Username    admin
    Input Password    administrator
    Submit Primary Form
    Dashboard Page Should Be Open
