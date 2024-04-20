import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './RefinedResume.css';

function RefinedResume({ onRegenerate }) {
  const navigate = useNavigate();
  const [resume, setResume] = useState(() => {
    return {
      education: 'Bachelor of Science in Computer Science, Emory University, 2023',
      experience: 'Software Engineering Intern at Innovative StartUp, Developed an internal tool to streamline workflows.',
      skills: 'Proficient in Java, JavaScript, Python; experienced with React and Node.js',
      projects: 'Collaborative project on a social media analytics platform using machine learning to identify trends.'
    };
  });
  const [prompts, setPrompts] = useState(
    Object.keys(resume).reduce((acc, key) => ({ ...acc, [key]: '' }), {})
  );

  const handleRegenerate = async (section) => {
    if (onRegenerate) {
      // Send the prompt for this section to the backend for processing
      const updatedSection = await onRegenerate(section, prompts[section]);
      setResume(prev => ({
        ...prev,
        [section]: updatedSection
      }));
    }
  };

  const handlePromptChange = (section, value) => {
    setPrompts(prev => ({
      ...prev,
      [section]: value
    }));
  };
  const handleGeneratePDF = () => {
    window.open('backendurl', '_blank');
  };

  return (
      <div className="refined-resume">
        {Object.keys(resume).map((section) => (
            <div key={section} className="resume-section">
              <h3>{section.charAt(0).toUpperCase() + section.slice(1)}</h3>
              <p>{resume[section]}</p>
              <textarea
                  value={prompts[section]}
                  onChange={(e) => handlePromptChange(section, e.target.value)}
                  placeholder={`Enter prompt to refine your ${section}`}
              />
              <button onClick={() => handleRegenerate(section)}>Regenerate section</button>
            </div>
        ))}
        <button onClick={() => navigate('/')}>Upload Another Resume</button>
        <button onClick={handleGeneratePDF}>Generate PDF</button>
      </div>
  );
}

export default RefinedResume;
