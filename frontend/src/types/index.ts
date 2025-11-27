// User types
export interface User {
  id: string;
  email: string;
  full_name: string;
  organization?: string;
  role: UserRole;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export type UserRole = 'admin' | 'analyst' | 'reviewer' | 'commander' | 'viewer';

export interface UserCreate {
  email: string;
  full_name: string;
  password: string;
  organization?: string;
  role?: UserRole;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// Country types
export interface Country {
  id: string;
  name: string;
  iso_code: string;
  iso_code_2: string;
  region?: string;
  subregion?: string;
  capital?: string;
  population?: number;
  area_sq_km?: number;
  gdp_usd?: number;
  defense_budget_usd?: number;
  lat?: number;
  lng?: number;
  flag_url?: string;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  military_branches?: MilitaryBranch[];
}

export interface MilitaryBranch {
  id: string;
  country_id: string;
  name: string;
  branch_type: BranchType;
  personnel_active?: number;
  personnel_reserve?: number;
  personnel_paramilitary?: number;
  budget_usd?: number;
  created_at: string;
  updated_at: string;
  equipment?: MilitaryEquipment[];
}

export type BranchType =
  | 'army'
  | 'navy'
  | 'air_force'
  | 'marines'
  | 'space_force'
  | 'coast_guard'
  | 'special_operations'
  | 'cyber'
  | 'other';

export interface MilitaryEquipment {
  id: string;
  branch_id: string;
  category: EquipmentCategory;
  name: string;
  model?: string;
  quantity: number;
  operational_percentage?: number;
  year_introduced?: number;
  country_of_origin?: string;
  specifications?: Record<string, unknown>;
  confidence_rating?: number;
  source?: string;
  created_at: string;
  updated_at: string;
}

export type EquipmentCategory =
  | 'tanks'
  | 'armored_vehicles'
  | 'artillery'
  | 'mlrs'
  | 'aircraft_fighter'
  | 'aircraft_attack'
  | 'aircraft_transport'
  | 'helicopters_attack'
  | 'helicopters_transport'
  | 'naval_carriers'
  | 'naval_destroyers'
  | 'naval_frigates'
  | 'naval_submarines'
  | 'naval_patrol'
  | 'missiles_ballistic'
  | 'missiles_cruise'
  | 'drones'
  | 'other';

export interface ForceSummary {
  total_personnel: number;
  active_personnel: number;
  reserve_personnel: number;
  paramilitary_personnel: number;
  total_tanks: number;
  total_aircraft: number;
  total_naval_vessels: number;
  defense_budget_usd?: number;
}

// Project types
export interface Project {
  id: string;
  owner_id: string;
  name: string;
  description?: string;
  status: ProjectStatus;
  classification: string;
  region_focus?: string;
  tags?: string[];
  settings?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  scenarios?: Scenario[];
}

export type ProjectStatus = 'active' | 'archived' | 'draft';

export interface ProjectCreate {
  name: string;
  description?: string;
  classification?: string;
  region_focus?: string;
  tags?: string[];
  settings?: Record<string, unknown>;
}

// Scenario types
export interface Scenario {
  id: string;
  project_id: string;
  creator_id: string;
  name: string;
  description?: string;
  scenario_type: ScenarioType;
  status: ScenarioStatus;
  bounds_north?: number;
  bounds_south?: number;
  bounds_east?: number;
  bounds_west?: number;
  center_lat?: number;
  center_lng?: number;
  zoom_level?: number;
  participants?: ScenarioParticipant[];
  forces?: Record<string, unknown>;
  objectives?: ScenarioObjective[];
  timeline?: TimelineEvent[];
  map_layers?: MapLayer[];
  annotations?: MapAnnotation[];
  simulation_config?: Record<string, unknown>;
  results?: Record<string, unknown>;
  version: number;
  parent_scenario_id?: string;
  created_at: string;
  updated_at: string;
}

export type ScenarioType =
  | 'conventional'
  | 'asymmetric'
  | 'cyber'
  | 'cbrn'
  | 'terror_response'
  | 'hybrid';

export type ScenarioStatus = 'draft' | 'active' | 'completed' | 'archived';

export interface ScenarioParticipant {
  country_id: string;
  country_name: string;
  role: 'red' | 'blue' | 'neutral';
  forces?: Record<string, number>;
}

export interface ScenarioObjective {
  id: string;
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'in_progress' | 'achieved' | 'failed';
  assigned_to?: string;
}

export interface TimelineEvent {
  id: string;
  timestamp: string;
  title: string;
  description?: string;
  type: 'action' | 'event' | 'milestone';
}

export interface MapLayer {
  id: string;
  name: string;
  type: 'political' | 'topographic' | 'infrastructure' | 'population' | 'custom';
  visible: boolean;
  opacity: number;
  source_url?: string;
}

export interface MapAnnotation {
  id: string;
  type: 'marker' | 'line' | 'polygon' | 'circle' | 'text';
  coordinates: number[] | number[][];
  properties: Record<string, unknown>;
  style?: Record<string, unknown>;
}

export interface ScenarioCreate {
  name: string;
  description?: string;
  scenario_type?: ScenarioType;
  project_id: string;
  bounds_north?: number;
  bounds_south?: number;
  bounds_east?: number;
  bounds_west?: number;
  center_lat?: number;
  center_lng?: number;
  zoom_level?: number;
  participants?: ScenarioParticipant[];
  forces?: Record<string, unknown>;
  objectives?: ScenarioObjective[];
}

// AI Configuration types
export interface AIConfig {
  id: string;
  user_id: string;
  provider: AIProvider;
  model?: string;
  fallback_mode: FallbackMode;
  allow_data_sharing: boolean;
  monthly_budget_usd?: number;
  current_month_usage_usd: number;
  max_input_tokens?: number;
  enabled_features?: AIFeatureId[];
  feature_settings?: Record<string, unknown>;
  local_model_path?: string;
  local_model_config?: Record<string, unknown>;
  has_api_key: boolean;
  created_at: string;
  updated_at: string;
}

export type AIProvider = 'openai' | 'anthropic' | 'local' | 'none';
export type FallbackMode = 'auto' | 'prompt' | 'block';

export type AIFeatureId =
  | 'intelligence_analysis'
  | 'scenario_generation'
  | 'threat_assessment'
  | 'report_generation'
  | 'translation';

export interface AIFeatureInfo {
  feature_id: AIFeatureId;
  name: string;
  description: string;
  ai_mode: string;
  fallback_mode: string;
  requires_api_key: boolean;
}

export interface AIProviderInfo {
  provider_id: AIProvider;
  name: string;
  models: string[];
  supports_streaming: boolean;
  max_tokens?: number;
}

export interface AIConfigCreate {
  provider?: AIProvider;
  model?: string;
  api_key?: string;
  fallback_mode?: FallbackMode;
  allow_data_sharing?: boolean;
  monthly_budget_usd?: number;
  max_input_tokens?: number;
  enabled_features?: AIFeatureId[];
  feature_settings?: Record<string, unknown>;
  local_model_path?: string;
  local_model_config?: Record<string, unknown>;
}

export interface AIAnalysisRequest {
  feature: AIFeatureId;
  input_text: string;
  context?: Record<string, unknown>;
  options?: Record<string, unknown>;
}

export interface AIAnalysisResponse {
  feature: AIFeatureId;
  result: string | Record<string, unknown>;
  tokens_used: number;
  cost_usd: number;
  provider: AIProvider;
  model?: string;
  is_fallback: boolean;
}

// Map types
export interface MapViewState {
  latitude: number;
  longitude: number;
  zoom: number;
  bearing?: number;
  pitch?: number;
}

export interface MapMarker {
  id: string;
  latitude: number;
  longitude: number;
  type: 'country' | 'base' | 'unit' | 'event' | 'custom';
  label?: string;
  icon?: string;
  color?: string;
  data?: Record<string, unknown>;
}

// API Response types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}
