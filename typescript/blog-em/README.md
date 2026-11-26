# Blog &apos;em Ipsum

> **Status: ✅ Completed**

A small React + TypeScript app for learning [TanStack Query](https://tanstack.com/query) (React Query). It lists blog posts from the [JSONPlaceholder](https://jsonplaceholder.typicode.com) API with paging, next-page prefetching, per-post comments, and delete/update mutations.

## Features

- **Paginated post list** — 5 posts per page with Previous / Next controls.
- **Next-page prefetching** — the following page is fetched in the background so paging feels instant.
- **Post detail view** — click a post to see its body and comments.
- **Mutations** — Delete a post and Update its title, with pending/success feedback.
- **Caching & stale time** — queries are cached and marked stale after 2s via React Query.
- **React Query Devtools** — included for inspecting cache and query state in development.

> **Note:** The API is [JSONPlaceholder](https://jsonplaceholder.typicode.com), a fake REST API. Delete and update requests return success responses but do not persist any changes on the server.

## Tech Stack

- [React 19](https://react.dev)
- [TypeScript](https://www.typescriptlang.org)
- [Vite](https://vite.dev) — dev server and build tooling
- [TanStack Query v5](https://tanstack.com/query) — server-state management
- [Axios](https://axios-http.com) — HTTP client
- [ESLint](https://eslint.org) — linting

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org) (18+ recommended)

### Install

```bash
npm install
```

### Run the dev server

```bash
npm run dev
```

Then open the URL Vite prints (defaults to <http://localhost:5173>).

## Available Scripts

| Script            | Description                                      |
| ----------------- | ------------------------------------------------ |
| `npm run dev`     | Start the Vite dev server with HMR.              |
| `npm run build`   | Type-check (`tsc -b`) and build for production.  |
| `npm run preview` | Preview the production build locally.            |
| `npm run lint`    | Run ESLint over the project.                     |

## Project Structure

```text
src/
├── main.tsx         # App entry point
├── App.tsx          # QueryClientProvider + Devtools + layout
├── Posts.tsx        # Post list, paging, prefetch, mutations
├── PostDetail.tsx   # Selected post body, comments, mutation UI
├── api.ts           # Axios client + fetch/delete/update functions
├── types.ts         # Post and Comment type definitions
└── *.css            # Styles
```

## How It Works

- `App.tsx` wraps the app in a `QueryClientProvider` and mounts the React Query Devtools.
- `Posts.tsx` uses `useQuery` to fetch the current page of posts and a `useEffect` + `queryClient.query` to prefetch the next page. Clicking a post selects it; `useMutation` handles delete and title updates.
- `PostDetail.tsx` fetches comments for the selected post and renders the delete/update buttons with their pending and success states.
- `api.ts` holds the Axios instance and all request functions against JSONPlaceholder.
