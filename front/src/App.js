import React from 'react';
import { Layout } from 'antd';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import RequirementAnalysis from './pages/RequirementAnalysis';
import MultiAgentCollaboration from './pages/MultiAgentCollaboration';
import TestReports from './pages/TestReports';

const { Content } = Layout;

function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <Sidebar />
        <Layout>
          <Header />
          <Content style={{ 
            background: '#f5f5f5',
            padding: '24px'
          }}>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/reports" element={<TestReports />} />
              <Route path="/ai/requirement" element={<RequirementAnalysis />} />
              <Route path="/ai/multi-agent" element={<MultiAgentCollaboration />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </BrowserRouter>
  );
}

export default App;