import React, { useState } from 'react';
import './ResumeUploader.css';
import { useNavigate } from 'react-router-dom';

function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Added loading state
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

    setIsLoading(true); // Start loading

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
      console.log('Parsed Resume JSON:', result.refinedResume);
      navigate('/refined', { state: { resumeText: result.refinedResume } });
    } catch (error) {
      console.error('Error uploading file:', error);
    }

    setIsLoading(false); // Stop loading
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
            disabled={isLoading} // Disable input when loading
          />
          <span className="file-name">{fileName || (isLoading ? 'Loading...' : 'No file chosen')}</span>
        </div>
        <button type="submit" className="button-primary" disabled={isLoading}>
          {isLoading ? 'Processing...' : 'Refine Resume'}
        </button>
      </form>
    </div>
  );
}

export default ResumeUploader;
