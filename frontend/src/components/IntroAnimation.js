import React, { useState, useEffect } from "react";

const IntroAnimation = ({ onComplete }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // After 4 seconds, slide the intro away
    const timer = setTimeout(() => {
      setIsVisible(false);
      // Wait for slide-out animation to complete, then notify parent
      setTimeout(() => {
        onComplete();
      }, 800);
    }, 4000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div
      className={`fixed inset-0 z-50 bg-black flex items-center justify-center transition-transform duration-800 ease-in-out ${
        isVisible ? "translate-y-0" : "-translate-y-full"
      }`}
    >
      {/* Animated Grid Background */}
      <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
      
      {/* Radial Glow Effect */}
      <div className="absolute inset-0 bg-gradient-radial from-blue-900/20 via-transparent to-transparent"></div>

      <div className="text-center relative z-10 px-4">
        <h1 className="text-6xl md:text-8xl lg:text-[10rem] xl:text-[12rem] font-black tracking-tighter leading-[0.9]">
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp text-white hover-glow"
              style={{
                animationDelay: "0.2s",
                animationFillMode: "forwards",
                letterSpacing: "-0.05em",
              }}
            >
              EXPERIENCE
            </span>
          </div>
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp text-white hover-glow"
              style={{
                animationDelay: "0.5s",
                animationFillMode: "forwards",
                letterSpacing: "-0.05em",
              }}
            >
              THE
            </span>
          </div>
          <div className="overflow-hidden my-2">
            <span
              className="block opacity-0 animate-fadeInUp text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 animate-gradient relative"
              style={{
                animationDelay: "0.8s",
                animationFillMode: "forwards",
                letterSpacing: "-0.05em",
                textShadow: "0 0 80px rgba(59, 130, 246, 0.5)",
              }}
            >
              SUPPLY CHAIN
            </span>
          </div>
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp text-white hover-glow"
              style={{
                animationDelay: "1.1s",
                animationFillMode: "forwards",
                letterSpacing: "-0.05em",
              }}
            >
              INTELLIGENCE
            </span>
          </div>
        </h1>

        {/* Subtitle with Icon */}
        <div
          className="mt-12 opacity-0 animate-fadeIn flex items-center justify-center space-x-3"
          style={{ animationDelay: "1.5s", animationFillMode: "forwards" }}
        >
          <div className="h-px w-12 bg-gradient-to-r from-transparent to-blue-500"></div>
          <p className="text-xl md:text-2xl text-gray-300 font-light tracking-widest uppercase">
            Powered by AI
          </p>
          <div className="h-px w-12 bg-gradient-to-l from-transparent to-blue-500"></div>
        </div>

        {/* Modern Loading Indicator */}
        <div
          className="mt-16 flex items-center justify-center space-x-2 opacity-0 animate-fadeIn"
          style={{ animationDelay: "2s", animationFillMode: "forwards" }}
        >
          <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
          <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: "0.2s" }}></div>
          <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: "0.4s" }}></div>
        </div>

        {/* Sleek Progress Bar */}
        <div
          className="mt-6 max-w-md mx-auto opacity-0 animate-fadeIn"
          style={{ animationDelay: "2.2s", animationFillMode: "forwards" }}
        >
          <div className="h-0.5 bg-gray-900 rounded-full overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 animate-loading-bar shadow-lg shadow-blue-500/50"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntroAnimation;
