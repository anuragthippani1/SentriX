import React from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import { Tooltip } from 'recharts';

const geoUrl = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson";

const WorldMap = ({ worldRiskData }) => {
  const getRiskColor = (riskLevel) => {
    if (riskLevel >= 4) return '#7C2D12'; // Critical - Dark red
    if (riskLevel === 3) return '#EF4444'; // High - Red
    if (riskLevel === 2) return '#F59E0B'; // Medium - Yellow
    if (riskLevel === 1) return '#10B981'; // Low - Green
    return '#E5E7EB'; // No data - Gray
  };

  const getRiskLabel = (riskLevel) => {
    if (riskLevel >= 4) return 'Critical Risk';
    if (riskLevel === 3) return 'High Risk';
    if (riskLevel === 2) return 'Medium Risk';
    if (riskLevel === 1) return 'Low Risk';
    return 'No Data';
  };

  return (
    <div className="w-full">
      <ComposableMap
        projectionConfig={{
          scale: 120,
          center: [0, 20]
        }}
        width={600}
        height={400}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const countryName = geo.properties.NAME || geo.properties.NAME_EN;
              const riskLevel = worldRiskData[countryName]?.risk_level || 0;
              const riskFactors = worldRiskData[countryName]?.risk_factors || [];
              
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
                      outline: 'none',
                    },
                    hover: {
                      fill: getRiskColor(riskLevel),
                      outline: 'none',
                      stroke: '#1E40AF',
                      strokeWidth: 2,
                    },
                    pressed: {
                      fill: getRiskColor(riskLevel),
                      outline: 'none',
                    },
                  }}
                  onMouseEnter={() => {
                    // Tooltip functionality would go here
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>

      {/* Legend */}
      <div className="mt-4 flex flex-wrap justify-center gap-4">
        {[
          { level: 0, label: 'No Data', color: '#E5E7EB' },
          { level: 1, label: 'Low Risk', color: '#10B981' },
          { level: 2, label: 'Medium Risk', color: '#F59E0B' },
          { level: 3, label: 'High Risk', color: '#EF4444' },
          { level: 4, label: 'Critical Risk', color: '#7C2D12' }
        ].map(({ level, label, color }) => (
          <div key={level} className="flex items-center space-x-2">
            <div 
              className="w-4 h-4 rounded" 
              style={{ backgroundColor: color }}
            />
            <span className="text-sm text-gray-600">{label}</span>
          </div>
        ))}
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
            {Object.values(worldRiskData).filter(data => data.risk_level >= 3).length}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorldMap;
