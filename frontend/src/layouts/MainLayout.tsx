import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore, useUIStore } from '../store';
import api from '../services/api';
import './MainLayout.css';

const MainLayout = () => {
  const { user, logout: clearAuth } = useAuthStore();
  const { sidebarOpen, toggleSidebar, theme } = useUIStore();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    api.logout();
    clearAuth();
    navigate('/login');
  };

  const navItems = [
    { path: '/dashboard', icon: '📊', label: 'Dashboard' },
    { path: '/map', icon: '🗺️', label: 'Global Map' },
    { path: '/countries', icon: '🌍', label: 'Countries' },
    { path: '/projects', icon: '📁', label: 'Projects' },
    { path: '/scenarios', icon: '⚔️', label: 'Scenarios' },
    { path: '/ai-settings', icon: '🤖', label: 'AI Settings' },
  ];

  return (
    <div className={`main-layout ${theme}`}>
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="logo">
            <span className="logo-icon">🛡️</span>
            {sidebarOpen && <span className="logo-text">AGD</span>}
          </div>
          <button className="toggle-btn" onClick={toggleSidebar}>
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          {sidebarOpen && user && (
            <div className="user-info">
              <span className="user-name">{user.full_name}</span>
              <span className="user-role">{user.role}</span>
            </div>
          )}
          <button className="logout-btn" onClick={handleLogout}>
            <span className="logout-icon">🚪</span>
            {sidebarOpen && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="main-content">
        <header className="top-bar">
          <div className="breadcrumb">
            <span className="app-name">Apex Global Defense</span>
            <span className="separator">/</span>
            <span className="current-page">
              {navItems.find((item) => item.path === location.pathname)?.label || 'Home'}
            </span>
          </div>

          <div className="top-bar-actions">
            <span className="classification-badge">UNCLASSIFIED</span>
            {user && (
              <span className="user-badge">
                {user.full_name} ({user.organization || 'No Org'})
              </span>
            )}
          </div>
        </header>

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
