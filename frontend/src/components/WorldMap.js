import React, { useState } from "react";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";

const geoUrl =
  "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson";

const WorldMap = ({ worldRiskData = {} }) => {
  const [tooltipContent, setTooltipContent] = useState("");
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  // Country name mapping to normalize different naming conventions
  const countryNameMapping = {
    "United States of America": "United States",
    "United States": "United States",
    USA: "United States",
    "United Kingdom": "United Kingdom",
    UK: "United Kingdom",
    "Great Britain": "United Kingdom",
    Russia: "Russia",
    "Russian Federation": "Russia",
    "South Korea": "South Korea",
    "Republic of Korea": "South Korea",
    "North Korea": "North Korea",
    "Democratic People's Republic of Korea": "North Korea",
    Iran: "Iran",
    "Islamic Republic of Iran": "Iran",
    Syria: "Syria",
    "Syrian Arab Republic": "Syria",
    Iraq: "Iraq",
    "Republic of Iraq": "Iraq",
    Afghanistan: "Afghanistan",
    "Islamic Republic of Afghanistan": "Afghanistan",
    Yemen: "Yemen",
    "Republic of Yemen": "Yemen",
    Somalia: "Somalia",
    "Federal Republic of Somalia": "Somalia",
    Libya: "Libya",
    "State of Libya": "Libya",
    Sudan: "Sudan",
    "Republic of the Sudan": "Sudan",
    "South Sudan": "South Sudan",
    "Republic of South Sudan": "South Sudan",
    "Central African Republic": "Central African Republic",
    CAR: "Central African Republic",
    "Democratic Republic of the Congo": "Democratic Republic of the Congo",
    DRC: "Democratic Republic of the Congo",
    Congo: "Congo",
    "Republic of the Congo": "Congo",
    "Dem. Rep. Congo": "Democratic Republic of the Congo",
    "Congo Kinshasa": "Democratic Republic of the Congo",
    "Congo Brazzaville": "Congo",
    China: "China",
    "People's Republic of China": "China",
    Vietnam: "Vietnam",
    "Viet Nam": "Vietnam",
    Myanmar: "Myanmar",
    Burma: "Myanmar",
    "Czech Republic": "Czech Republic",
    Czechia: "Czech Republic",
    Tanzania: "Tanzania",
    "United Republic of Tanzania": "Tanzania",
  };

  const getRiskColor = (riskLevel) => {
    if (riskLevel >= 4) return "#7F1D1D"; // Critical Risk - Very Dark Red
    if (riskLevel === 3) return "#DC2626"; // High Risk - Dark Red
    if (riskLevel === 2) return "#F59E0B"; // Medium Risk - Amber
    if (riskLevel === 1) return "#059669"; // Low Risk - Emerald Green
    return "#F3F4F6"; // No Data - Light Gray
  };

  const getRiskLabel = (riskLevel) => {
    if (riskLevel >= 4) return "Critical Risk";
    if (riskLevel === 3) return "High Risk";
    if (riskLevel === 2) return "Medium Risk";
    if (riskLevel === 1) return "Low Risk";
    return "No Data";
  };

  const getCountryRiskData = (countryName) => {
    // Check if countryName is valid
    if (!countryName || typeof countryName !== "string") {
      return null;
    }

    // Try exact match first
    if (worldRiskData[countryName]) {
      return worldRiskData[countryName];
    }

    // Try mapped name
    const mappedName = countryNameMapping[countryName];
    if (mappedName && worldRiskData[mappedName]) {
      return worldRiskData[mappedName];
    }

    // Try case-insensitive match
    const lowerCountryName = countryName.toLowerCase();
    for (const [key, value] of Object.entries(worldRiskData)) {
      if (key.toLowerCase() === lowerCountryName) {
        return value;
      }
    }

    return null;
  };

  const handleMouseEnter = (geo, event) => {
    const countryName = geo.properties?.NAME || geo.properties?.NAME_EN;
    const riskData = getCountryRiskData(countryName);

    if (riskData) {
      const riskFactors = riskData.risk_factors
        ? riskData.risk_factors.join(", ")
        : "None identified";

      const riskLevel = riskData.risk_level;
      const riskColor = getRiskColor(riskLevel);
      const riskLabel = getRiskLabel(riskLevel);

      setTooltipContent(`
        <div class="bg-white rounded-lg shadow-xl border border-gray-200 p-4 max-w-sm">
          <div class="flex items-center space-x-2 mb-2">
            <div class="w-3 h-3 rounded-full" style="background-color: ${riskColor}"></div>
            <div class="font-bold text-gray-900 text-lg">${countryName}</div>
          </div>
          <div class="mb-3">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" style="background-color: ${riskColor}; color: white;">
              ${riskLabel}
            </span>
          </div>
          <div class="text-sm text-gray-700 mb-2">${riskData.details}</div>
          <div class="text-xs text-gray-600">
            <div class="font-semibold mb-1">Risk Factors:</div>
            <div class="text-gray-500">${riskFactors}</div>
          </div>
          ${
            riskLevel >= 3
              ? `
            <div class="mt-3 pt-2 border-t border-gray-200">
              <div class="text-xs font-semibold text-red-600 mb-1">⚠️ High Risk Alert</div>
              <div class="text-xs text-gray-600">Consider alternative routes or enhanced security measures</div>
            </div>
          `
              : ""
          }
        </div>
      `);
    } else {
      setTooltipContent(`
        <div class="bg-white rounded-lg shadow-xl border border-gray-200 p-4">
          <div class="font-bold text-gray-900 text-lg mb-2">${countryName}</div>
          <div class="text-sm text-gray-600">No risk data available</div>
          <div class="text-xs text-gray-500 mt-2">Data collection in progress</div>
        </div>
      `);
    }

    setTooltipPosition({ x: event.clientX, y: event.clientY });
  };

  const handleMouseLeave = () => {
    setTooltipContent("");
  };

  return (
    <div className="w-full">
      <ComposableMap
        projectionConfig={{
          scale: 120,
          center: [0, 20],
        }}
        width={600}
        height={400}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const countryName =
                geo.properties?.NAME || geo.properties?.NAME_EN;
              const riskData = getCountryRiskData(countryName);
              const riskLevel = riskData ? riskData.risk_level : 0;

              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={getRiskColor(riskLevel)}
                  stroke="#FFFFFF"
                  strokeWidth={0.5}
                  style={{
                    default: {
                      fill: getRiskColor(riskLevel),
                      outline: "none",
                    },
                    hover: {
                      fill: getRiskColor(riskLevel),
                      outline: "none",
                      stroke: "#1E40AF",
                      strokeWidth: 2,
                    },
                    pressed: {
                      fill: getRiskColor(riskLevel),
                      outline: "none",
                    },
                  }}
                  onMouseEnter={(event) => handleMouseEnter(geo, event)}
                  onMouseLeave={handleMouseLeave}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>

      {/* Tooltip */}
      {tooltipContent && (
        <div
          className="fixed z-50 pointer-events-none"
          style={{
            left: `${tooltipPosition.x + 10}px`,
            top: `${tooltipPosition.y + 10}px`,
          }}
          dangerouslySetInnerHTML={{ __html: tooltipContent }}
        />
      )}

      {/* Enhanced Legend */}
      <div className="mt-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
        <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
          <span className="mr-2">🗺️</span>
          Risk Assessment Legend
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            {
              level: 4,
              label: "Critical Risk",
              color: "#7F1D1D",
              description: "Active conflicts, sanctions, severe instability",
            },
            {
              level: 3,
              label: "High Risk",
              color: "#DC2626",
              description: "Political tensions, security concerns",
            },
            {
              level: 2,
              label: "Medium Risk",
              color: "#F59E0B",
              description: "Moderate political uncertainty",
            },
            {
              level: 1,
              label: "Low Risk",
              color: "#059669",
              description: "Stable political environment",
            },
            {
              level: 0,
              label: "No Data",
              color: "#F3F4F6",
              description: "Data collection in progress",
            },
          ].map(({ level, label, color, description }) => (
            <div key={level} className="flex items-start space-x-3">
              <div
                className="w-4 h-4 rounded flex-shrink-0 mt-0.5"
                style={{ backgroundColor: color }}
              />
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium text-gray-900">{label}</div>
                <div className="text-xs text-gray-500 leading-tight">
                  {description}
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 pt-3 border-t border-blue-200">
          <div className="text-xs text-gray-600">
            <div className="font-semibold mb-2 flex items-center">
              <span className="mr-1">💡</span>
              Interactive Tips:
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-gray-500">
              <div>• Hover over countries for detailed risk information</div>
              <div>• Colors update in real-time based on risk levels</div>
              <div>• Consider alternative routes for critical shipments</div>
              <div>• Risk levels are continuously monitored</div>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Summary */}
      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div className="bg-gray-50 p-3 rounded">
          <div className="font-medium text-gray-900">Countries Monitored</div>
          <div className="text-2xl font-bold text-blue-600">
            {Object.keys(worldRiskData).length}
          </div>
        </div>
        <div className="bg-gray-50 p-3 rounded">
          <div className="font-medium text-gray-900">High Risk Countries</div>
          <div className="text-2xl font-bold text-red-600">
            {
              Object.values(worldRiskData).filter(
                (data) => data.risk_level >= 3
              ).length
            }
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorldMap;
