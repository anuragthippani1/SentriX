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
      <div className="text-center">
        <h1 className="text-6xl md:text-8xl lg:text-9xl font-black text-white tracking-tight leading-none">
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp"
              style={{
                animationDelay: "0.2s",
                animationFillMode: "forwards",
              }}
            >
              EXPERIENCE
            </span>
          </div>
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp"
              style={{
                animationDelay: "0.5s",
                animationFillMode: "forwards",
              }}
            >
              THE
            </span>
          </div>
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500"
              style={{
                animationDelay: "0.8s",
                animationFillMode: "forwards",
              }}
            >
              SUPPLY CHAIN
            </span>
          </div>
          <div className="overflow-hidden">
            <span
              className="block opacity-0 animate-fadeInUp"
              style={{
                animationDelay: "1.1s",
                animationFillMode: "forwards",
              }}
            >
              INTELLIGENCE
            </span>
          </div>
        </h1>

        {/* Subtitle */}
        <div
          className="mt-8 opacity-0 animate-fadeIn"
          style={{ animationDelay: "1.5s", animationFillMode: "forwards" }}
        >
          <p className="text-xl md:text-2xl text-gray-400 font-light">
            Powered by AI
          </p>
        </div>

        {/* Loading bar */}
        <div
          className="mt-12 max-w-xs mx-auto opacity-0 animate-fadeIn"
          style={{ animationDelay: "2s", animationFillMode: "forwards" }}
        >
          <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-blue-400 to-purple-600 animate-loading-bar"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntroAnimation;

