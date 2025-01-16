import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router";

import Home from './pages/Home.jsx';
import Layout from './layout/Layout.jsx';

import './index.css';
import Metric from './pages/Metric.jsx';

import UserGuide from './pages/UserGuide.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/metric/:metricId" element={<Metric />} />
          <Route path="/userguide" element={<UserGuide />} /> 
          <Route path="*" element={<h1 >404 Not Found</h1>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
