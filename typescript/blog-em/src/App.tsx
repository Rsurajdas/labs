import { Posts } from "./Posts";
import "./App.css";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const query = new QueryClient();

function App() {
  return (
    // provide React Query client to App
    <QueryClientProvider client={query}>
      <ReactQueryDevtools initialIsOpen={false} />
      <div className="App">
        <h1>Blog &apos;em Ipsum</h1>
        <Posts />
      </div>
    </QueryClientProvider>
  );
}

export default App;
