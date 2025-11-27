import { useEffect, useState, useCallback } from 'react';
import { useAIStore } from '../store';
import api from '../services/api';
import type { AIConfig, AIProviderInfo, AIFeatureInfo, AIConfigCreate, AIFeatureId } from '../types';
import './AISettingsPage.css';

const AISettingsPage = () => {
  const { config, setConfig, setLoading, isLoading } = useAIStore();
  const [providers, setProviders] = useState<AIProviderInfo[]>([]);
  const [features, setFeatures] = useState<AIFeatureInfo[]>([]);
  const [formData, setFormData] = useState<AIConfigCreate>({
    provider: 'none',
    model: '',
    api_key: '',
    fallback_mode: 'prompt',
    allow_data_sharing: false,
    monthly_budget_usd: undefined,
    enabled_features: [],
  });
  const [showApiKey, setShowApiKey] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');

  const loadAIData = useCallback(async () => {
    setLoading(true);
    try {
      const [providersData, featuresData, configData] = await Promise.all([
        api.getAIProviders(),
        api.getAIFeatures(),
        api.getAIConfig(),
      ]);
      setProviders(providersData);
      setFeatures(featuresData);
      if (configData) {
        setConfig(configData);
      }
    } catch (error) {
      console.error('Failed to load AI data:', error);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setConfig]);

  useEffect(() => {
    loadAIData();
  }, [loadAIData]);

  useEffect(() => {
    if (config) {
      setFormData({
        provider: config.provider,
        model: config.model || '',
        api_key: '',
        fallback_mode: config.fallback_mode,
        allow_data_sharing: config.allow_data_sharing,
        monthly_budget_usd: config.monthly_budget_usd,
        enabled_features: config.enabled_features || [],
      });
    }
  }, [config]);

  const handleSave = async () => {
    setSaveStatus('saving');
    try {
      let savedConfig: AIConfig;
      if (config) {
        savedConfig = await api.updateAIConfig(formData);
      } else {
        savedConfig = await api.createAIConfig(formData);
      }
      setConfig(savedConfig);
      setSaveStatus('saved');
      setTimeout(() => setSaveStatus('idle'), 2000);
    } catch (error) {
      console.error('Failed to save AI config:', error);
      setSaveStatus('error');
      setTimeout(() => setSaveStatus('idle'), 3000);
    }
  };

  const handleProviderChange = (providerId: string) => {
    const provider = providers.find((p) => p.provider_id === providerId);
    setFormData({
      ...formData,
      provider: providerId as AIConfigCreate['provider'],
      model: provider?.models[0] || '',
    });
  };

  const handleFeatureToggle = (featureId: string) => {
    const currentFeatures = formData.enabled_features || [];
    const typedFeatureId = featureId as AIFeatureId;
    const newFeatures = currentFeatures.includes(typedFeatureId)
      ? currentFeatures.filter((f) => f !== featureId)
      : [...currentFeatures, typedFeatureId];
    setFormData({ ...formData, enabled_features: newFeatures });
  };

  const selectedProvider = providers.find((p) => p.provider_id === formData.provider);

  return (
    <div className="ai-settings-page">
      {/* Header */}
      <div className="page-header">
        <div className="header-content">
          <h1>🤖 AI Configuration</h1>
          <p>Configure AI providers and features for enhanced analysis capabilities</p>
        </div>
        <div className="header-actions">
          <button
            className={`save-btn ${saveStatus}`}
            onClick={handleSave}
            disabled={saveStatus === 'saving'}
          >
            {saveStatus === 'saving' && '⏳ Saving...'}
            {saveStatus === 'saved' && '✓ Saved'}
            {saveStatus === 'error' && '✕ Error'}
            {saveStatus === 'idle' && '💾 Save Configuration'}
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading AI configuration...</p>
        </div>
      ) : (
        <div className="settings-content">
          {/* AI Status Card */}
          <div className="status-card">
            <div className="status-indicator">
              <span
                className={`status-dot ${
                  config?.provider !== 'none' && config?.has_api_key ? 'active' : 'inactive'
                }`}
              ></span>
              <span className="status-text">
                {config?.provider !== 'none' && config?.has_api_key
                  ? 'AI Features Enabled'
                  : 'AI Features Disabled'}
              </span>
            </div>
            {config && (
              <div className="usage-info">
                <span className="usage-label">Monthly Usage:</span>
                <span className="usage-value">
                  ${config.current_month_usage_usd.toFixed(2)}
                  {config.monthly_budget_usd && ` / $${config.monthly_budget_usd}`}
                </span>
              </div>
            )}
          </div>

          {/* Provider Selection */}
          <section className="settings-section">
            <h2>Provider Selection</h2>
            <p className="section-description">
              Select your preferred AI provider. Each provider offers different models and capabilities.
            </p>

            <div className="provider-grid">
              {providers.map((provider) => (
                <div
                  key={provider.provider_id}
                  className={`provider-card ${
                    formData.provider === provider.provider_id ? 'selected' : ''
                  }`}
                  onClick={() => handleProviderChange(provider.provider_id)}
                >
                  <div className="provider-icon">
                    {provider.provider_id === 'openai' && '🧠'}
                    {provider.provider_id === 'anthropic' && '🤖'}
                    {provider.provider_id === 'local' && '💻'}
                    {provider.provider_id === 'none' && '❌'}
                  </div>
                  <div className="provider-info">
                    <h3>{provider.name}</h3>
                    <p>{provider.models.length} models available</p>
                    {provider.supports_streaming && (
                      <span className="badge">Streaming</span>
                    )}
                  </div>
                  <div className="provider-check">
                    {formData.provider === provider.provider_id && '✓'}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Model & API Key */}
          {formData.provider !== 'none' && (
            <section className="settings-section">
              <h2>Authentication</h2>

              <div className="form-grid">
                {selectedProvider && selectedProvider.models.length > 0 && (
                  <div className="form-group">
                    <label>Model</label>
                    <select
                      value={formData.model}
                      onChange={(e) =>
                        setFormData({ ...formData, model: e.target.value })
                      }
                    >
                      {selectedProvider.models.map((model) => (
                        <option key={model} value={model}>
                          {model}
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                {formData.provider !== 'local' && (
                  <div className="form-group">
                    <label>
                      API Key
                      {config?.has_api_key && (
                        <span className="key-status">✓ Key saved</span>
                      )}
                    </label>
                    <div className="api-key-input">
                      <input
                        type={showApiKey ? 'text' : 'password'}
                        value={formData.api_key}
                        onChange={(e) =>
                          setFormData({ ...formData, api_key: e.target.value })
                        }
                        placeholder={
                          config?.has_api_key
                            ? 'Enter new key to update'
                            : 'Enter your API key'
                        }
                      />
                      <button
                        type="button"
                        className="toggle-visibility"
                        onClick={() => setShowApiKey(!showApiKey)}
                      >
                        {showApiKey ? '👁️' : '👁️‍🗨️'}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </section>
          )}

          {/* Features */}
          <section className="settings-section">
            <h2>AI Features</h2>
            <p className="section-description">
              Enable or disable specific AI-powered features. Each feature has a fallback mode
              when AI is unavailable.
            </p>

            <div className="features-list">
              {features.map((feature) => (
                <div key={feature.feature_id} className="feature-item">
                  <div className="feature-toggle">
                    <input
                      type="checkbox"
                      id={feature.feature_id}
                      checked={formData.enabled_features?.includes(feature.feature_id)}
                      onChange={() => handleFeatureToggle(feature.feature_id)}
                      disabled={formData.provider === 'none'}
                    />
                    <label htmlFor={feature.feature_id}></label>
                  </div>
                  <div className="feature-info">
                    <h4>{feature.name}</h4>
                    <p>{feature.description}</p>
                    <div className="feature-modes">
                      <span className="mode ai-mode">
                        <strong>AI Mode:</strong> {feature.ai_mode}
                      </span>
                      <span className="mode fallback-mode">
                        <strong>Fallback:</strong> {feature.fallback_mode}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Settings */}
          <section className="settings-section">
            <h2>Behavior Settings</h2>

            <div className="form-grid">
              <div className="form-group">
                <label>Fallback Behavior</label>
                <select
                  value={formData.fallback_mode}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      fallback_mode: e.target.value as AIConfigCreate['fallback_mode'],
                    })
                  }
                >
                  <option value="auto">Auto - Use fallback automatically</option>
                  <option value="prompt">Prompt - Ask before using fallback</option>
                  <option value="block">Block - Disable if AI unavailable</option>
                </select>
              </div>

              <div className="form-group">
                <label>Monthly Budget (USD)</label>
                <input
                  type="number"
                  value={formData.monthly_budget_usd || ''}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      monthly_budget_usd: e.target.value
                        ? parseFloat(e.target.value)
                        : undefined,
                    })
                  }
                  placeholder="No limit"
                  min="0"
                  step="10"
                />
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={formData.allow_data_sharing}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        allow_data_sharing: e.target.checked,
                      })
                    }
                  />
                  Allow data sharing with AI provider for model improvement
                </label>
                <p className="help-text">
                  When disabled, your data will not be used to train AI models.
                </p>
              </div>
            </div>
          </section>

          {/* Warning Notice */}
          <div className="warning-notice">
            <span className="warning-icon">⚠️</span>
            <div className="warning-content">
              <h4>Security Notice</h4>
              <p>
                AI features process data through external services. Do not use AI features
                with classified or sensitive information. All AI interactions are logged
                for audit purposes.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AISettingsPage;
