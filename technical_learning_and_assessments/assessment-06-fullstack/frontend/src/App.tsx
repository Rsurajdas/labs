import { useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import { RoomsPage } from "./pages/RoomsPage";
import RoomDetailPage from "./pages/RoomDetailPage";
import { MyBookingsPage } from "./pages/MyBookingsPage";
import { LoginPage } from "./pages/LoginPage";
import { NotFoundPage } from "./pages/NotFoundPage";

export default function App() {
  const [token, setToken] = useState<string | null>(null);

  return (
    <Routes>
      <Route
        path="/"
        element={<Layout isLoggedIn={true} onLogout={() => {}} />}
      >
        <Route index element={<RoomsPage />} />
        <Route path={`rooms/:roomId`} element={<RoomDetailPage />} />

        <Route
          path={`/bookings`}
          element={
            <>
              {!token ? (
                <Navigate to="/login" replace />
              ) : (
                <MyBookingsPage token={token} />
              )}
            </>
          }
        />
        <Route
          path={`/login`}
          element={<LoginPage onLogin={(token) => {}} />}
        />
        <Route path={`*`} element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
