import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './RefinedResume.css';

function RefinedResume({ onRegenerate }) {
  const navigate = useNavigate();
  const [resume, setResume] = useState(() => {
    return{
    "header": {
        "name": "John Doe",
        "address": "1234 Elm St, Springfield, IL 62701",
        "email": "john.doe@email.com",
        "phone": "(555) 555-5555",
        "website": "johndoe.github.io"
    },
    "education": [
        {
            "school": "Emory University",
            "degree": "Bachelor of Science in Computer Science, Minor in Applied Math",
            "start": "August 2022",
            "end": "Present",
            "gpa": "3.8/4.0",
            "details": [
                "Dean's List: Spring 2023, Fall 2023",
                "Relevant Coursework: Data Structs. and Alg., Comp. Arch., Algs., Lin. Alg., ML, Comp. Ling.",
                "Awards/Distinctions: Phi Eta Sigma Honor Society, National Merit Scholar"
            ]
        }
    ],
    "experience": [
        {
            "company": "Emory Libraries, Computing Center at Cox Hall",
            "position": "Computing Center Technology Consultant",
            "location": "Atlanta, GA",
            "start": "August 2023",
            "end": "Present",
            "description": [
                "Maintain friendly environment free of technical difficulties for students and faculty by managing CCCH's A/V system",
                "Provide a secure, up-to-date online experience for 200+ students by servicing CCCH's 32 computers and 4 printers"
            ]
        },
        {
            "company": "Kerygma Digital",
            "position": "Software Engineer",
            "location": "Remote",
            "start": "June 2023",
            "end": "July 2023",
            "description": [
                "Reduced service response latency by 60% (~400 ms) by implementing a custom configurable time-to-live HTTP cache in order to create a more responsive experience for 5m+ users across 60,000+ Discord servers",
                "Decreased HTML and JSON cache usage by 99% and 39% by creating custom middleware to strip stored responses",
                "Leveraged knowledge in Java, MVC, REST, and Git to learn and work in C# with the ASP.NET framework"
            ]
        }
    ],
    "projects": [
        {
            "name": "Personal Website",
            "description": [
                "Researched, designed, and developed a personal portfolio website in order to showcase skills and learn front-end technology and design best-practices to support Project Emory and RIDEmory's front-end/design team"
            ],
            "website": "https://johndoe.github.io",
            "technologies": [
                "React + Vite",
                "TypeScript",
                "HTML/CSS",
                "Figma",
                "Git",
                "Firefox/Chrome Developer Tools"
            ]
        },
        {
            "name": "RIDEmory",
            "description": [
                "Build a comprehensive rideshare solution for Emory's students through a self-updating database of ride information",
                "Guided engineers through MongoDB GeoJSON indexing to filter search for nearby rides and current traffic times",
                "Used Java and Spring Boot to teach MVC/REST and promote collaboration within the project's back-end team"
            ],
            "website": "https://ridemory.com",
            "technologies": [
                "Java/Spring Boot",
                "MongoDB Atlas",
                "Python/Flask",
                "React",
                "Figma",
                "Git",
                "Google Maps/Routes API"
            ]
        }
    ],
    "extracurriculars": [
        {
            "organization": "Project Emory",
            "position": "Educational Director",
            "location": "Atlanta, GA",
            "start": "May 2023",
            "end": "Present",
            "description": [
                "Craft engaging Spring Boot, MongoDB, and Git curriculum to enhance the technical proficiency of 20+ members",
                "Provide working CS experience to 30+ students by establishing and running Emory's only open project-building club"
            ]
        },
        {
            "organization": "Emory Hack4Impact",
            "position": "Software Engineer",
            "location": "Atlanta, GA",
            "start": "December 2023",
            "end": "Present",
            "description": [
                "Design and develop an internal operations webpage including an announcements board, HR service page, personal dashboard, and resources page to provide Odyssey Family Consulting Center with a unified employee experience",
                "Leverage knowledge in Figma to design pages based on client specifications and JavaScript to implement pages"
            ]
        }
    ],
    "other": [
        {
            "title": "Software",
            "content": [
                "(proficient): Java, Git, JavaScript/TypeScript, HTML/CSS, Python",
                "(familiar): Shell, C, C#, Go"
            ]
        },
        {
            "title": "Interests",
            "content": [
                "Backpacking",
                "Volleyball",
                "Technical/Modded Minecraft",
                "Linux",
                "Performance Arts (Oboe and Guitar)"
            ]
        }
    ]
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
const renderSectionContent = (content) => {
  if (Array.isArray(content)) {
    return content.map((item, index) => (
      <div key={index} className="section-content">
        {Object.entries(item).map(([key, value]) => (
          Array.isArray(value)
            ? <div key={key} className="item"><span className="key">{key}:</span> <ul className="value">{value.map((val, idx) => <li key={idx}>{val}</li>)}</ul></div>
            : <div key={key} className="item"><span className="key">{key}:</span> <span className="value">{value}</span></div>
        ))}
      </div>
    ));
  } else {
    return (
      <div className="section-content">
        {Object.entries(content).map(([key, value]) => (
          <div key={key} className="item"><span className="key">{key}:</span> <span className="value">{value}</span></div>
        ))}
      </div>
    );
  }
};

   return (
    <div className="refined-resume">
      {Object.keys(resume).map((section) => (
        <div key={section} className="resume-section">
          <h3>{section.charAt(0).toUpperCase() + section.slice(1)}</h3>
          {renderSectionContent(resume[section])}
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