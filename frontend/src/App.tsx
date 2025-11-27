import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useAuthStore } from './store';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import MapPage from './pages/MapPage';
import CountriesPage from './pages/CountriesPage';
import ProjectsPage from './pages/ProjectsPage';
import AISettingsPage from './pages/AISettingsPage';
import './App.css';

// Auth event listener component to handle API 401 responses
const AuthEventListener: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleUnauthorized = (event: CustomEvent<{ redirect: string }>) => {
      navigate(event.detail.redirect, { replace: true });
    };

    window.addEventListener('auth:unauthorized', handleUnauthorized as EventListener);
    return () => {
      window.removeEventListener('auth:unauthorized', handleUnauthorized as EventListener);
    };
  }, [navigate]);

  return null;
};

// Protected Route component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

// Public Route component (redirects to dashboard if already authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return <>{children}</>;
};

function App() {
  return (
    <BrowserRouter>
      <AuthEventListener />
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        {/* Protected routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="map" element={<MapPage />} />
          <Route path="countries" element={<CountriesPage />} />
          <Route path="countries/:id" element={<CountriesPage />} />
          <Route path="projects" element={<ProjectsPage />} />
          <Route path="projects/:id" element={<ProjectsPage />} />
          <Route path="scenarios" element={<ProjectsPage />} />
          <Route path="ai-settings" element={<AISettingsPage />} />
        </Route>

        {/* Catch all - redirect to dashboard */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
