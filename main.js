import './style.css';
import {Map, View} from 'ol';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import LayerGroup from 'ol/layer/Group.js';
import Overlay from 'ol/Overlay.js';
import Geolocation from 'ol/Geolocation';
import {useGeographic} from 'ol/proj'; // Optional: Use geographic coordinates directly
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import CircleStyle from 'ol/style/Circle';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Style from 'ol/style/Style';

const fwsAreas = new VectorSource({
    url: 'https://storage.googleapis.com/grousemapper/clean_boundaries_2/NWR USFS Lands.geojson',
    format: new GeoJSON({

        featureProjection: 'EPSG:3857'
    }),
});

const fwsAreasLayer = new VectorLayer({
    source: fwsAreas,
});

const wildlifeManagementAreas = new VectorSource({
    url: 'https://storage.googleapis.com/grousemapper/clean_boundaries_2/WVDNR Managed Lands.geojson',
    format: new GeoJSON({
        featureProjection: 'EPSG:3857'
    }),
});

const wildlifeManagementAreasLayer = new VectorLayer({
    source: wildlifeManagementAreas,
});

const stateForests = new VectorSource({
    url: 'https://storage.googleapis.com/grousemapper/clean_boundaries_2/WV State Forest Lands.geojson',
    format: new GeoJSON({
        featureProjection: 'EPSG:3857'
    }),
});

const stateForestsLayer = new VectorLayer({
    source: stateForests,
});

const stateParks = new VectorSource({
    url: 'https://storage.googleapis.com/grousemapper/clean_boundaries_2/WV State Parks.geojson',
    format: new GeoJSON({
        featureProjection: 'EPSG:3857'
    }),
});

const stateParksLayer = new VectorLayer({
    source: stateParks,
});

const nationalParkService = new VectorSource({
    url: 'https://storage.googleapis.com/grousemapper/clean_boundaries_2/NPS Lands WV.geojson',
    format: new GeoJSON({
        featureProjection: 'EPSG:3857'
    }),
});

const nationalParkServiceLayer = new VectorLayer({
    source: nationalParkService,
});

const wildernessAreas = new VectorSource({
    url: 'https://storage.googleapis.com/grousemapper/clean_boundaries_2/WildernessAreas.geojson',
    format: new GeoJSON({
        featureProjection: 'EPSG:3857'
    }),
});

const wildernessAreasLayer = new VectorLayer({
    source: wildernessAreas,
});



// Group layer for boundaries
const boundariesMapGroup = new LayerGroup({
    visible: true,
    opacity: 1,
    title: 'Boundaries',
    layers: [fwsAreasLayer,
        wildlifeManagementAreasLayer,
        stateForestsLayer,
        stateParksLayer,
        nationalParkServiceLayer,
        wildernessAreasLayer]
});

// Context Layers
const suitabilityLayer = new ol.layer.Tile({
    source: new ol.source.XYZ({
        minZoom: 2,
        maxZoom: 15,
        url: 'https://storage.googleapis.com/grousemapper/suitability_tiles_clip_rgb/{z}/{x}/{-y}.png'
    },),
    visible: false
});


// Initialize baselayers
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
    layers: [osmLayer, satelliteLayer, terrainLayer, suitabilityLayer, boundariesMapGroup],
    view: new View({
        center: ol.proj.fromLonLat([-80.181745, 38.92017]), // Center of WV
        zoom: 7
    })
});

// Optional: Call useGeographic() to make the view use lat/lon coordinates
useGeographic();

const geolocation = new Geolocation({
    // enableHighAccuracy: true, // Optional: requests more accurate position
    tracking: true, // Start tracking the location immediately
    projection: map.getView().getProjection(), // Bind the geolocation to the map's projection
});

geolocation.on('change', function () {
    const coordinates = geolocation.getPosition();
    // Use the coordinates (e.g., diSsplay them in an HTML element)
    // Example: document.getElementById('coords').innerText = coordinates;
});

const positionFeature = new Feature({
    geometry: new Point([0, 0]),
});

const accuracyFeature = new Feature();

// Style the position marker
positionFeature.setStyle(
    new Style({
        image: new CircleStyle({
            radius: 6,
            fill: new Fill({
                color: '#3399CC',
            }),
            stroke: new Stroke({
                color: '#fff',
                width: 2,
            }),
        }),
    })
);

const ownLocation = new VectorLayer({
    source: new VectorSource({
        features: [positionFeature, accuracyFeature],
    }),
});

map.addLayer(ownLocation);


geolocation.on('change', function () {
    const coordinates = geolocation.getPosition();
    positionFeature.getGeometry().setCoordinates(coordinates);

    const accuracy = geolocation.getAccuracyGeometry();
    accuracyFeature.setGeometry(accuracy);
});


geolocation.on('error', function (error) {
    console.error(error.message);
    alert('Geolocation failed: ' + error.message);
});


// Layer control functionality
const layerMap = {
    'osm': osmLayer,
    'satellite': satelliteLayer,
    'terrain': terrainLayer,
    'suitability': suitabilityLayer,
    'boundaries': boundariesMapGroup
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


// popups
// Setup the Popup Overlay
const container = document.getElementById('popup');
const content = document.getElementById('popup-content');
const closer = document.getElementById('popup-closer');

const overlay = new Overlay({
    element: container,
    autoPan: {
        animation: {
            duration: 250
        }
    }
});
map.addOverlay(overlay);

// Hide popup when closer is clicked
closer.onclick = function () {
    overlay.setPosition(undefined);
    closer.blur();
    return false;
};

// --- 5. Handle Map Clicks for Overlapping Features ---
map.on('click', function (evt) {
    const coordinate = evt.coordinate;
    const features = map.getFeaturesAtPixel(evt.pixel);

    if (features.length > 0) {
        let popupContentHTML = '<h5>Public Land</h5>';

        // Iterate through all features found at the pixel
        features.forEach(function (feature) {
            const attributes = feature.getProperties();
            // Iterate through attributes and skip empty/null values
            if (attributes.Name !== undefined) {
                popupContentHTML += '<h4><u>' + attributes.Name + '</h4></u>';
                for (let key in attributes) {
                    // Ignore geometry or hidden fields
                    if (key === 'geometry') continue;
                    const value = attributes[key];
                    // Check if value is not empty, null, or undefined
                    if (value !== null && value !== undefined && value !== '' && key !== 'Source') {
                        popupContentHTML += '<b>' + key + ': </b>' + value + '<br>';
                    }
                }
            }
        });
        content.innerHTML = popupContentHTML;
        overlay.setPosition(coordinate); // Position the popup
    } else {
        // Hide popup if no feature is clicked
        overlay.setPosition(undefined);
        closer.blur();
    }
});