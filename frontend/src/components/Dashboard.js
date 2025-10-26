import React from "react";
import { useDashboard } from "../context/DashboardContext";
import WorldMap from "./WorldMap";
import RiskTables from "./RiskTables";
import RiskCharts from "./RiskCharts";
import LoadingSpinner from "./LoadingSpinner";
import { 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  CheckCircle,
  Package,
  Ship,
  Truck,
  Globe
} from "lucide-react";

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

  // Calculate statistics
  const totalCountries = Object.keys(dashboardData.worldRiskData || {}).length;
  const highRiskCount = Object.values(dashboardData.worldRiskData || {}).filter(
    d => d.risk_level >= 3
  ).length;
  const lowRiskCount = Object.values(dashboardData.worldRiskData || {}).filter(
    d => d.risk_level === 1
  ).length;
  const avgRisk = totalCountries > 0 
    ? (Object.values(dashboardData.worldRiskData || {}).reduce((sum, d) => sum + d.risk_level, 0) / totalCountries).toFixed(1)
    : 0;

  const stats = [
    {
      label: "Total Regions",
      value: totalCountries,
      icon: Globe,
      gradient: "from-blue-500 to-blue-600",
      trend: "neutral",
      bgColor: "bg-blue-50",
      iconColor: "text-blue-600"
    },
    {
      label: "High Risk Zones",
      value: highRiskCount,
      icon: AlertTriangle,
      gradient: "from-red-500 to-orange-600",
      trend: "down",
      bgColor: "bg-red-50",
      iconColor: "text-red-600"
    },
    {
      label: "Safe Zones",
      value: lowRiskCount,
      icon: CheckCircle,
      gradient: "from-green-500 to-emerald-600",
      trend: "up",
      bgColor: "bg-green-50",
      iconColor: "text-green-600"
    },
    {
      label: "Avg Risk Score",
      value: avgRisk,
      icon: TrendingUp,
      gradient: "from-indigo-500 to-purple-600",
      trend: "neutral",
      bgColor: "bg-indigo-50",
      iconColor: "text-indigo-600"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Modern Header with Gradient */}
        <div className="mb-8 relative">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl opacity-10"></div>
          <div className="relative bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center space-x-3">
                  <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-3 rounded-xl">
                    <Ship className="h-8 w-8 text-white" />
                  </div>
                  <div>
                    <h1 className="text-3xl font-bold text-gray-900">
                      Supply Chain Control Center
                    </h1>
                    <p className="mt-1 text-gray-600">
                      Real-time global logistics risk monitoring
                    </p>
                  </div>
                </div>
                {currentSession && (
                  <div className="mt-4 flex items-center space-x-2 text-sm">
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="font-medium">Active Session</span>
                    </div>
                    <span className="text-gray-500">{currentSession.name}</span>
                  </div>
                )}
              </div>
              <div className="hidden lg:flex items-center space-x-4">
                <div className="text-right">
                  <p className="text-sm text-gray-500">Last Updated</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {new Date().toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div
              key={index}
              className={`relative bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 overflow-hidden`}
            >
              <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${stat.gradient} opacity-10 rounded-full -mr-16 -mt-16`}></div>
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <div className={`${stat.bgColor} p-3 rounded-lg`}>
                    <stat.icon className={`h-6 w-6 ${stat.iconColor}`} />
                  </div>
                  {stat.trend === "up" && (
                    <TrendingUp className="h-5 w-5 text-green-500" />
                  )}
                  {stat.trend === "down" && (
                    <TrendingDown className="h-5 w-5 text-red-500" />
                  )}
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">
                    {stat.label}
                  </p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stat.value}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="space-y-6">
          {/* World Risk Map - Modern Card */}
          <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4">
              <div className="flex items-center space-x-3">
                <Globe className="h-6 w-6 text-white" />
                <div>
                  <h3 className="text-xl font-bold text-white">
                    Global Risk Heatmap
                  </h3>
                  <p className="text-sm text-blue-100">
                    Interactive world risk assessment & route monitoring
                  </p>
                </div>
              </div>
            </div>
            <div className="p-6 bg-gradient-to-br from-gray-50 to-blue-50">
              <WorldMap worldRiskData={dashboardData.worldRiskData} />
            </div>
          </div>

          {/* Risk Tables - Modern Layout */}
          <RiskTables
            politicalRisks={dashboardData.politicalRisks}
            scheduleRisks={dashboardData.scheduleRisks}
          />

          {/* Risk Charts - Enhanced */}
          <RiskCharts
            politicalRisks={dashboardData.politicalRisks}
            scheduleRisks={dashboardData.scheduleRisks}
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
