*** Settings ***
Documentation     A distribution test suite.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Create Distribution With All Fields
    Fail  Not implemented

Display Distribution Metadata
    Fail  Not implemented

Edit Distribution
    Fail  Not implemented

Remove Distribution
    Fail  Not implemented
