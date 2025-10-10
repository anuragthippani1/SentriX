import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Brain, MessageSquare, FileText, Search, Copy, Check } from 'lucide-react';
import { useState } from 'react';

const Navbar = ({ currentPage, setCurrentPage }) => {
  const [copied, setCopied] = useState(false);
  const location = useLocation();

  const copySessionId = () => {
    const sessionId = `SENTRIX-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    navigator.clipboard.writeText(sessionId);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Brain, path: '/' },
    { id: 'reports', label: 'Reports', icon: FileText, path: '/reports' },
    { id: 'thinking-logs', label: 'Thinking Logs', icon: MessageSquare, path: '/thinking-logs' }
  ];

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <Brain className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">SentriX</span>
            </div>
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
                    to={item.path}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
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

          {/* Right side - Search and Session ID */}
          <div className="flex items-center space-x-4">
            {/* Search */}
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search..."
                className="block w-64 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>

            {/* Session ID */}
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">Session:</span>
              <div className="flex items-center space-x-1 bg-gray-100 px-2 py-1 rounded">
                <span className="text-xs font-mono text-gray-700">
                  SENTRIX-{Date.now().toString().slice(-6)}
                </span>
                <button
                  onClick={copySessionId}
                  className="p-1 hover:bg-gray-200 rounded transition-colors"
                  title="Copy Session ID"
                >
                  {copied ? (
                    <Check className="h-3 w-3 text-green-600" />
                  ) : (
                    <Copy className="h-3 w-3 text-gray-500" />
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
