import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Dashboard from "./components/Dashboard";
import SentriXAssistantPage from "./components/SentriXAssistantPage";
import Reports from "./components/Reports";
import ThinkingLogs from "./components/ThinkingLogs";
import SessionManagerPage from "./components/SessionManagerPage";
import { DashboardProvider } from "./context/DashboardContext";
import { ThemeProvider } from "./context/ThemeContext";
import "./index.css";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  return (
    <ThemeProvider>
      <DashboardProvider>
        <Router>
          <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
            <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />

            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/assistant" element={<SentriXAssistantPage />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/thinking-logs" element={<ThinkingLogs />} />
              <Route path="/session-manager" element={<SessionManagerPage />} />
            </Routes>
          </div>
        </Router>
      </DashboardProvider>
    </ThemeProvider>
  );
}

export default App;
