import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthProvider";
import AppContent from "./AppContent";

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
