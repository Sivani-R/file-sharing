import React, { useState } from 'react';
import axios from 'axios';

function DownloadFile() {
  const [fileId, setFileId] = useState('');
  const [downloadLink, setDownloadLink] = useState('');

  const handleDownload = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/file/download/${fileId}`, {
        headers: {
          'x-access-tokens': 'your_token_here' 
        }
      });
      setDownloadLink(response.data['download-link']);
    } catch (error) {
      alert('Error fetching download link');
    }
  };

  return (
    <div>
      <input type="text" placeholder="File ID" value={fileId} onChange={(e) => setFileId(e.target.value)} required />
      <button onClick={handleDownload}>Get Download Link</button>
      {downloadLink && <a href={downloadLink} target="_blank" rel="noopener noreferrer">Download File</a>}
    </div>
  );
}

export default DownloadFile;
