import './style.css';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import ImageLayer from 'ol/layer/Image.js';
import TileLayer from 'ol/layer/Tile.js';
import ImageArcGISRest from 'ol/source/ImageArcGISRest.js';

const stateForestLayer = new ImageArcGISRest({
      ratio: 1,
      params: {},
      url: 'https://services6.arcgis.com/cGI8zn9Oo7U9dF6z/arcgis/rest/services/WV_Public_Lands_pro/FeatureServer/0',
    }),


// Initialize map layers
const osmLayer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: true
});

const satelliteLayer = new ol.layer.Tile({
    source: new ol.source.XYZ({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 19
    }),
    visible: false
});

const terrainLayer = new ol.layer.Tile({
    source: new ol.source.XYZ({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 19
    }),
    visible: false
});

// Create map
const map = new ol.Map({
    target: 'map',
    layers: [osmLayer, satelliteLayer, terrainLayer],
    view: new ol.View({
        center: ol.proj.fromLonLat([-98.5795, 39.8283]), // Center of USA
        zoom: 4
    })
});

// Layer control functionality
const layerMap = {
    'osm': osmLayer,
    'satellite': satelliteLayer,
    'terrain': stateForestLayer
};

document.querySelectorAll('.layer-item').forEach(item => {
    const layerName = item.dataset.layer;
    const layer = layerMap[layerName];
    const toggleSwitch = item.querySelector('.toggle-switch');
    const opacitySlider = item.querySelector('.opacity-slider');
    const opacityValue = item.querySelector('.opacity-value');

    // Toggle layer visibility
    item.querySelector('.layer-header').addEventListener('click', () => {
        const isVisible = layer.getVisible();
        layer.setVisible(!isVisible);
        toggleSwitch.classList.toggle('active');
    });

    // Control layer opacity
    opacitySlider.addEventListener('input', (e) => {
        const opacity = e.target.value / 100;
        layer.setOpacity(opacity);
        opacityValue.textContent = e.target.value + '%';
    });
});

// Add zoom controls
map.addControl(new ol.control.Zoom());
map.addControl(new ol.control.ScaleLine());