import './style.css';
import {Map, View} from 'ol';
import OSM from 'ol/source/OSM';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import ImageLayer from 'ol/layer/Image';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';


// Tester
const vectorSource = new VectorSource({
  url: 'https://services6.arcgis.com/cGI8zn9Oo7U9dF6z/arcgis/rest/services/WV_Public_Lands_pro/FeatureServer/0/query?where=1=1&outFields=*&f=geojson',
  format: new GeoJSON(),
  //url: 'https://services6.arcgis.com/cGI8zn9Oo7U9dF6z/arcgis/rest/services/WV_Public_Lands_pro/FeatureServer/0/query?where=1=1&outFields=*&f=geojson', // Path to your GeoJSON file
});


var stateForestLayer = new VectorLayer({
  source: vectorSource,
});


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

const map = new Map({
  target: 'map',
  layers: [stateForestLayer],
  view: new View({
    center: ol.proj.fromLonLat([-80.181745, 38.92017]), // Center of USA
    zoom: 7
  })
});


// Layer control functionality
const layerMap = {
    'osm': osmLayer,
    'satellite': satelliteLayer,
    'terrain': terrainLayer,
    'stateForest': stateForestLayer
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