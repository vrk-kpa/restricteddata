*** Settings ***
Documentation     A search test suite.
Resource          ../restricteddata.robot
Test Setup        Reset Data And Open Front Page
Test Teardown     Close Chromium

*** Test Cases ***
Dataset Search With Filters
    Fail  Not implemented
