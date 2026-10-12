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

`frontend/index.ts` starts Expo Router; it is the entry point configured in
`package.json`. `src/app/index.tsx` is a different file: it redirects the root
route `/` to `/find-drivers` and is hidden from the tab bar.

`src/app/_layout.tsx` defines `NavBar`, with **Find Drivers**, **Map**, and **Profile**
tabs. Each tab's title is also its screen header. The route files
`find-drivers.tsx`, `map.tsx`, and `profile.tsx` export the UML screen components
`FindDrivers`, `MapDisplay`, and `ProfilePage` from `components/`.

The screens share `components/PlaceholderScreen.tsx` and
`styles/screenStyles.ts`. Update those files to change all placeholder cards.
Replace each screen component when its feature is ready. Driver search/UserCard,
MapWidget, and profile editing are future work.

The tab bar's height includes the device's bottom safe area so controls stay
above the home indicator. It does not add a separate minimum-height gap.
The original `App.tsx` starter is no longer the app entry point.

Keep `package-lock.json` committed alongside dependency changes. It records exact
versions for consistent installs across teammates and supports `npm ci`.

### Verify changes

- Install dependencies with `npm ci` (Node.js 22.13 or newer).
- Run `npm run lint` and `npm run typecheck`.
- Run `npx expo start`, then open the app in Expo Go.
- Confirm Find Drivers appears first. Tap Map, Profile, and Find Drivers and
  confirm the screen title and selected tab change together.
- Check that only three tabs appear, the header matches the selected screen, and
  the tab bar reaches the bottom safe area without an extra blank strip.
- Open `/`, `/find-drivers`, `/map`, and `/profile` in the browser to check routes.
- For browser preview, run `npm run web`.
