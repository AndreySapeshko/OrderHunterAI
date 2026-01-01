import { Routes, Route, Link } from "react-router-dom";
import RawItemsPage from "./pages/RawItemsPage.jsx";
import UserLeadsPage from "./pages/UserLeadsPage";
import UserLeadDetailPage from "./pages/UserLeadsPage.jsx";

export default function App() {
  return (
    <div style={{ padding: 20, fontFamily: "system-ui" }}>
      <nav style={{ marginBottom: 20 }}>
        <Link to="/raw-items">Raw items</Link>{" | "}
        <Link to="/leads">My leads</Link>
      </nav>

      <Routes>
        <Route path="/raw-items" element={<RawItemsPage />} />
        <Route path="/leads" element={<UserLeadsPage />} />
        <Route path="/leads/:id" element={<UserLeadDetailPage />} />
        <Route path="*" element={<UserLeadsPage />} />
      </Routes>
    </div>
  );
}
