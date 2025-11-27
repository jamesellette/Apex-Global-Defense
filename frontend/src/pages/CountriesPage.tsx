import { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { useCountryStore } from '../store';
import api from '../services/api';
import type { Country, ForceSummary } from '../types';
import './CountriesPage.css';

const CountriesPage = () => {
  const { countries, setCountries, isLoading, setLoading } = useCountryStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRegion, setSelectedRegion] = useState<string>('all');
  const [selectedCountry, setSelectedCountry] = useState<Country | null>(null);
  const [forceSummary, setForceSummary] = useState<ForceSummary | null>(null);
  const [sortBy, setSortBy] = useState<'name' | 'budget' | 'population'>('budget');

  const loadCountries = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getCountries({ limit: 100 });
      setCountries(data);
    } catch (error) {
      console.error('Failed to load countries:', error);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setCountries]);

  useEffect(() => {
    loadCountries();
  }, [loadCountries]);

  const loadForceSummary = async (countryId: string) => {
    try {
      const summary = await api.getCountryForceSummary(countryId);
      setForceSummary(summary);
    } catch (error) {
      console.error('Failed to load force summary:', error);
    }
  };

  const handleCountrySelect = async (country: Country) => {
    setSelectedCountry(country);
    await loadForceSummary(country.id);
  };

  const regions = ['all', ...new Set(countries.map((c) => c.region).filter(Boolean))];

  const filteredCountries = countries
    .filter((country) => {
      const matchesSearch =
        country.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        country.iso_code.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesRegion =
        selectedRegion === 'all' || country.region === selectedRegion;
      return matchesSearch && matchesRegion;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'budget':
          return (b.defense_budget_usd || 0) - (a.defense_budget_usd || 0);
        case 'population':
          return (b.population || 0) - (a.population || 0);
        default:
          return 0;
      }
    });

  const formatNumber = (num: number | undefined | null): string => {
    if (!num) return 'N/A';
    if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(1)}B`;
    if (num >= 1e6) return `${(num / 1e6).toFixed(1)}M`;
    return num.toLocaleString();
  };

  return (
    <div className="countries-page">
      {/* Header */}
      <div className="page-header">
        <div className="header-content">
          <h1>🌍 Global Military Database</h1>
          <p>Order of Battle for top military powers worldwide</p>
        </div>
        <div className="header-stats">
          <div className="stat-item">
            <span className="stat-value">{countries.length}</span>
            <span className="stat-label">Countries</span>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-bar">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Search countries..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label>Region:</label>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
          >
            {regions.map((region) => (
              <option key={region} value={region}>
                {region === 'all' ? 'All Regions' : region}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Sort by:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
          >
            <option value="budget">Defense Budget</option>
            <option value="name">Name</option>
            <option value="population">Population</option>
          </select>
        </div>
      </div>

      {/* Main Content */}
      <div className="countries-content">
        {/* Countries List */}
        <div className="countries-list">
          {isLoading ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Loading countries...</p>
            </div>
          ) : filteredCountries.length === 0 ? (
            <div className="empty-state">
              <span className="empty-icon">🌐</span>
              <p>No countries found</p>
            </div>
          ) : (
            <div className="countries-grid">
              {filteredCountries.map((country, index) => (
                <div
                  key={country.id}
                  className={`country-card ${
                    selectedCountry?.id === country.id ? 'selected' : ''
                  }`}
                  onClick={() => handleCountrySelect(country)}
                >
                  <div className="card-rank">#{index + 1}</div>
                  <div className="card-content">
                    <div className="country-header">
                      <h3>{country.name}</h3>
                      <span className="iso-code">{country.iso_code}</span>
                    </div>
                    <div className="country-stats">
                      <div className="stat">
                        <span className="label">Defense Budget</span>
                        <span className="value">
                          {formatNumber(country.defense_budget_usd)}
                        </span>
                      </div>
                      <div className="stat">
                        <span className="label">Population</span>
                        <span className="value">
                          {formatNumber(country.population)}
                        </span>
                      </div>
                    </div>
                    <div className="country-meta">
                      <span className="region-badge">{country.region}</span>
                      {country.capital && (
                        <span className="capital">📍 {country.capital}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Country Detail Panel */}
        {selectedCountry && (
          <div className="country-detail-panel">
            <div className="panel-header">
              <h2>{selectedCountry.name}</h2>
              <button onClick={() => setSelectedCountry(null)}>✕</button>
            </div>

            <div className="panel-content">
              {/* Basic Info */}
              <section className="detail-section">
                <h3>📊 Overview</h3>
                <div className="info-grid">
                  <div className="info-item">
                    <span className="label">ISO Code</span>
                    <span className="value">{selectedCountry.iso_code}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Capital</span>
                    <span className="value">{selectedCountry.capital || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Region</span>
                    <span className="value">{selectedCountry.region || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Subregion</span>
                    <span className="value">{selectedCountry.subregion || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Population</span>
                    <span className="value">{formatNumber(selectedCountry.population)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Area</span>
                    <span className="value">
                      {selectedCountry.area_sq_km?.toLocaleString()} km²
                    </span>
                  </div>
                </div>
              </section>

              {/* Economic Data */}
              <section className="detail-section">
                <h3>💰 Economic & Defense</h3>
                <div className="info-grid">
                  <div className="info-item highlight">
                    <span className="label">Defense Budget</span>
                    <span className="value">
                      {formatNumber(selectedCountry.defense_budget_usd)}
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="label">GDP</span>
                    <span className="value">{formatNumber(selectedCountry.gdp_usd)}</span>
                  </div>
                </div>
              </section>

              {/* Force Summary */}
              {forceSummary && (
                <section className="detail-section">
                  <h3>⚔️ Force Summary</h3>
                  <div className="force-grid">
                    <div className="force-item">
                      <span className="force-icon">👥</span>
                      <span className="force-value">
                        {forceSummary.total_personnel.toLocaleString()}
                      </span>
                      <span className="force-label">Total Personnel</span>
                    </div>
                    <div className="force-item">
                      <span className="force-icon">🪖</span>
                      <span className="force-value">
                        {forceSummary.active_personnel.toLocaleString()}
                      </span>
                      <span className="force-label">Active</span>
                    </div>
                    <div className="force-item">
                      <span className="force-icon">🎖️</span>
                      <span className="force-value">
                        {forceSummary.reserve_personnel.toLocaleString()}
                      </span>
                      <span className="force-label">Reserve</span>
                    </div>
                    <div className="force-item">
                      <span className="force-icon">🛡️</span>
                      <span className="force-value">{forceSummary.total_tanks}</span>
                      <span className="force-label">Tanks</span>
                    </div>
                    <div className="force-item">
                      <span className="force-icon">✈️</span>
                      <span className="force-value">{forceSummary.total_aircraft}</span>
                      <span className="force-label">Aircraft</span>
                    </div>
                    <div className="force-item">
                      <span className="force-icon">🚢</span>
                      <span className="force-value">{forceSummary.total_naval_vessels}</span>
                      <span className="force-label">Naval Vessels</span>
                    </div>
                  </div>
                </section>
              )}

              <div className="panel-actions">
                <Link to={`/map?focus=${selectedCountry.iso_code}`} className="action-btn">
                  🗺️ View on Map
                </Link>
                <button className="action-btn secondary">📊 Full Report</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CountriesPage;
