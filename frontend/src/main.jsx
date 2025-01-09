import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router";

import Home from './pages/Home.jsx';
import Layout from './layout/Layout.jsx';

import './index.css';
import Metric from './pages/Metric.jsx';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ThemeProvider } from './layout/ThemeSelector.jsx';

const queryClient = new QueryClient();

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<Layout />}>
              <Route path="/" element={<Home />} />
              <Route path="/metric/:metricId" element={<Metric />} />
              <Route path="*" element={<h1 >404 Not Found</h1>} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  </StrictMode>
);
