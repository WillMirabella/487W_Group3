# Penn State Abington Ridesharing App

A number of Penn State Abington students lack consistent access to a car and/or easy access to public transportation. In some instances, students have resorted to regular Uber use, which can be cost-prohibitive. We are seeking a ride-share app, that would be limited to the PSU Abington Community. The app would allow drivers and riders to identify one another based on location and timing. Drivers could include conditions (i.e. time parameters, expected payment mode and amount, cost differential for set meeting place and/or for door to door) and riders could post the same in terms of need. Payment mechanism would not be included within the app, but parties can choose acceptable payment methods (Venmo, Zelle, cash, gas, etc.).

## Local Setup

### Repo

- Clone the repo
  - git clone <https://github.com/WillMirabella/487W_Group3.git>
  - NOTE THIS WILL CHANGE WHEN REPO NAME CHANGES
- Confirm repo creation
  - git status
  - Should see 'On branch main'
- Checkout a branch for your task
  - use following template for branch names
  - name/task#/description-of-task
  - ex. git checkout -b will/task21/design-user-card

### Frontend

- Prerequisites
  - Node.js
    - check by using
      - node --version
  - Expo Go
    - Phone app that will let us test the app using our own phones

- cd frontend
- npm install
- npx expo start

