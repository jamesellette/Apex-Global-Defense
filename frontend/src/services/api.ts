import axios, { type AxiosError, type AxiosInstance } from 'axios';
import type {
  User,
  UserCreate,
  Token,
  Country,
  MilitaryBranch,
  ForceSummary,
  Project,
  ProjectCreate,
  Scenario,
  ScenarioCreate,
  AIConfig,
  AIConfigCreate,
  AIFeatureInfo,
  AIProviderInfo,
  AIAnalysisRequest,
  AIAnalysisResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Load token from localStorage
    this.token = localStorage.getItem('access_token');

    // Request interceptor for auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.logout();
          // Dispatch custom event for navigation - can be handled by React components
          const event = new CustomEvent('auth:unauthorized', { detail: { redirect: '/login' } });
          window.dispatchEvent(event);
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth methods
  async register(data: UserCreate): Promise<User> {
    const response = await this.client.post<User>('/auth/register', data);
    return response.data;
  }

  async login(email: string, password: string): Promise<Token> {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await this.client.post<Token>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    this.token = response.data.access_token;
    localStorage.setItem('access_token', this.token);
    return response.data;
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('access_token');
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get<User>('/auth/me');
    return response.data;
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }

  // Country methods
  async getCountries(params?: {
    skip?: number;
    limit?: number;
    region?: string;
    search?: string;
  }): Promise<Country[]> {
    const response = await this.client.get<Country[]>('/countries/', { params });
    return response.data;
  }

  async getCountry(countryId: string): Promise<Country> {
    const response = await this.client.get<Country>(`/countries/${countryId}`);
    return response.data;
  }

  async getCountryByIso(isoCode: string): Promise<Country> {
    const response = await this.client.get<Country>(`/countries/iso/${isoCode}`);
    return response.data;
  }

  async getCountryForceSummary(countryId: string): Promise<ForceSummary> {
    const response = await this.client.get<ForceSummary>(
      `/countries/${countryId}/summary`
    );
    return response.data;
  }

  async getCountryBranches(countryId: string): Promise<MilitaryBranch[]> {
    const response = await this.client.get<MilitaryBranch[]>(
      `/countries/${countryId}/branches`
    );
    return response.data;
  }

  // Project methods
  async getProjects(params?: {
    skip?: number;
    limit?: number;
    status_filter?: string;
  }): Promise<Project[]> {
    const response = await this.client.get<Project[]>('/projects/', { params });
    return response.data;
  }

  async getProject(projectId: string): Promise<Project> {
    const response = await this.client.get<Project>(`/projects/${projectId}`);
    return response.data;
  }

  async createProject(data: ProjectCreate): Promise<Project> {
    const response = await this.client.post<Project>('/projects/', data);
    return response.data;
  }

  async updateProject(
    projectId: string,
    data: Partial<ProjectCreate>
  ): Promise<Project> {
    const response = await this.client.patch<Project>(
      `/projects/${projectId}`,
      data
    );
    return response.data;
  }

  async deleteProject(projectId: string): Promise<void> {
    await this.client.delete(`/projects/${projectId}`);
  }

  // Scenario methods
  async getScenarios(
    projectId: string,
    params?: { skip?: number; limit?: number }
  ): Promise<Scenario[]> {
    const response = await this.client.get<Scenario[]>(
      `/projects/${projectId}/scenarios`,
      { params }
    );
    return response.data;
  }

  async getScenario(projectId: string, scenarioId: string): Promise<Scenario> {
    const response = await this.client.get<Scenario>(
      `/projects/${projectId}/scenarios/${scenarioId}`
    );
    return response.data;
  }

  async createScenario(
    projectId: string,
    data: Omit<ScenarioCreate, 'project_id'>
  ): Promise<Scenario> {
    const response = await this.client.post<Scenario>(
      `/projects/${projectId}/scenarios`,
      { ...data, project_id: projectId }
    );
    return response.data;
  }

  async updateScenario(
    projectId: string,
    scenarioId: string,
    data: Partial<ScenarioCreate>
  ): Promise<Scenario> {
    const response = await this.client.patch<Scenario>(
      `/projects/${projectId}/scenarios/${scenarioId}`,
      data
    );
    return response.data;
  }

  async deleteScenario(projectId: string, scenarioId: string): Promise<void> {
    await this.client.delete(`/projects/${projectId}/scenarios/${scenarioId}`);
  }

  async branchScenario(
    projectId: string,
    scenarioId: string,
    newName: string
  ): Promise<Scenario> {
    const response = await this.client.post<Scenario>(
      `/projects/${projectId}/scenarios/${scenarioId}/branch`,
      null,
      { params: { new_name: newName } }
    );
    return response.data;
  }

  // AI Configuration methods
  async getAIProviders(): Promise<AIProviderInfo[]> {
    const response = await this.client.get<AIProviderInfo[]>('/ai/providers');
    return response.data;
  }

  async getAIFeatures(): Promise<AIFeatureInfo[]> {
    const response = await this.client.get<AIFeatureInfo[]>('/ai/features');
    return response.data;
  }

  async getAIConfig(): Promise<AIConfig | null> {
    const response = await this.client.get<AIConfig | null>('/ai/config');
    return response.data;
  }

  async createAIConfig(data: AIConfigCreate): Promise<AIConfig> {
    const response = await this.client.post<AIConfig>('/ai/config', data);
    return response.data;
  }

  async updateAIConfig(data: AIConfigCreate): Promise<AIConfig> {
    const response = await this.client.patch<AIConfig>('/ai/config', data);
    return response.data;
  }

  async deleteAIConfig(): Promise<void> {
    await this.client.delete('/ai/config');
  }

  async analyzeWithAI(data: AIAnalysisRequest): Promise<AIAnalysisResponse> {
    const response = await this.client.post<AIAnalysisResponse>(
      '/ai/analyze',
      data
    );
    return response.data;
  }
}

export const api = new ApiService();
export default api;
