// Esri basemap tiles, through Spot-a-Crop's own ArcGIS Location Platform keys (basemaps only).
// The key here is the website's, locked to spotacrop.com. tools/build-web.mjs swaps in the app's own
// key (kept out of git, in ~/spotacrop-voices/secrets/esri.key) for the iPhone build.
// Both expire 2027-10-28: make new ones in the ArcGIS dashboard before then.
export const ESRI_KEY = 'AAPTamGYBh3SmLYXOSZBeSd1qYg.._JQvSC8pFj8yIf-81SN_BDP4JwRZdgC82puqdxKWVi3KB5hR6DGKiS1d4dnEATOmt-K4OnnbZ9RwC7_TofxNk_7EAXRQq-eYmezVD4alAwIU4fWtcjhQ8MDKrfSIzOXVW0jl5AgaUqou3LWxUGRuviTw7f8xPIfZXFQs49Bg30E0sXx1kvHpnCyq8HIAJiYSuiVFu8uLoScUbFXQjihQh5iwm8aAc71sr9cPE36YcuM2UB235CBKn-a2AT1_y4451yJ0';
const STATIC = 'https://static-map-tiles-api.arcgis.com/arcgis/rest/services/static-basemap-tiles-service/v1';
export const imageryTile = (z, y, x) => `https://ibasemaps-api.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/${z}/${y}/${x}?token=${ESRI_KEY}`;
export const imageryUrl = imageryTile('{z}', '{y}', '{x}');
export const staticUrl = (style) => `${STATIC}/${style}/static/tile/{z}/{y}/{x}?token=${ESRI_KEY}`;
