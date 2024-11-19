## Commands:

<p>To prevent conflicts in rules between ESLint and Prettier, and also to add linting of ES2015+ (ES6+) import/export syntax, let’s add the following plugins:</p>

```
npm install --save-dev eslint-config-prettier eslint-plugin-prettier eslint-plugin-import
```
- eslint-config-prettier: Turns off all ESLint rules that have the potential to interfere with Prettier rules.
- eslint-plugin-prettier: Turns Prettier rules into ESLint rules.
- eslint-plugin-import: Adds support for linting ES2015+ (ES6+) import/export syntax.

<br>
<p>Install the Airbnb ESLint config and the required plugins:</p>

```
npm init @eslint/config@latest
npm install --save-dev eslint-config-airbnb-base eslint-plugin-import
```

```
npm install
npm run backend
npm run dev
```

## Google Calendar API:

https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/metrics?hl=fi&project=unique-acronym-406815
