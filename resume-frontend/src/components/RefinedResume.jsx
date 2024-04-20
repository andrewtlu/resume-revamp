// RefinedResume.jsx
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './RefinedResume.css';
function RefinedResume({ onRegenerate }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [promptText, setPromptText] = useState('');

  const resumeText = location.state?.resumeText || '';

  const handleRegenerate = () => {
    if(onRegenerate) {
      onRegenerate(promptText);
    } else {
    }
  };

  const handleDownload = () => {
  };

  const handleGoBack = () => {
    navigate('/');
  };

  return (
    <div className="refined-resume">
      <button onClick={handleDownload}>Download Resume</button>
      <textarea
        value={promptText}
        onChange={(e) => setPromptText(e.target.value)}
        placeholder="Describe how you want to change your resume."
      />
      <button onClick={handleRegenerate}>Regenerate Resume</button>
      <button onClick={handleGoBack}>Upload Another Resume</button>
      {resumeText && <div>{resumeText}</div>}
    </div>
  );
}

export default RefinedResume;
