*** Settings ***
Library   ../CkanLibrary.py

Resource  ../restricteddata.robot

*** Test cases ***
CKAN version
  CKAN Version Should Be  2.10.5

Site title
  Open Chromium
  Front Page Should Be Open
  [Teardown]    Close Chromium
