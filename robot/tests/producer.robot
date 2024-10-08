*** Settings ***
Documentation     A producer test suite.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Create Producer With All Fields
    Fail  Not implemented

Display Producer Metadata
    Fail  Not implemented

Edit Producer
    Fail  Not implemented

Remove Producer
    Fail  Not implemented
