This directory will contain our frontend mobile application.
We will be using Expo for development of React Native.

### Setup on your machine

- Move into the frontend directory
  - cd frontend
- Install dependencies
  - npm install

### Running the app

- Start the server (from the frontend directory)
  - npx expo start
- Scan the QR code with your phone or choose an option on your computer

### Navigation

The app starts through `index.ts`, which loads Expo Router. The bottom tabs in
`src/app/_layout.tsx` follow the UML: **Find Drivers**, **Map**, and **Profile**.
`src/app/index.tsx` is the default Find Drivers screen; `map.tsx` and `profile.tsx`
are the other screens. Each screen contains its own simple placeholder layout and styles.
The function names match the UML: `NavBar`, `FindDrivers`, `MapDisplay`, and
`ProfilePage`. The tab labels remain Find Drivers, Map, and Profile.
The white background and blue accents follow the UML's light-mode theme.
Search/UserCard, MapWidget, and profile editing are future work.
The original `App.tsx` starter is no longer the app entry point.

These screens do not fetch users, render routes, or save profile information yet.

### Verify changes

- Install dependencies with `npm ci` (Node.js 22.13 or newer).
- Run `npm run lint` and `npm run typecheck`.
- Run `npx expo start`, then open the app in Expo Go.
- Confirm Find Drivers appears first. Tap Map, Profile, and Find Drivers and
  confirm the screen title and selected tab change together.
- Check that the tab bar stays visible and content is readable on a small screen.
- For browser preview, run `npm run web`.
