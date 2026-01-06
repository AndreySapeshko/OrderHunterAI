import { useState } from "react";
import { register } from "../api/auth";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");

    try {
      await register(email, password);
      setMessage("Registration submitted. Await admin approval.");
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <form onSubmit={submit} style={{ padding: 20 }}>
      <h2>Register</h2>

      {error && <div style={{ color: "crimson" }}>{error}</div>}
      {message && <div>{message}</div>}

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

      <button type="submit">Register</button>
    </form>
  );
}
