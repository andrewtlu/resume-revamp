import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './RefinedResume.css';

function RefinedResume() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(false);
  const [resume, setResume] = useState(location.state?.resumeText || {});

  // Initialize prompts state to handle each section and sub-items if applicable
  const [prompts, setPrompts] = useState(
    Object.keys(resume).reduce((acc, key) => {
      if (Array.isArray(resume[key])) {
        return { ...acc, [key]: resume[key].map(() => '') };
      } else {
        return { ...acc, [key]: '' };
      }
    }, {})
  );

const handleRegenerate = async (section, index = null) => {
  const promptText = typeof index === 'number' ? prompts[section][index] : prompts[section];
  if (!promptText.trim()) return;
  setIsLoading(true);

  const contentToRegenerate = typeof index === 'number' ? resume[section][index] : resume[section];
  try {
    const requestBody = {
      resume: contentToRegenerate,
      key: section,
      suggestion: promptText
    };

    if (typeof index === 'number') {
      requestBody.index = index;
    }

    const response = await fetch('http://127.0.0.1:5000/regeneration', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    setResume((prev) => {
      if (typeof index === 'number') {
        // Update only the edited item within the array section
        const updatedSection = [...prev[section]];
        updatedSection[index] = result.refined_resume; // Updated content received from backend
        return {
          ...prev,
          [section]: updatedSection
        };
      } else {
        // Update the entire section for non-array types
        return {
          ...prev,
          [section]: result.refined_resume // Updated content received from backend
        };
      }
    });

    setIsLoading(false); // Stop loading after response is handled
  } catch (error) {
    console.error('Failed to regenerate section:', error);
  }
};


  const handlePromptChange = (section, value, index = null) => {
    setPrompts((prev) => {
      if (typeof index === 'number') {
        // For array sections, update the specific prompt for the item
        const updatedPrompts = [...prev[section]];
        updatedPrompts[index] = value;
        return { ...prev, [section]: updatedPrompts };
      } else {
        // For string and object sections, update the prompt for the entire section
        return { ...prev, [section]: value };
      }
    });
  };
  const handleGeneratePDF = () => {
    console.log('Generating PDF...');
    // Implement PDF generation logic
  };
  // Render the content of each resume section
const renderSectionContent = (sectionContent, sectionKey) => {
  if (Array.isArray(sectionContent)) {
    return sectionContent.map((item, index) => (
      <div key={index} className="section-content">
        <h4>{sectionKey} {index + 1}</h4>
        {Object.entries(item).map(([key, value]) => {
          // Check if the key is 'description' to render it as bullet points
          if (key === 'description' && Array.isArray(value)) {
            return (
              <div key={key} className="item">
                <span className="key">{key}:</span>
                <ul className="value">
                  {value.map((point, idx) => (
                    <li key={idx}>{point}</li>
                  ))}
                </ul>
              </div>
            );
          } else if (Array.isArray(value)) {
            return (
              <div key={key} className="item">
                <span className="key">{key}:</span>
                <ul className="value">
                  {value.map((val, idx) => <li key={idx}>{val}</li>)}
                </ul>
              </div>
            );
          } else {
            return (
              <div key={key} className="item">
                <span className="key">{key}:</span>
                <span className="value">{value}</span>
              </div>
            );
          }
        })}
        <textarea
          value={prompts[sectionKey][index]}
          onChange={(e) => handlePromptChange(sectionKey, e.target.value, index)}
          placeholder={`Enter prompt to refine your ${sectionKey}`}
        />
        <button
          onClick={() => handleRegenerate(sectionKey, index)}
          disabled={isLoading}
        >
          {isLoading ? 'Loading...' : 'Regenerate section'}
        </button>
      </div>
    ));
  }  else {
      return (
        <>
          <span>{sectionContent}</span>
          <textarea
            value={prompts[sectionKey]}
            onChange={(e) => handlePromptChange(sectionKey, e.target.value)}
            placeholder={`Enter prompt to refine your ${sectionKey}`}
          />
          <button
            onClick={() => handleRegenerate(sectionKey)}
            disabled={isLoading}
          >
            {isLoading ? 'Loading...' : 'Regenerate section'}
          </button>
        </>
      );
    }
  };

  return (
    <div className="refined-resume">
      {Object.keys(resume).map((sectionKey) => (
        <div key={sectionKey} className="resume-section">
          <h3>{sectionKey.charAt(0).toUpperCase() + sectionKey.slice(1)}</h3>
          {renderSectionContent(resume[sectionKey], sectionKey)}
        </div>
      ))}
      <button onClick={() => navigate('/')}>Upload Another Resume</button>
      <button onClick={handleGeneratePDF}>Generate PDF</button>
    </div>
  );
}

export default RefinedResume;

// Add your handleGeneratePDF function or any other necessary code as needed
