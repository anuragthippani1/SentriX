import React from "react";
import { useDashboard } from "../context/DashboardContext";
import WorldMap from "./WorldMap";
import RiskTables from "./RiskTables";
import RiskCharts from "./RiskCharts";
import LoadingSpinner from "./LoadingSpinner";

const Dashboard = () => {
  const { dashboardData, sessionId, currentSession } = useDashboard();

  // Debug: Log dashboard data
  console.log("Dashboard - dashboardData:", dashboardData);
  console.log("Dashboard - worldRiskData:", dashboardData.worldRiskData);

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
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-lg text-gray-600">
          Real-time supply chain risk intelligence
        </p>
        {currentSession && (
          <div className="mt-2 text-sm text-gray-500">
            Session: {currentSession.name} ({currentSession.id})
          </div>
        )}
      </div>

      <div className="space-y-6">
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
    </div>
  );
};

export default Dashboard;
