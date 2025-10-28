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
    <nav className="bg-gradient-to-r from-[#A0937D] to-[#B6C7AA] shadow-lg border-b border-[#E7D4B5]">
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
              <span className="ml-2 text-xl font-bold text-white">
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
                        ? "bg-white/20 text-white backdrop-blur-sm"
                        : "text-white/80 hover:bg-white/10 hover:text-white"
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
