*** Settings ***
Resource  resource.robot
Resource    home.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username    Piia
    Set Password    Piiansalasana1
    Set Password_confirmation    Piiansalasana1
    Submit Credentials
    Registration Should Succeed

Register With Too Short Username And Valid Password
    Set Username    Pi
    Set Password    Piiansalasana1
    Set Password_confirmation    Piiansalasana1
    Submit Credentials
    Register Should Fail With Message    Username must be minimum of 3 letters

Register With Valid Username And Too Short Password
    Set Username    Piia
    Set Password    Piia1
    Set Password_confirmation    Piiansalasana1
    Submit Credentials
    Register Should Fail With Message    Password must be minimum of 8 characters

Register With Valid Username And Invalid Password
    Set Username    Piia
    Set Password    Piiansalasana
    Set Password_confirmation    Piiansalasana
    Submit Credentials
    Register Should Fail With Message    Password must contain atleast one special charracter

Register With Nonmatching Password And Password Confirmation
    Set Username    Piia
    Set Password    Piiansalasanana1
    Set Password_confirmation    Piiansalasana1
    Submit Credentials
    Register Should Fail With Message    password confirmation does not match

Register With Username That Is Already In Use
    Create User  Piia  kalle123
    Set Username  Piia
    Set Password  Kirre123
    Set Password_confirmation    Kirre123
    Submit Credentials
    Register Should Fail With Message    User with username Piia already exists

*** Keywords ***
Go To Register Page
    Go To  ${REGISTER_URL}

Registration Should Succeed
    Welcome Page Should Be Open

Welcome Page Should Be Open
    Title Should Be  Welcome to Ohtu Application!
Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Register Page Should Be Open
    Title Should Be  Register 

Submit Credentials
    Click Button  Register

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password_confirmation
    [Arguments]  ${password_confirmation}
    Input Password    password_confirmation    ${password_confirmation}


*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Go To Register Page

