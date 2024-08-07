import React from 'react';

const Legend = () => {
  return (
    <div className="legend">
      <span style={{ backgroundColor: 'green' }}>Low</span>
      <span style={{ backgroundColor: 'yellow' }}>Medium</span>
      <span style={{ backgroundColor: 'orange' }}>High</span>
      <span style={{ backgroundColor: 'red' }}>Very High</span>
      <span style={{ backgroundColor: 'purple' }}>Extreme</span>
    </div>
  );
};

export default Legend;
