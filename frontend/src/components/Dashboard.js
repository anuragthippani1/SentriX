import React from "react";
import { useDashboard } from "../context/DashboardContext";
import WorldMap from "./WorldMap";
import ChatPanel from "./ChatPanel";
import RiskTables from "./RiskTables";
import RiskCharts from "./RiskCharts";
import LoadingSpinner from "./LoadingSpinner";
import SessionManager from "./SessionManager";

const Dashboard = () => {
  const { dashboardData, sessionId, currentSession } = useDashboard();

  if (dashboardData.loading) {
    return <LoadingSpinner />;
  }

  if (dashboardData.error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">
                Error Loading Dashboard
              </h3>
              <div className="mt-2 text-sm text-red-700">
                {dashboardData.error}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Session Manager */}
      <SessionManager />

      {/* Current Session Banner */}
      {currentSession && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-blue-900">
                Active Session
              </h2>
              <p className="text-sm text-blue-700">{currentSession.name}</p>
              {currentSession.description && (
                <p className="text-xs text-blue-600">
                  {currentSession.description}
                </p>
              )}
            </div>
            <div className="text-sm text-blue-600">
              Real-time risk monitoring active
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content - Left Side */}
        <div className="lg:col-span-2 space-y-6">
          {/* World Risk Map */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                Global Risk Heatmap
              </h3>
              <p className="text-sm text-gray-600">
                Real-time political and supply chain risk assessment
              </p>
            </div>
            <div className="p-6">
              <WorldMap worldRiskData={dashboardData.worldRiskData} />
            </div>
          </div>

          {/* Risk Tables */}
          <RiskTables
            politicalRisks={dashboardData.politicalRisks}
            scheduleRisks={dashboardData.scheduleRisks}
          />

          {/* Risk Charts */}
          <RiskCharts
            politicalRisks={dashboardData.politicalRisks}
            scheduleRisks={dashboardData.scheduleRisks}
          />
        </div>

        {/* Chat Panel - Right Side */}
        <div className="lg:col-span-1">
          <ChatPanel />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
