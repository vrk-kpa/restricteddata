*** Settings ***
Documentation     A category test suite.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Create Category With All Fields
    Fail  Not implemented

Display Category Metadata
    Fail  Not implemented

Edit Category
    Fail  Not implemented

Remove Category
    Fail  Not implemented
