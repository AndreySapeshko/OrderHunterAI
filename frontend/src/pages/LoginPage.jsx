import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login as apiLogin } from "../api/auth";
import { useAuth } from "../auth/useAuth";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const auth = useAuth();
  const navigate = useNavigate();

  async function submit(e) {
    e.preventDefault();
    setError("");

    try {
      const data = await apiLogin(email, password);
      auth.login(data.access_token);
      navigate("/");
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <form onSubmit={submit} style={{ padding: 20 }}>
      <h2>Login</h2>

      {error && <div style={{ color: "crimson" }}>{error}</div>}

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />

      <button type="submit">Login</button>
    </form>
  );
}
