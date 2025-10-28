import React from "react";
import { Link, useLocation } from "react-router-dom";

import { Brain, MessageSquare, FileText, Users, Bot } from "lucide-react";

const Navbar = ({ currentPage, setCurrentPage }) => {
  const location = useLocation();

  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: Brain, path: "/dashboard" },
    {
      id: "assistant",
      label: "SentriX Assistant",
      icon: Bot,
      path: "/assistant",
    },
    { id: "reports", label: "Reports", icon: FileText, path: "/reports" },
    {
      id: "thinking-logs",
      label: "Thinking Logs",
      icon: MessageSquare,
      path: "/thinking-logs",
    },
    {
      id: "session-manager",
      label: "Session Manager",
      icon: Users,
      path: "/session-manager",
    },
  ];

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo - Clickable to go home */}
          <div className="flex items-center">
            <Link
              to="/"
              onClick={() => setCurrentPage("home")}
              className="flex-shrink-0 flex items-center hover:opacity-80 transition"
            >
              <img src="/logo.png" alt="SentriX Logo" className="h-8 w-8" />
              <span className="ml-2 text-xl font-bold text-gray-900">
                SentriX
              </span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.id}
                    onClick={() => setCurrentPage(item.id)}
                    to={item.path}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? "bg-gray-100 text-gray-900"
                        : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                    }`}
                  >
                    <div className="flex items-center">
                      <Icon className="h-4 w-4 mr-2" />
                      {item.label}
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
