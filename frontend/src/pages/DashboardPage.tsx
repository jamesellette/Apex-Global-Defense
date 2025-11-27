import { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore, useProjectStore, useCountryStore } from '../store';
import api from '../services/api';
import type { Project } from '../types';
import './Dashboard.css';

const DashboardPage = () => {
  const { user } = useAuthStore();
  const { setProjects, setLoading: setProjectsLoading } = useProjectStore();
  const { countries, setCountries, setLoading: setCountriesLoading } = useCountryStore();
  const [recentProjects, setRecentProjects] = useState<Project[]>([]);
  const [stats, setStats] = useState({
    totalCountries: 0,
    totalProjects: 0,
    activeScenarios: 0,
    pendingAnalyses: 0,
  });

  const loadDashboardData = useCallback(async () => {
    try {
      setProjectsLoading(true);
      setCountriesLoading(true);

      const [projectsData, countriesData] = await Promise.all([
        api.getProjects({ limit: 10 }),
        api.getCountries({ limit: 50 }),
      ]);

      setProjects(projectsData);
      setCountries(countriesData);
      setRecentProjects(projectsData.slice(0, 5));

      // Calculate stats
      const activeScenarios = projectsData.reduce(
        (count, p) => count + (p.scenarios?.filter((s) => s.status === 'active').length || 0),
        0
      );

      setStats({
        totalCountries: countriesData.length,
        totalProjects: projectsData.length,
        activeScenarios,
        pendingAnalyses: 0,
      });
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setProjectsLoading(false);
      setCountriesLoading(false);
    }
  }, [setProjectsLoading, setCountriesLoading, setProjects, setCountries]);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const statCards = [
    {
      title: 'Countries Tracked',
      value: stats.totalCountries,
      icon: '🌍',
      color: '#4a90d9',
      link: '/countries',
    },
    {
      title: 'Active Projects',
      value: stats.totalProjects,
      icon: '📁',
      color: '#28a745',
      link: '/projects',
    },
    {
      title: 'Active Scenarios',
      value: stats.activeScenarios,
      icon: '⚔️',
      color: '#ffc107',
      link: '/scenarios',
    },
    {
      title: 'Pending Analyses',
      value: stats.pendingAnalyses,
      icon: '🔬',
      color: '#dc3545',
      link: '/analyses',
    },
  ];

  const quickActions = [
    { title: 'New Project', icon: '➕', path: '/projects/new', color: '#4a90d9' },
    { title: 'View Map', icon: '🗺️', path: '/map', color: '#28a745' },
    { title: 'Country Intel', icon: '📊', path: '/countries', color: '#ffc107' },
    { title: 'AI Settings', icon: '🤖', path: '/ai-settings', color: '#9c27b0' },
  ];

  return (
    <div className="dashboard">
      {/* Welcome Section */}
      <section className="welcome-section">
        <div className="welcome-content">
          <h1>Welcome back, {user?.full_name?.split(' ')[0] || 'Analyst'}</h1>
          <p>Defense Intelligence Dashboard • Real-time strategic overview</p>
        </div>
        <div className="welcome-date">
          {new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          })}
        </div>
      </section>

      {/* Stats Grid */}
      <section className="stats-section">
        <div className="stats-grid">
          {statCards.map((stat) => (
            <Link to={stat.link} key={stat.title} className="stat-card">
              <div className="stat-icon" style={{ backgroundColor: `${stat.color}20` }}>
                <span>{stat.icon}</span>
              </div>
              <div className="stat-info">
                <span className="stat-value">{stat.value}</span>
                <span className="stat-title">{stat.title}</span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Quick Actions */}
      <section className="quick-actions-section">
        <h2>Quick Actions</h2>
        <div className="quick-actions-grid">
          {quickActions.map((action) => (
            <Link
              to={action.path}
              key={action.title}
              className="quick-action-card"
              style={{ borderColor: action.color }}
            >
              <span className="action-icon">{action.icon}</span>
              <span className="action-title">{action.title}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Main Content Grid */}
      <div className="dashboard-grid">
        {/* Recent Projects */}
        <section className="dashboard-card recent-projects">
          <div className="card-header">
            <h2>Recent Projects</h2>
            <Link to="/projects" className="view-all">
              View All →
            </Link>
          </div>
          <div className="card-content">
            {recentProjects.length > 0 ? (
              <ul className="project-list">
                {recentProjects.map((project) => (
                  <li key={project.id} className="project-item">
                    <Link to={`/projects/${project.id}`}>
                      <div className="project-info">
                        <span className="project-name">{project.name}</span>
                        <span className="project-meta">
                          {project.scenarios?.length || 0} scenarios •{' '}
                          {project.status}
                        </span>
                      </div>
                      <span
                        className={`status-badge status-${project.status}`}
                      >
                        {project.status}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="empty-state">
                <span className="empty-icon">📁</span>
                <p>No projects yet</p>
                <Link to="/projects/new" className="create-btn">
                  Create Your First Project
                </Link>
              </div>
            )}
          </div>
        </section>

        {/* Global Hotspots */}
        <section className="dashboard-card global-hotspots">
          <div className="card-header">
            <h2>Top Military Powers</h2>
            <Link to="/countries" className="view-all">
              View All →
            </Link>
          </div>
          <div className="card-content">
            <ul className="country-list">
              {countries.slice(0, 5).map((country, index) => (
                <li key={country.id} className="country-item">
                  <Link to={`/countries/${country.id}`}>
                    <span className="country-rank">#{index + 1}</span>
                    <div className="country-info">
                      <span className="country-name">{country.name}</span>
                      <span className="country-budget">
                        Defense: ${((country.defense_budget_usd || 0) / 1e9).toFixed(1)}B
                      </span>
                    </div>
                    <span className="country-region">{country.region}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Domain Overview */}
        <section className="dashboard-card domain-overview">
          <div className="card-header">
            <h2>Warfare Domains</h2>
          </div>
          <div className="card-content">
            <div className="domains-grid">
              <div className="domain-card">
                <span className="domain-icon">🏔️</span>
                <span className="domain-name">Land</span>
              </div>
              <div className="domain-card">
                <span className="domain-icon">✈️</span>
                <span className="domain-name">Air</span>
              </div>
              <div className="domain-card">
                <span className="domain-icon">🚢</span>
                <span className="domain-name">Sea</span>
              </div>
              <div className="domain-card">
                <span className="domain-icon">💻</span>
                <span className="domain-name">Cyber</span>
              </div>
              <div className="domain-card">
                <span className="domain-icon">☢️</span>
                <span className="domain-name">CBRN</span>
              </div>
              <div className="domain-card">
                <span className="domain-icon">🛰️</span>
                <span className="domain-name">Space</span>
              </div>
            </div>
          </div>
        </section>

        {/* System Status */}
        <section className="dashboard-card system-status">
          <div className="card-header">
            <h2>System Status</h2>
          </div>
          <div className="card-content">
            <ul className="status-list">
              <li className="status-item online">
                <span className="status-indicator"></span>
                <span className="status-name">API Services</span>
                <span className="status-value">Online</span>
              </li>
              <li className="status-item online">
                <span className="status-indicator"></span>
                <span className="status-name">Database</span>
                <span className="status-value">Connected</span>
              </li>
              <li className="status-item warning">
                <span className="status-indicator"></span>
                <span className="status-name">AI Services</span>
                <span className="status-value">Configure</span>
              </li>
              <li className="status-item online">
                <span className="status-indicator"></span>
                <span className="status-name">Map Tiles</span>
                <span className="status-value">Ready</span>
              </li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  );
};

export default DashboardPage;
