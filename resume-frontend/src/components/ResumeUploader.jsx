import React, { useState } from 'react';
import './ResumeUploader.css';
import { useNavigate } from 'react-router-dom';

function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [resumeText, setResumeText] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('resume_pdf', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/parse_resume', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setResumeText(result.refinedResume);
      navigate('/refined', { state: { resumeText: result.refinedResume } });
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="resume-uploader">
      <form onSubmit={handleSubmit}>
        <div className="file-input-container">
          <label htmlFor="file-upload" className="custom-file-upload">
            Choose File
          </label>
          <input
            id="file-upload"
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.doc,.docx,.txt"
          />
          <span className="file-name">{fileName || 'No file chosen'}</span>
        </div>
        <button type="submit" className="button-primary">Refine Resume</button>
      </form>
      {resumeText && (
        <div className="resume-display">
          <h2>Refined Resume</h2>
          <p>{resumeText}</p>
        </div>
      )}
    </div>
  );
}

export default ResumeUploader;
