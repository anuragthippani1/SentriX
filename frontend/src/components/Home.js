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
    <div className="min-h-screen bg-white dark:bg-gray-900 relative overflow-hidden transition-colors">
      {/* Hero Section with Lift-up Animation - Inspired by Modern Interactive Design */}
      <div className="relative h-screen bg-gray-900 dark:bg-black text-white overflow-hidden">
        {/* Background Ship Image */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat brightness-50"
          style={{ backgroundImage: "url(/ship.jpg)" }}
        ></div>

        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-black/60"></div>

        {/* Content - Split Screen Effect */}
        <div className="relative z-10 h-full flex items-center justify-center">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
            
            {/* Main Headline - Lift Up Animation */}
            <div className="text-center mb-12 overflow-hidden">
              <div className="animate-slideUp">
                <h1 className="text-7xl md:text-9xl font-black mb-4 tracking-tight leading-none">
                  <span className="block opacity-0 animate-fadeInUp" style={{ animationDelay: '0.1s', animationFillMode: 'forwards' }}>
                    EXPERIENCE
                  </span>
                  <span className="block opacity-0 animate-fadeInUp" style={{ animationDelay: '0.3s', animationFillMode: 'forwards' }}>
                    THE
                  </span>
                  <span className="block opacity-0 animate-fadeInUp text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600" style={{ animationDelay: '0.5s', animationFillMode: 'forwards' }}>
                    SUPPLY CHAIN
                  </span>
                  <span className="block opacity-0 animate-fadeInUp" style={{ animationDelay: '0.7s', animationFillMode: 'forwards' }}>
                    INTELLIGENCE
                  </span>
                </h1>
              </div>
            </div>

            {/* Subtitle */}
            <div className="text-center mb-12 opacity-0 animate-fadeIn" style={{ animationDelay: '1s', animationFillMode: 'forwards' }}>
              <p className="text-xl md:text-2xl text-gray-300 font-light tracking-wide">
                Real-Time Risk Analysis • Global Coverage • AI-Powered Insights
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 opacity-0 animate-fadeIn" style={{ animationDelay: '1.2s', animationFillMode: 'forwards' }}>
              <button
                onClick={() => navigate("/dashboard")}
                className="group relative px-10 py-5 bg-white text-black font-bold text-lg rounded-none overflow-hidden transform hover:scale-105 transition-all duration-300"
              >
                <span className="relative z-10 flex items-center">
                  View Dashboard
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-2 transition-transform" />
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
              </button>
              <button
                onClick={() => navigate("/assistant")}
                className="group px-10 py-5 border-2 border-white text-white font-bold text-lg rounded-none hover:bg-white hover:text-black transform hover:scale-105 transition-all duration-300 flex items-center"
              >
                <Zap className="mr-2 h-5 w-5" />
                Try AI Assistant
              </button>
            </div>

            {/* Scroll Indicator */}
            <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 opacity-0 animate-bounce" style={{ animationDelay: '1.5s', animationFillMode: 'forwards' }}>
              <div className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center p-2">
                <div className="w-1 h-3 bg-white/50 rounded-full animate-pulse"></div>
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
              className="group bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md p-6 transform transition-all duration-200 hover:scale-105 cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    {stat.label}
                  </p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                    {stat.value}
                  </p>
                </div>
                <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg">
                  <stat.icon className="h-6 w-6 text-gray-600 dark:text-gray-300" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative bg-white dark:bg-gray-900">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Quick Actions
          </h2>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            Get started with these powerful features
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => navigate(action.path)}
              className="group bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md p-6 text-left transform transition-all duration-200 hover:scale-105"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg">
                  <action.icon className="h-6 w-6 text-gray-700 dark:text-gray-300" />
                </div>
                <ArrowRight className="h-5 w-5 text-gray-400 dark:text-gray-500 group-hover:translate-x-1 group-hover:text-gray-700 dark:group-hover:text-gray-300 transition-all" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {action.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                {action.description}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className="relative py-20 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose SentriX?
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-lg">
              Comprehensive risk intelligence at your fingertips
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group text-center transform transition-all duration-200 hover:scale-105"
              >
                <div className="bg-white dark:bg-gray-700 w-16 h-16 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-sm border border-gray-200 dark:border-gray-600 group-hover:shadow-md transition-all">
                  <feature.icon className="h-8 w-8 text-gray-700 dark:text-gray-300" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
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
      <div className="relative bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <img src="/logo.png" alt="SentriX Logo" className="h-8 w-8" />
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                SentriX
              </span>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-2">
              © 2024 SentriX. Real-Time Supply Chain Risk Intelligence.
            </p>
            <p className="text-gray-500 dark:text-gray-500 text-sm flex items-center justify-center space-x-4">
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
