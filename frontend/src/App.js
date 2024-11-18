import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import UploadFile from './components/UploadFile';
import DownloadFile from './components/DownloadFile';
import FileList from './components/FileList';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/upload" element={<UploadFile />} />
          <Route path="/download" element={<DownloadFile />} />
          <Route path="/files" element={<FileList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
