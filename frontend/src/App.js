import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./components/Dashboard";
import SentriXAssistantPage from "./components/SentriXAssistantPage";
import Reports from "./components/Reports";
import ThinkingLogs from "./components/ThinkingLogs";
import SessionManagerPage from "./components/SessionManagerPage";
import { DashboardProvider } from "./context/DashboardContext";
import "./index.css";

function App() {
  const [currentPage, setCurrentPage] = useState("dashboard");

  return (
    <DashboardProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />

          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/assistant" element={<SentriXAssistantPage />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/thinking-logs" element={<ThinkingLogs />} />
            <Route path="/session-manager" element={<SessionManagerPage />} />
          </Routes>
        </div>
      </Router>
    </DashboardProvider>
  );
}

export default App;
