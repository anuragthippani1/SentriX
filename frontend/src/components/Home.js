import React from "react";
import { useNavigate } from "react-router-dom";
import { useDashboard } from "../context/DashboardContext";
import {
  TrendingUp,
  Globe,
  AlertTriangle,
  FileText,
  ArrowRight,
  Shield,
  BarChart3,
  Map,
  Zap,
  Activity,
} from "lucide-react";

const Home = () => {
  const navigate = useNavigate();
  const { dashboardData, reports } = useDashboard();

  // Calculate statistics
  const totalCountries = Object.keys(dashboardData.worldRiskData || {}).length;
  const highRiskCountries = Object.values(
    dashboardData.worldRiskData || {}
  ).filter((data) => data.risk_level >= 3).length;
  const totalReports = reports.length;
  const criticalAlerts = Object.values(
    dashboardData.worldRiskData || {}
  ).filter((data) => data.risk_level === 4).length;

  const stats = [
    {
      label: "Countries Monitored",
      value: totalCountries,
      icon: Globe,
      gradient: "from-[#6D94C5] to-[#5A7DAD]",
      shadowColor: "shadow-[#6D94C5]/30",
    },
    {
      label: "High Risk Countries",
      value: highRiskCountries,
      icon: AlertTriangle,
      gradient: "from-[#C5946D] to-[#AD7D5A]",
      shadowColor: "shadow-[#C5946D]/30",
    },
    {
      label: "Reports Generated",
      value: totalReports,
      icon: FileText,
      gradient: "from-[#E8DFCA] to-[#D4C5AE]",
      shadowColor: "shadow-[#E8DFCA]/30",
    },
    {
      label: "Critical Alerts",
      value: criticalAlerts,
      icon: Shield,
      gradient: "from-[#6D94C5] to-[#8AABCE]",
      shadowColor: "shadow-[#6D94C5]/30",
    },
  ];

  const quickActions = [
    {
      title: "View Dashboard",
      description: "Explore global risk heatmap and analytics",
      icon: BarChart3,
      gradient: "from-[#6D94C5] to-[#5A7DAD]",
      path: "/dashboard",
    },
    {
      title: "SentriX Assistant",
      description: "Get AI-powered route analysis and insights",
      icon: Zap,
      gradient: "from-[#E8DFCA] to-[#D4C5AE]",
      path: "/assistant",
    },
    {
      title: "Risk Reports",
      description: "Access detailed risk assessment reports",
      icon: FileText,
      gradient: "from-[#6D94C5] to-[#8AABCE]",
      path: "/reports",
    },
    {
      title: "Global Map",
      description: "Interactive world risk visualization",
      icon: Map,
      gradient: "from-[#C5946D] to-[#D4A98A]",
      path: "/dashboard",
    },
  ];

  const features = [
    {
      title: "Real-Time Risk Monitoring",
      description:
        "Track political and supply chain risks across 100+ countries in real-time.",
      icon: Globe,
    },
    {
      title: "AI-Powered Analysis",
      description:
        "Get intelligent route recommendations and risk assessments using advanced AI.",
      icon: TrendingUp,
    },
    {
      title: "Comprehensive Reports",
      description:
        "Generate detailed risk reports with actionable insights and mitigation strategies.",
      icon: FileText,
    },
    {
      title: "Interactive Visualization",
      description:
        "Explore risk data through intuitive maps, charts, and interactive dashboards.",
      icon: BarChart3,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#6D94C5] via-[#CBDCEB] to-[#6D94C5] relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-[#F5EFE6]/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-[#E8DFCA]/20 rounded-full blur-3xl animate-pulse delay-700"></div>
      </div>

      {/* Hero Section with Ship Image */}
      <div className="relative h-[600px] bg-gradient-to-r from-[#6D94C5] via-[#5A7DAD] to-[#6D94C5] text-white overflow-hidden">
        {/* Background Ship Image */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-70"
          style={{ backgroundImage: "url(/ship.jpg)" }}
        ></div>

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#6D94C5]/40 via-[#5A7DAD]/30 to-[#6D94C5]/40"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#6D94C5]/30"></div>

        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>

        {/* Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center relative z-10">
          <div className="text-center w-full">
            <div className="inline-block mb-6">
              <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full border border-white/20 shadow-xl">
                <Activity className="h-5 w-5 animate-pulse" />
                <span className="text-sm font-semibold">
                  Real-Time Intelligence
                </span>
              </div>
            </div>
            <h1 className="text-6xl md:text-7xl font-extrabold mb-6 text-white drop-shadow-2xl">
              Welcome to SentriX
            </h1>
            <p className="text-2xl md:text-3xl font-bold text-blue-100 mb-6 max-w-3xl mx-auto drop-shadow-lg">
              Real-Time Supply Chain Risk Intelligence
            </p>
            <p className="text-lg md:text-xl text-blue-50 max-w-2xl mx-auto leading-relaxed drop-shadow-md mb-8">
              Navigate global logistics with confidence. Track container ships
              across deep seas, monitor geopolitical risks, and make informed
              decisions powered by AI.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <button
                onClick={() => navigate("/dashboard")}
                className="group bg-white text-[#6D94C5] px-8 py-4 rounded-xl font-bold text-lg shadow-2xl hover:shadow-white/20 transform hover:scale-105 transition-all duration-300 flex items-center space-x-2"
              >
                <span>View Dashboard</span>
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button
                onClick={() => navigate("/assistant")}
                className="group bg-white/10 backdrop-blur-sm text-white px-8 py-4 rounded-xl font-bold text-lg border-2 border-white/30 shadow-xl hover:bg-white/20 transform hover:scale-105 transition-all duration-300 flex items-center space-x-2"
              >
                <Zap className="h-5 w-5" />
                <span>Try AI Assistant</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <div
              key={index}
              className={`group bg-gradient-to-br ${stat.gradient} rounded-2xl shadow-2xl ${stat.shadowColor} p-6 transform transition-all duration-300 hover:scale-110 hover:-rotate-1 cursor-pointer border border-white/20 backdrop-blur-sm`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold text-white/80 uppercase tracking-wider">
                    {stat.label}
                  </p>
                  <p className="text-5xl font-extrabold text-white mt-2 group-hover:scale-110 transition-transform">
                    {stat.value}
                  </p>
                </div>
                <div className="bg-white/20 backdrop-blur-md p-4 rounded-xl group-hover:bg-white/30 transition-colors">
                  <stat.icon className="h-8 w-8 text-white animate-pulse" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative">
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
            Quick Actions
          </h2>
          <p className="text-blue-200 text-lg">
            Get started with these powerful features
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => navigate(action.path)}
              className={`group relative bg-gradient-to-br ${action.gradient} rounded-2xl shadow-2xl p-8 text-left transform transition-all duration-300 hover:scale-105 hover:shadow-purple-500/50 border border-white/10 overflow-hidden`}
            >
              <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-6">
                  <div className="bg-white/20 backdrop-blur-md p-3 rounded-xl group-hover:scale-110 transition-transform">
                    <action.icon className="h-8 w-8 text-white" />
                  </div>
                  <ArrowRight className="h-6 w-6 text-white/60 group-hover:translate-x-1 group-hover:text-white transition-all" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">
                  {action.title}
                </h3>
                <p className="text-sm text-white/80 leading-relaxed">
                  {action.description}
                </p>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className="relative py-20 bg-gradient-to-br from-[#5A7DAD] via-[#6D94C5] to-[#5A7DAD]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
              Why Choose SentriX?
            </h2>
            <p className="text-blue-200 text-lg">
              Comprehensive risk intelligence at your fingertips
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group text-center transform transition-all duration-300 hover:scale-105"
              >
                <div className="relative bg-gradient-to-br from-blue-600 to-indigo-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-2xl group-hover:shadow-blue-500/50 group-hover:rotate-6 transition-all">
                  <div className="absolute inset-0 bg-white/10 rounded-2xl group-hover:bg-white/20 transition-colors"></div>
                  <feature.icon className="h-10 w-10 text-white relative z-10" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3 group-hover:text-blue-300 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-sm text-blue-100 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative">
        <div className="relative bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 rounded-3xl shadow-2xl shadow-blue-500/30 p-16 text-center text-white overflow-hidden border border-white/10">
          <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
          <div className="relative z-10">
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
              <Zap className="h-4 w-4" />
              <span className="text-sm font-semibold">Get Started Now</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-extrabold mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-blue-100 mb-10 max-w-2xl mx-auto leading-relaxed">
              Explore the dashboard to see real-time risk intelligence in action
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button
                onClick={() => navigate("/dashboard")}
                className="group relative bg-white text-blue-600 px-10 py-4 rounded-xl font-bold text-lg hover:bg-blue-50 transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl"
              >
                <span className="relative z-10">View Dashboard</span>
                <ArrowRight className="inline-block ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button
                onClick={() => navigate("/assistant")}
                className="group relative bg-indigo-600 text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-indigo-700 transition-all transform hover:scale-105 border-2 border-white/20 shadow-xl hover:shadow-2xl"
              >
                <span className="relative z-10">Try Assistant</span>
                <Zap className="inline-block ml-2 h-5 w-5 group-hover:rotate-12 transition-transform" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="relative bg-gradient-to-br from-[#4A6B96] via-[#5A7DAD] to-[#4A6B96] border-t border-[#CBDCEB]/20 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <div className="h-8 w-8 bg-gradient-to-br from-[#CBDCEB] to-[#E8DFCA] rounded-lg"></div>
              <span className="text-2xl font-bold text-white">SentriX</span>
            </div>
            <p className="text-gray-400 mb-2">
              © 2024 SentriX. Real-Time Supply Chain Risk Intelligence.
            </p>
            <p className="text-gray-500 text-sm flex items-center justify-center space-x-4">
              <span className="flex items-center">
                <Zap className="h-4 w-4 mr-1 text-blue-400" /> Powered by AI
              </span>
              <span>•</span>
              <span className="flex items-center">
                <Globe className="h-4 w-4 mr-1 text-indigo-400" /> Global
                Coverage
              </span>
              <span>•</span>
              <span className="flex items-center">
                <Activity className="h-4 w-4 mr-1 text-blue-400" /> 24/7
                Monitoring
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
