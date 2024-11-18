import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FileList() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get('http://localhost:5000/file/files', {
          headers: {
            'x-access-tokens': 'your_token_here' 
          }
        });
        setFiles(response.data);
      } catch (error) {
        alert('Error fetching files');
      }
    };

    fetchFiles();
  }, []);

  return (
    <ul>
      {files.map(file => (
        <li key={file.id}>{file.filename}</li>
      ))}
    </ul>
  );
}

export default FileList;
