-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'viewer',
    organization VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Countries table
CREATE TABLE IF NOT EXISTS countries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    iso_code VARCHAR(3) UNIQUE NOT NULL,
    iso_code_2 VARCHAR(2) UNIQUE NOT NULL,
    region VARCHAR(100),
    subregion VARCHAR(100),
    capital VARCHAR(255),
    population INTEGER,
    area_sq_km FLOAT,
    gdp_usd FLOAT,
    defense_budget_usd FLOAT,
    lat FLOAT,
    lng FLOAT,
    flag_url VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Military branches table
CREATE TABLE IF NOT EXISTS military_branches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    country_id UUID NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    branch_type VARCHAR(50) NOT NULL,
    personnel_active INTEGER,
    personnel_reserve INTEGER,
    personnel_paramilitary INTEGER,
    budget_usd FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Military equipment table
CREATE TABLE IF NOT EXISTS military_equipment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    branch_id UUID NOT NULL REFERENCES military_branches(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(255),
    quantity INTEGER DEFAULT 0,
    operational_percentage FLOAT,
    year_introduced INTEGER,
    country_of_origin VARCHAR(100),
    specifications JSONB DEFAULT '{}',
    confidence_rating FLOAT,
    source VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    classification VARCHAR(50) DEFAULT 'unclassified',
    region_focus VARCHAR(255),
    tags JSONB DEFAULT '[]',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scenarios table
CREATE TABLE IF NOT EXISTS scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    creator_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    scenario_type VARCHAR(50) DEFAULT 'conventional',
    status VARCHAR(50) DEFAULT 'draft',
    bounds_north FLOAT,
    bounds_south FLOAT,
    bounds_east FLOAT,
    bounds_west FLOAT,
    center_lat FLOAT,
    center_lng FLOAT,
    zoom_level INTEGER,
    participants JSONB DEFAULT '[]',
    forces JSONB DEFAULT '{}',
    objectives JSONB DEFAULT '[]',
    timeline JSONB DEFAULT '[]',
    map_layers JSONB DEFAULT '[]',
    annotations JSONB DEFAULT '[]',
    simulation_config JSONB DEFAULT '{}',
    results JSONB DEFAULT '{}',
    version INTEGER DEFAULT 1,
    parent_scenario_id UUID REFERENCES scenarios(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Configurations table
CREATE TABLE IF NOT EXISTS ai_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) DEFAULT 'none',
    model VARCHAR(100),
    api_key_encrypted TEXT,
    monthly_budget_usd FLOAT,
    current_month_usage_usd FLOAT DEFAULT 0.0,
    allow_data_sharing BOOLEAN DEFAULT FALSE,
    max_input_tokens INTEGER,
    fallback_mode VARCHAR(50) DEFAULT 'prompt',
    enabled_features JSONB DEFAULT '[]',
    feature_settings JSONB DEFAULT '{}',
    local_model_path VARCHAR(500),
    local_model_config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_countries_region ON countries(region);
CREATE INDEX idx_countries_iso_code ON countries(iso_code);
CREATE INDEX idx_military_branches_country ON military_branches(country_id);
CREATE INDEX idx_military_equipment_branch ON military_equipment(branch_id);
CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_scenarios_project ON scenarios(project_id);
CREATE INDEX idx_scenarios_creator ON scenarios(creator_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_countries_updated_at BEFORE UPDATE ON countries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_military_branches_updated_at BEFORE UPDATE ON military_branches FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_military_equipment_updated_at BEFORE UPDATE ON military_equipment FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_scenarios_updated_at BEFORE UPDATE ON scenarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ai_configurations_updated_at BEFORE UPDATE ON ai_configurations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
