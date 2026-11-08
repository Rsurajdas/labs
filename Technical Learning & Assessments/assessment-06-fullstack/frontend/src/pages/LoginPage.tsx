// GIVEN — do not change.
import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { getErrorMessage, login } from "../api";

type LoginPageProps = { onLogin: (token: string) => void };

export function LoginPage({ onLogin }: LoginPageProps) {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const username = String(formData.get("username") ?? "").trim();
    const password = String(formData.get("password") ?? "");
    try {
      const token = await login(username, password);
      onLogin(token);
      navigate("/bookings");
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }

  return (
    <section>
      <h2>Log in</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username
          <input name="username" required />
        </label>
        <label>
          Password
          <input name="password" type="password" required />
        </label>
        {error && <p role="alert">{error}</p>}
        <button type="submit">Log in</button>
      </form>
    </section>
  );
}
