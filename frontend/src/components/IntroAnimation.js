import React, { useState, useEffect } from "react";

const IntroAnimation = ({ onComplete }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // After 2.5 seconds, slide the intro away
    const timer = setTimeout(() => {
      setIsVisible(false);
      // Wait for slide-out animation to complete, then notify parent
      setTimeout(() => {
        onComplete();
      }, 800);
    }, 2500);

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
        <h1 className="text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-black tracking-tight leading-tight">
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp text-white hover-glow"
              style={{
                animationDelay: "0.1s",
                animationFillMode: "forwards",
              }}
            >
              EXPERIENCE
            </span>
          </div>
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp text-white hover-glow"
              style={{
                animationDelay: "0.3s",
                animationFillMode: "forwards",
              }}
            >
              THE
            </span>
          </div>
          <div className="overflow-hidden my-2">
            <span
              className="block opacity-0 animate-fadeInUp text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 animate-gradient relative"
              style={{
                animationDelay: "0.5s",
                animationFillMode: "forwards",
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
                animationDelay: "0.7s",
                animationFillMode: "forwards",
              }}
            >
              INTELLIGENCE
            </span>
          </div>
        </h1>

        {/* Subtitle with Icon */}
        <div
          className="mt-10 opacity-0 animate-fadeIn flex items-center justify-center space-x-3"
          style={{ animationDelay: "1s", animationFillMode: "forwards" }}
        >
          <div className="h-px w-12 bg-gradient-to-r from-transparent to-blue-500"></div>
          <p className="text-lg md:text-xl text-gray-300 font-light tracking-widest uppercase">
            Powered by AI
          </p>
          <div className="h-px w-12 bg-gradient-to-l from-transparent to-blue-500"></div>
        </div>
      </div>
    </div>
  );
};

export default IntroAnimation;
