import * as THREE from 'three';
import { construire } from './decors.js';
import { creer, animer } from './animaux.js';

let renderer, camera, W = 1080, H = 1920;
const worlds = new Map(), rigs = new Map();

export function init(w, h) {
  W = w; H = h;
  const canvas = document.getElementById('c'); canvas.width = w; canvas.height = h;
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
  renderer.setSize(w, h, false); renderer.setPixelRatio(1);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  camera = new THREE.PerspectiveCamera(32, w / h, 0.1, 400);
}

// cadrages : hauteur visible (en unités), hauteur du point visé
const FR = { wide: { vis: 4.9, ly: 0.80 }, med: { vis: 3.7, ly: 0.66 }, close: { vis: 2.8, ly: 0.98 }, xclose: { vis: 2.15, ly: 1.12 } };

function world(name, seed) {
  const k = name + ':' + seed;
  if (!worlds.has(k)) worlds.set(k, construire(name, seed));
  return worlds.get(k);
}

export function draw(st) {
  const Wd = world(st.decor, st.seed);
  const scene = Wd.scene;
  // personnages
  for (const r of rigs.values()) if (r.root.parent) r.root.parent.remove(r.root);
  st.actors.forEach((a, i) => {
    const key = a.who + '#' + i;
    if (!rigs.has(key)) rigs.set(key, creer(a.who));
    const rig = rigs.get(key);
    scene.add(rig.root);
    const X = (a.x - 640) / 160;
    rig.root.position.set(X, Wd.hf ? Math.max(0, Wd.hf(X, 0)) : 0, 0);
    animer(rig, a, st.t, i);
  });
  Wd.upd.forEach((f) => f(st.t));
  // caméra
  const c = st.cam, fr = FR[c.kind] || FR.wide, vis = fr.vis / (c.zoom || 1);
  const tx = (c.x - 640) / 160 + (c.dx || 0);
  const d = vis / (2 * Math.tan((camera.fov * Math.PI / 180) / 2));
  const yaw = c.yaw || 0, pitch = (c.kind === 'xclose' || c.kind === 'close') ? 0.04 : 0.1;
  camera.position.set(tx + Math.sin(yaw) * d, fr.ly + Math.sin(pitch) * d * 0.6, Math.cos(yaw) * d);
  camera.lookAt(tx, fr.ly, 0);
  // la lune éclaire de face-gauche, l'ombre tombe derrière
  Wd.key.position.set(tx - 4.5, 8, 5.5); Wd.key.target.position.set(tx, 0, 0); Wd.key.target.updateMatrixWorld();
  renderer.render(scene, camera);
  return renderer.domElement.toDataURL('image/jpeg', 0.94);
}
window.sm = { init, draw };
window.ready = true;
