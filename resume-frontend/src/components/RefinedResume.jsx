import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './RefinedResume.css';

function RefinedResume({ onRegenerate }) {
  const navigate = useNavigate();
  const location = useLocation();

  // Retrieve the resume data from the location state or use a fallback
  const [resume, setResume] = useState(location.state?.resumeText || {});

  // Initialize prompts based on the resume sections
  const [prompts, setPrompts] = useState(
    Object.keys(resume).reduce((acc, key) => ({ ...acc, [key]: '' }), {})
  );

  // Handle the regeneration of individual sections
  const handleRegenerate = async (section) => {
    if (onRegenerate) {
      const updatedSection = await onRegenerate(section, prompts[section]);
      setResume((prev) => ({
        ...prev,
        [section]: updatedSection
      }));
    }
  };

  // Handle changes in the prompt inputs
  const handlePromptChange = (section, value) => {
    setPrompts((prev) => ({
      ...prev,
      [section]: value
    }));
  };

  // Dummy function to simulate PDF generation
  const handleGeneratePDF = () => {
    console.log('Generating PDF...');
    // Implement PDF generation logic
  };

  // Render the content of each resume section
  const renderSectionContent = (sectionContent) => {
    if (Array.isArray(sectionContent)) {
      // Render array of items
      return sectionContent.map((item, index) => (
        <div key={index} className="section-content">
          {Object.entries(item).map(([key, value]) => (
            Array.isArray(value) ? (
              <div key={key} className="item">
                <span className="key">{key}:</span>
                <ul className="value">
                  {value.map((val, idx) => <li key={idx}>{val}</li>)}
                </ul>
              </div>
            ) : (
              <div key={key} className="item">
                <span className="key">{key}:</span>
                <span className="value">{value}</span>
              </div>
            )
          ))}
        </div>
      ));
    } else if (typeof sectionContent === 'object' && sectionContent !== null) {
    return Object.entries(sectionContent).map(([key, value]) => {
      // If the value is an array, render it as a list
      if (Array.isArray(value)) {
        return (
          <div key={key} className="item">
            <span className="key">{key}:</span>
            <ul className="value">
              {value.map((val, idx) => <li key={idx}>{val}</li>)}
            </ul>
          </div>
        );
      }
      // If the value is a string, render it directly
      else {
        return (
          <div key={key} className="item">
            <span className="key">{key}:</span>
            <span className="value">{value}</span>
          </div>
        );
      }
    });
  }
  // If it's neither (e.g., a string), just return the content directly.
  else {
    return <span>{sectionContent}</span>;
  }
};

  return (
    <div className="refined-resume">
      {Object.keys(resume).map((sectionKey) => {
        const sectionContent = resume[sectionKey];
        return (
          <div key={sectionKey} className="resume-section">
            <h3>{sectionKey.charAt(0).toUpperCase() + sectionKey.slice(1)}</h3>
            {renderSectionContent(sectionContent)}
            <textarea
              value={prompts[sectionKey]}
              onChange={(e) => handlePromptChange(sectionKey, e.target.value)}
              placeholder={`Enter prompt to refine your ${sectionKey}`}
            />
            <button onClick={() => handleRegenerate(sectionKey)}>Regenerate section</button>
          </div>
        );
      })}
      <button onClick={() => navigate('/')}>Upload Another Resume</button>
      <button onClick={handleGeneratePDF}>Generate PDF</button>
    </div>
  );
}

export default RefinedResume;
