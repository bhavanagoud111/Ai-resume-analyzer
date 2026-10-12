# Resume Analyzer frontend

React app (Create React App, Material UI) for the resume analyzer. It sends the pasted resume text to the backend's `/analyze` endpoint, shows the extracted skills, education and experience, and lists job recommendations from `/recommend`.

## Setup

```bash
npm install
npm start
```

The app runs on http://localhost:3000 and expects the backend at `http://127.0.0.1:8000`. To use a different backend URL, set `REACT_APP_API_URL` before starting:

```bash
REACT_APP_API_URL=http://127.0.0.1:8080 npm start
```

## Scripts

- `npm start`: start the development server
- `npm test`: run the tests
- `npm run build`: create a production build in `build/`
