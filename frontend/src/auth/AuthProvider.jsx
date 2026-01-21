import { useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { fetchMe } from "../api/auth";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(() => Boolean(localStorage.getItem("token")));
  
  useEffect(() => {
    if (!token) return;
    fetchMe(token)
      .then((u) => setUser(u))
      .catch(() => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
        setLoading(false);
      });
  }, [token]);

  function login(newToken) {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setUser(null);
    setLoading(true);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    setLoading(false);
  }

  const computedLoading = Boolean(token) && user === null && loading;

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading: computedLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
