import React, { useState } from 'react';
import axios from 'axios';

function UploadFile() {
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post('http://localhost:5000/file/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'x-access-tokens': 'your_token_here' 
        }
      });
      alert('File uploaded successfully');
    } catch (error) {
      alert('Error uploading file');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} required />
      <button type="submit">Upload File</button>
    </form>
  );
}

export default UploadFile;
