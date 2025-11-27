import { useEffect, useRef, useState, useCallback } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { useMapStore, useCountryStore } from '../store';
import api from '../services/api';
import type { Country } from '../types';
import './MapPage.css';

// Mapbox access token from environment variables
const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;
const isMapboxConfigured = Boolean(MAPBOX_TOKEN && !MAPBOX_TOKEN.startsWith('pk.placeholder'));

const MapPage = () => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const { viewState, setViewState, activeLayers, toggleLayer } = useMapStore();
  const { setCountries, selectedCountry, setSelectedCountry } = useCountryStore();
  const [isLoading, setIsLoading] = useState(isMapboxConfigured);
  const [mapStyle, setMapStyle] = useState<'dark' | 'satellite' | 'light'>('dark');

  const addCountryMarkers = useCallback((countryData: Country[]) => {
    if (!map.current) return;

    countryData.forEach((country) => {
      if (!country.lat || !country.lng) return;

      // Create marker element
      const el = document.createElement('div');
      el.className = 'country-marker';
      el.innerHTML = `
        <div class="marker-dot"></div>
        <div class="marker-label">${country.iso_code}</div>
      `;

      // Add popup
      const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(`
        <div class="country-popup">
          <h3>${country.name}</h3>
          <p><strong>Capital:</strong> ${country.capital || 'N/A'}</p>
          <p><strong>Defense Budget:</strong> $${((country.defense_budget_usd || 0) / 1e9).toFixed(1)}B</p>
          <p><strong>Population:</strong> ${((country.population || 0) / 1e6).toFixed(1)}M</p>
          <p><strong>Region:</strong> ${country.region || 'N/A'}</p>
        </div>
      `);

      // Add marker to map
      new mapboxgl.Marker(el)
        .setLngLat([country.lng, country.lat])
        .setPopup(popup)
        .addTo(map.current!);

      el.addEventListener('click', () => {
        setSelectedCountry(country);
      });
    });
  }, [setSelectedCountry]);

  const loadCountryData = useCallback(async () => {
    try {
      const data = await api.getCountries({ limit: 50 });
      setCountries(data);
      addCountryMarkers(data);
    } catch (error) {
      console.error('Failed to load countries:', error);
    }
  }, [setCountries, addCountryMarkers]);

  useEffect(() => {
    // Skip map initialization if Mapbox is not configured
    if (!isMapboxConfigured || !mapContainer.current || map.current) return;

    // Initialize map
    mapboxgl.accessToken = MAPBOX_TOKEN!;

    const styles: Record<string, string> = {
      dark: 'mapbox://styles/mapbox/dark-v11',
      satellite: 'mapbox://styles/mapbox/satellite-streets-v12',
      light: 'mapbox://styles/mapbox/light-v11',
    };

    try {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: styles[mapStyle],
        center: [viewState.longitude, viewState.latitude],
        zoom: viewState.zoom,
        pitch: viewState.pitch || 0,
        bearing: viewState.bearing || 0,
      });

      // Add navigation controls
      map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');
      map.current.addControl(new mapboxgl.ScaleControl(), 'bottom-left');
      map.current.addControl(
        new mapboxgl.GeolocateControl({
          positionOptions: { enableHighAccuracy: true },
          trackUserLocation: true,
        }),
        'top-right'
      );

    map.current.on('load', () => {
      setIsLoading(false);
      loadCountryData();
    });

    map.current.on('error', (e) => {
      console.error('Map error:', e);
      setIsLoading(false);
    });

    map.current.on('moveend', () => {
      if (!map.current) return;
      const center = map.current.getCenter();
      setViewState({
        latitude: center.lat,
        longitude: center.lng,
        zoom: map.current.getZoom(),
        bearing: map.current.getBearing(),
        pitch: map.current.getPitch(),
      });
    });
    } catch (error) {
      console.error('Failed to initialize map:', error);
      // If map fails to initialize, it's likely a token issue
      setIsLoading(false);
    }

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, [mapStyle, viewState, setViewState, loadCountryData]);

  const handleStyleChange = (style: 'dark' | 'satellite' | 'light') => {
    if (!map.current) return;
    setMapStyle(style);
    
    const styles: Record<string, string> = {
      dark: 'mapbox://styles/mapbox/dark-v11',
      satellite: 'mapbox://styles/mapbox/satellite-streets-v12',
      light: 'mapbox://styles/mapbox/light-v11',
    };

    map.current.setStyle(styles[style]);
  };

  const handleFlyTo = (lng: number, lat: number, zoom = 5) => {
    if (!map.current) return;
    map.current.flyTo({
      center: [lng, lat],
      zoom,
      duration: 2000,
    });
  };

  const layerOptions = [
    { id: 'countries', label: 'Country Markers', icon: '📍' },
    { id: 'military', label: 'Military Bases', icon: '🏛️' },
    { id: 'conflicts', label: 'Conflict Zones', icon: '⚔️' },
    { id: 'infrastructure', label: 'Infrastructure', icon: '🏭' },
    { id: 'population', label: 'Population Density', icon: '👥' },
  ];

  // Show error message if Mapbox is not configured
  if (!isMapboxConfigured) {
    return (
      <div className="map-page">
        <div className="map-error">
          <div className="error-icon">🗺️</div>
          <h2>Map Configuration Required</h2>
          <p>Mapbox token not configured. Please set VITE_MAPBOX_TOKEN environment variable.</p>
          <div className="error-instructions">
            <h3>Setup Instructions:</h3>
            <ol>
              <li>Create a free account at <a href="https://mapbox.com" target="_blank" rel="noopener noreferrer">mapbox.com</a></li>
              <li>Get your public access token from the dashboard</li>
              <li>Create a <code>.env</code> file in the frontend directory</li>
              <li>Add: <code>VITE_MAPBOX_TOKEN=your_token_here</code></li>
              <li>Restart the development server</li>
            </ol>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="map-page">
      {/* Map Container */}
      <div ref={mapContainer} className="map-container">
        {isLoading && (
          <div className="map-loading">
            <div className="loading-spinner"></div>
            <p>Loading map...</p>
          </div>
        )}
      </div>

      {/* Map Controls Panel */}
      <div className="map-controls-panel">
        <div className="control-section">
          <h3>Map Style</h3>
          <div className="style-buttons">
            <button
              className={mapStyle === 'dark' ? 'active' : ''}
              onClick={() => handleStyleChange('dark')}
            >
              🌙 Dark
            </button>
            <button
              className={mapStyle === 'satellite' ? 'active' : ''}
              onClick={() => handleStyleChange('satellite')}
            >
              🛰️ Satellite
            </button>
            <button
              className={mapStyle === 'light' ? 'active' : ''}
              onClick={() => handleStyleChange('light')}
            >
              ☀️ Light
            </button>
          </div>
        </div>

        <div className="control-section">
          <h3>Layers</h3>
          <div className="layer-toggles">
            {layerOptions.map((layer) => (
              <label key={layer.id} className="layer-toggle">
                <input
                  type="checkbox"
                  checked={activeLayers.includes(layer.id)}
                  onChange={() => toggleLayer(layer.id)}
                />
                <span className="layer-icon">{layer.icon}</span>
                <span className="layer-label">{layer.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="control-section">
          <h3>Quick Navigation</h3>
          <div className="nav-buttons">
            <button onClick={() => handleFlyTo(-77.04, 38.90, 5)}>
              🇺🇸 USA
            </button>
            <button onClick={() => handleFlyTo(37.62, 55.75, 5)}>
              🇷🇺 Russia
            </button>
            <button onClick={() => handleFlyTo(116.40, 39.90, 5)}>
              🇨🇳 China
            </button>
            <button onClick={() => handleFlyTo(77.21, 28.61, 5)}>
              🇮🇳 India
            </button>
            <button onClick={() => handleFlyTo(0, 20, 2)}>
              🌍 Global View
            </button>
          </div>
        </div>
      </div>

      {/* Selected Country Panel */}
      {selectedCountry && (
        <div className="country-panel">
          <div className="panel-header">
            <h3>{selectedCountry.name}</h3>
            <button onClick={() => setSelectedCountry(null)}>✕</button>
          </div>
          <div className="panel-content">
            <div className="info-row">
              <span className="label">ISO Code</span>
              <span className="value">{selectedCountry.iso_code}</span>
            </div>
            <div className="info-row">
              <span className="label">Capital</span>
              <span className="value">{selectedCountry.capital || 'N/A'}</span>
            </div>
            <div className="info-row">
              <span className="label">Region</span>
              <span className="value">{selectedCountry.region || 'N/A'}</span>
            </div>
            <div className="info-row">
              <span className="label">Population</span>
              <span className="value">
                {((selectedCountry.population || 0) / 1e6).toFixed(1)}M
              </span>
            </div>
            <div className="info-row">
              <span className="label">Defense Budget</span>
              <span className="value highlight">
                ${((selectedCountry.defense_budget_usd || 0) / 1e9).toFixed(1)}B
              </span>
            </div>
            <div className="info-row">
              <span className="label">GDP</span>
              <span className="value">
                ${((selectedCountry.gdp_usd || 0) / 1e12).toFixed(2)}T
              </span>
            </div>
            <button
              className="view-details-btn"
              onClick={() => handleFlyTo(selectedCountry.lng!, selectedCountry.lat!, 6)}
            >
              📍 Focus on Map
            </button>
          </div>
        </div>
      )}

      {/* Map Legend */}
      <div className="map-legend">
        <h4>Legend</h4>
        <div className="legend-item">
          <span className="legend-dot blue"></span>
          <span>Country Capital</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot red"></span>
          <span>Conflict Zone</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot green"></span>
          <span>Military Base</span>
        </div>
      </div>
    </div>
  );
};

export default MapPage;
