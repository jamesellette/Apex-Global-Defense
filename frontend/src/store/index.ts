import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, Project, Scenario, Country, AIConfig, MapViewState } from '../types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      logout: () => set({ user: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);

interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  setProjects: (projects: Project[]) => void;
  setCurrentProject: (project: Project | null) => void;
  addProject: (project: Project) => void;
  updateProject: (project: Project) => void;
  removeProject: (projectId: string) => void;
  setLoading: (isLoading: boolean) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  projects: [],
  currentProject: null,
  isLoading: false,
  setProjects: (projects) => set({ projects }),
  setCurrentProject: (currentProject) => set({ currentProject }),
  addProject: (project) =>
    set((state) => ({ projects: [...state.projects, project] })),
  updateProject: (project) =>
    set((state) => ({
      projects: state.projects.map((p) => (p.id === project.id ? project : p)),
      currentProject:
        state.currentProject?.id === project.id ? project : state.currentProject,
    })),
  removeProject: (projectId) =>
    set((state) => ({
      projects: state.projects.filter((p) => p.id !== projectId),
      currentProject:
        state.currentProject?.id === projectId ? null : state.currentProject,
    })),
  setLoading: (isLoading) => set({ isLoading }),
}));

interface ScenarioState {
  scenarios: Scenario[];
  currentScenario: Scenario | null;
  isLoading: boolean;
  setScenarios: (scenarios: Scenario[]) => void;
  setCurrentScenario: (scenario: Scenario | null) => void;
  addScenario: (scenario: Scenario) => void;
  updateScenario: (scenario: Scenario) => void;
  removeScenario: (scenarioId: string) => void;
  setLoading: (isLoading: boolean) => void;
}

export const useScenarioStore = create<ScenarioState>((set) => ({
  scenarios: [],
  currentScenario: null,
  isLoading: false,
  setScenarios: (scenarios) => set({ scenarios }),
  setCurrentScenario: (currentScenario) => set({ currentScenario }),
  addScenario: (scenario) =>
    set((state) => ({ scenarios: [...state.scenarios, scenario] })),
  updateScenario: (scenario) =>
    set((state) => ({
      scenarios: state.scenarios.map((s) => (s.id === scenario.id ? scenario : s)),
      currentScenario:
        state.currentScenario?.id === scenario.id ? scenario : state.currentScenario,
    })),
  removeScenario: (scenarioId) =>
    set((state) => ({
      scenarios: state.scenarios.filter((s) => s.id !== scenarioId),
      currentScenario:
        state.currentScenario?.id === scenarioId ? null : state.currentScenario,
    })),
  setLoading: (isLoading) => set({ isLoading }),
}));

interface CountryState {
  countries: Country[];
  selectedCountry: Country | null;
  isLoading: boolean;
  setCountries: (countries: Country[]) => void;
  setSelectedCountry: (country: Country | null) => void;
  setLoading: (isLoading: boolean) => void;
}

export const useCountryStore = create<CountryState>((set) => ({
  countries: [],
  selectedCountry: null,
  isLoading: false,
  setCountries: (countries) => set({ countries }),
  setSelectedCountry: (selectedCountry) => set({ selectedCountry }),
  setLoading: (isLoading) => set({ isLoading }),
}));

interface MapState {
  viewState: MapViewState;
  selectedMarkerId: string | null;
  activeLayers: string[];
  setViewState: (viewState: MapViewState) => void;
  setSelectedMarkerId: (markerId: string | null) => void;
  toggleLayer: (layerId: string) => void;
  setActiveLayers: (layers: string[]) => void;
}

export const useMapStore = create<MapState>((set) => ({
  viewState: {
    latitude: 20,
    longitude: 0,
    zoom: 2,
  },
  selectedMarkerId: null,
  activeLayers: ['countries'],
  setViewState: (viewState) => set({ viewState }),
  setSelectedMarkerId: (selectedMarkerId) => set({ selectedMarkerId }),
  toggleLayer: (layerId) =>
    set((state) => ({
      activeLayers: state.activeLayers.includes(layerId)
        ? state.activeLayers.filter((id) => id !== layerId)
        : [...state.activeLayers, layerId],
    })),
  setActiveLayers: (activeLayers) => set({ activeLayers }),
}));

interface AIState {
  config: AIConfig | null;
  isEnabled: boolean;
  isLoading: boolean;
  setConfig: (config: AIConfig | null) => void;
  setLoading: (isLoading: boolean) => void;
}

export const useAIStore = create<AIState>((set) => ({
  config: null,
  isEnabled: false,
  isLoading: false,
  setConfig: (config) =>
    set({ config, isEnabled: config?.provider !== 'none' && config?.has_api_key }),
  setLoading: (isLoading) => set({ isLoading }),
}));

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  notifications: Notification[];
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
}

interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  theme: 'dark',
  notifications: [],
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
  setTheme: (theme) => set({ theme }),
  addNotification: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...notification, id: crypto.randomUUID() },
      ],
    })),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
}));
