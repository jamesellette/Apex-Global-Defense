import { useEffect, useState, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useProjectStore } from '../store';
import api from '../services/api';
import type { Project, ProjectCreate } from '../types';
import './ProjectsPage.css';

const ProjectsPage = () => {
  const { projects, setProjects, isLoading, setLoading, addProject, removeProject } = useProjectStore();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const navigate = useNavigate();

  const loadProjects = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getProjects({ limit: 100 });
      setProjects(data);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setProjects]);

  useEffect(() => {
    loadProjects();
  }, [loadProjects]);

  const handleDeleteProject = async (projectId: string) => {
    if (!confirm('Are you sure you want to delete this project?')) return;
    try {
      await api.deleteProject(projectId);
      removeProject(projectId);
    } catch (error) {
      console.error('Failed to delete project:', error);
    }
  };

  const filteredProjects = projects.filter((project) => {
    const matchesSearch = project.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || project.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="projects-page">
      {/* Header */}
      <div className="page-header">
        <div className="header-content">
          <h1>📁 Projects</h1>
          <p>Manage your defense analysis projects and scenarios</p>
        </div>
        <button className="create-btn" onClick={() => setShowCreateModal(true)}>
          ➕ New Project
        </button>
      </div>

      {/* Filters */}
      <div className="filters-bar">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Search projects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label>Status:</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="draft">Draft</option>
            <option value="archived">Archived</option>
          </select>
        </div>
      </div>

      {/* Projects Grid */}
      {isLoading ? (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading projects...</p>
        </div>
      ) : filteredProjects.length === 0 ? (
        <div className="empty-state">
          <span className="empty-icon">📁</span>
          <h3>No Projects Yet</h3>
          <p>Create your first project to start analyzing defense scenarios</p>
          <button className="create-btn" onClick={() => setShowCreateModal(true)}>
            Create Project
          </button>
        </div>
      ) : (
        <div className="projects-grid">
          {filteredProjects.map((project) => (
            <div key={project.id} className="project-card">
              <div className="card-header">
                <div className="project-title">
                  <h3>{project.name}</h3>
                  <span className={`status-badge status-${project.status}`}>
                    {project.status}
                  </span>
                </div>
                <div className="card-actions">
                  <button
                    className="action-btn"
                    onClick={() => navigate(`/projects/${project.id}`)}
                  >
                    📝
                  </button>
                  <button
                    className="action-btn delete"
                    onClick={() => handleDeleteProject(project.id)}
                  >
                    🗑️
                  </button>
                </div>
              </div>

              <p className="project-description">
                {project.description || 'No description provided'}
              </p>

              <div className="project-meta">
                {project.region_focus && (
                  <span className="meta-item">
                    🌍 {project.region_focus}
                  </span>
                )}
                <span className="meta-item">
                  ⚔️ {project.scenarios?.length || 0} scenarios
                </span>
                <span className="meta-item classification">
                  🔒 {project.classification}
                </span>
              </div>

              {project.tags && project.tags.length > 0 && (
                <div className="project-tags">
                  {project.tags.map((tag) => (
                    <span key={tag} className="tag">
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              <div className="card-footer">
                <span className="timestamp">
                  Updated {new Date(project.updated_at).toLocaleDateString()}
                </span>
                <Link to={`/projects/${project.id}`} className="view-link">
                  View Details →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <CreateProjectModal
          onClose={() => setShowCreateModal(false)}
          onCreate={(project) => {
            addProject(project);
            setShowCreateModal(false);
          }}
        />
      )}
    </div>
  );
};

interface CreateProjectModalProps {
  onClose: () => void;
  onCreate: (project: Project) => void;
}

const CreateProjectModal: React.FC<CreateProjectModalProps> = ({ onClose, onCreate }) => {
  const [formData, setFormData] = useState<ProjectCreate>({
    name: '',
    description: '',
    classification: 'unclassified',
    region_focus: '',
    tags: [],
  });
  const [tagInput, setTagInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim()) {
      setError('Project name is required');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const project = await api.createProject(formData);
      onCreate(project);
    } catch {
      setError('Failed to create project');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags?.includes(tagInput.trim())) {
      setFormData({
        ...formData,
        tags: [...(formData.tags || []), tagInput.trim()],
      });
      setTagInput('');
    }
  };

  const handleRemoveTag = (tag: string) => {
    setFormData({
      ...formData,
      tags: formData.tags?.filter((t) => t !== tag),
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create New Project</h2>
          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {error && <div className="form-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="name">Project Name *</label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Enter project name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              value={formData.description || ''}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              placeholder="Describe the project objectives..."
              rows={3}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="classification">Classification</label>
              <select
                id="classification"
                value={formData.classification}
                onChange={(e) =>
                  setFormData({ ...formData, classification: e.target.value })
                }
              >
                <option value="unclassified">Unclassified</option>
                <option value="confidential">Confidential</option>
                <option value="secret">Secret</option>
                <option value="top_secret">Top Secret</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="region">Region Focus</label>
              <input
                type="text"
                id="region"
                value={formData.region_focus || ''}
                onChange={(e) =>
                  setFormData({ ...formData, region_focus: e.target.value })
                }
                placeholder="e.g., Middle East, Asia Pacific"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Tags</label>
            <div className="tags-input">
              <input
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
                placeholder="Add tag and press Enter"
              />
              <button type="button" onClick={handleAddTag}>
                Add
              </button>
            </div>
            {formData.tags && formData.tags.length > 0 && (
              <div className="tags-list">
                {formData.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                    <button type="button" onClick={() => handleRemoveTag(tag)}>
                      ×
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="modal-actions">
            <button type="button" className="cancel-btn" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="submit-btn" disabled={isSubmitting}>
              {isSubmitting ? 'Creating...' : 'Create Project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProjectsPage;
