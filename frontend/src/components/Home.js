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
    },
    {
      label: "High Risk Countries",
      value: highRiskCountries,
      icon: AlertTriangle,
    },
    {
      label: "Reports Generated",
      value: totalReports,
      icon: FileText,
    },
    {
      label: "Critical Alerts",
      value: criticalAlerts,
      icon: Shield,
    },
  ];

  const quickActions = [
    {
      title: "View Dashboard",
      description: "Explore global risk heatmap and analytics",
      icon: BarChart3,
      path: "/dashboard",
    },
    {
      title: "SentriX Assistant",
      description: "Get AI-powered route analysis and insights",
      icon: Zap,
      path: "/assistant",
    },
    {
      title: "Risk Reports",
      description: "Access detailed risk assessment reports",
      icon: FileText,
      path: "/reports",
    },
    {
      title: "Global Map",
      description: "Interactive world risk visualization",
      icon: Map,
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
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Hero Section with Ship Image */}
      <div className="relative h-[600px] bg-gray-900 text-white overflow-hidden">
        {/* Background Ship Image */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat brightness-90"
          style={{ backgroundImage: "url(/ship.jpg)" }}
        ></div>

        {/* Enhanced Vignette Effect - Darker Edges */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-black/20 to-black/70"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/60"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-black/40 via-transparent to-black/40"></div>

        {/* Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center relative z-10">
          <div className="text-center w-full">
            {/* Text Content Box with Backdrop */}
            <div className="max-w-4xl mx-auto bg-black/40 backdrop-blur-lg rounded-2xl p-8 md:p-12 border border-white/10 shadow-2xl">
              <div className="inline-block mb-6">
                <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full border border-white/20">
                  <Activity className="h-5 w-5 animate-pulse text-white" />
                  <span className="text-sm font-semibold text-white">
                    Real-Time Intelligence
                  </span>
                </div>
              </div>

              <h1 className="text-5xl md:text-7xl font-extrabold mb-6 text-white drop-shadow-2xl leading-tight">
                Welcome to SentriX
              </h1>

              <p className="text-2xl md:text-3xl font-semibold text-gray-100 mb-6 drop-shadow-lg">
                Real-Time Supply Chain Risk Intelligence
              </p>

              <p className="text-base md:text-lg text-gray-200 max-w-2xl mx-auto leading-relaxed mb-8">
                Navigate global logistics with confidence. Track container ships
                across deep seas, monitor geopolitical risks, and make informed
                decisions powered by AI.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                <button
                  onClick={() => navigate("/dashboard")}
                  className="group bg-white text-gray-900 px-8 py-4 rounded-lg font-semibold text-base shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center space-x-2"
                >
                  <span>View Dashboard</span>
                  <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </button>
                <button
                  onClick={() => navigate("/assistant")}
                  className="group bg-transparent text-white px-8 py-4 rounded-lg font-semibold text-base border-2 border-white/60 hover:bg-white/10 transform hover:scale-105 transition-all duration-200 flex items-center space-x-2"
                >
                  <Zap className="h-5 w-5" />
                  <span>Try AI Assistant</span>
                </button>
              </div>
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
              className="group bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md p-6 transform transition-all duration-200 hover:scale-105 cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {stat.label}
                  </p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {stat.value}
                  </p>
                </div>
                <div className="bg-gray-100 p-3 rounded-lg">
                  <stat.icon className="h-6 w-6 text-gray-600" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative bg-white">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Quick Actions
          </h2>
          <p className="text-gray-600 text-lg">
            Get started with these powerful features
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => navigate(action.path)}
              className="group bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md p-6 text-left transform transition-all duration-200 hover:scale-105"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="bg-gray-100 p-3 rounded-lg">
                  <action.icon className="h-6 w-6 text-gray-700" />
                </div>
                <ArrowRight className="h-5 w-5 text-gray-400 group-hover:translate-x-1 group-hover:text-gray-700 transition-all" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {action.title}
              </h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                {action.description}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className="relative py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose SentriX?
            </h2>
            <p className="text-gray-600 text-lg">
              Comprehensive risk intelligence at your fingertips
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group text-center transform transition-all duration-200 hover:scale-105"
              >
                <div className="bg-white w-16 h-16 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-sm border border-gray-200 group-hover:shadow-md transition-all">
                  <feature.icon className="h-8 w-8 text-gray-700" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative">
        <div className="relative bg-gray-900 rounded-2xl shadow-xl p-12 md:p-16 text-center text-white overflow-hidden">
          <div className="relative z-10">
            <div className="inline-flex items-center space-x-2 bg-white/10 px-4 py-2 rounded-full mb-6">
              <Zap className="h-4 w-4" />
              <span className="text-sm font-semibold">Get Started Now</span>
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Get Started?
            </h2>
            <p className="text-lg text-gray-300 mb-8 max-w-2xl mx-auto">
              Explore the dashboard to see real-time risk intelligence in action
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button
                onClick={() => navigate("/dashboard")}
                className="group bg-white text-gray-900 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg flex items-center justify-center"
              >
                <span>View Dashboard</span>
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button
                onClick={() => navigate("/assistant")}
                className="group bg-transparent text-white px-8 py-3 rounded-lg font-semibold border-2 border-white/40 hover:bg-white/10 transition-all transform hover:scale-105 flex items-center justify-center"
              >
                <Zap className="mr-2 h-5 w-5" />
                <span>Try Assistant</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="relative bg-white border-t border-gray-200 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <img src="/logo.png" alt="SentriX Logo" className="h-8 w-8" />
              <span className="text-xl font-bold text-gray-900">SentriX</span>
            </div>
            <p className="text-gray-600 mb-2">
              © 2024 SentriX. Real-Time Supply Chain Risk Intelligence.
            </p>
            <p className="text-gray-500 text-sm flex items-center justify-center space-x-4">
              <span className="flex items-center">
                <Zap className="h-4 w-4 mr-1" /> Powered by AI
              </span>
              <span>•</span>
              <span className="flex items-center">
                <Globe className="h-4 w-4 mr-1" /> Global Coverage
              </span>
              <span>•</span>
              <span className="flex items-center">
                <Activity className="h-4 w-4 mr-1" /> 24/7 Monitoring
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
