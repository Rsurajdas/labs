import { NavLink, Outlet } from "react-router-dom";

type LayoutProps = {
  isLoggedIn: boolean;
  onLogout: () => void;
};

export default function Layout({ isLoggedIn, onLogout }: LayoutProps) {
  return (
    <>
      <header>
        <NavLink to="/">Rooms</NavLink>
        {isLoggedIn ? (
          <>
            <NavLink to="/bookings">My bookings</NavLink>
            <button type="button" onClick={onLogout}>
              Log out
            </button>
          </>
        ) : (
          <>
            <NavLink to="/login">Log in</NavLink>
          </>
        )}
      </header>
      <main>
        <Outlet />
      </main>
    </>
  );
}
