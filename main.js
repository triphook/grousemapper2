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
    //url: 'https://openlayers.org/data/vector/ecoregions.json',
    url: 'https://services6.arcgis.com/cGI8zn9Oo7U9dF6z/arcgis/rest/services/WV_Public_Lands_pro/FeatureServer/0/query?where=1=1&outFields=*&f=geojson',
    format: new GeoJSON({
        //dataProjection: 'EPSG:26917',
        featureProjection: 'EPSG:3857'
    }),
});


const stateForestLayer = new VectorLayer({
    source: vectorSource,
});


const suitabilityLayer = new ol.layer.Tile({
    source: new ol.source.XYZ({
        minZoom: 2,
        maxZoom: 10,
        url: 'https://storage.googleapis.com/grousemapper/rugr_LC_3_tiles/{z}/{x}/{-y}.png'
    })
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
    layers: [osmLayer, satelliteLayer, terrainLayer, suitabilityLayer, stateForestLayer],
    view: new View({
        center: ol.proj.fromLonLat([-80.181745, 38.92017]), // Center of WV
        zoom: 7
    })
});


// Layer control functionality
const layerMap = {
    'osm': osmLayer,
    'satellite': satelliteLayer,
    'terrain': terrainLayer,
    'stateForest': stateForestLayer,
    'suitability': suitabilityLayer
};

//map.addLayer(osmLayer);
//map.addLayer(satelliteLayer);
//map.addLayer(terrainLayer);

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