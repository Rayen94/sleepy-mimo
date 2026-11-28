// Décors 3D : ciel, sol, arbres, lumière de lune, lucioles, pluie, neige... Tout est déterministe (même résultat pour un même temps).
import * as THREE from 'three';

export function prng(seed) { let s = (seed >>> 0) || 1; return () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296); }
const col = (c) => new THREE.Color(c);

function canvasTex(w, h, draw, rep) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep, rep); t.anisotropy = 4; }
  return t;
}
export function glowTex(color = '#ffffff') {
  return canvasTex(128, 128, (g, w, h) => {
    const r = g.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
    r.addColorStop(0, color); r.addColorStop(0.25, color.replace(')', ',0.55)').replace('rgb', 'rgba')); r.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = r; g.fillRect(0, 0, w, h);
  });
}
const GLOW = {};
function glow(hex) {
  if (!GLOW[hex]) {
    const c = col(hex); const s = `rgb(${Math.round(c.r * 255)},${Math.round(c.g * 255)},${Math.round(c.b * 255)})`;
    GLOW[hex] = glowTex(s);
  }
  return GLOW[hex];
}
function sprite(hex, size, pos, op = 1) {
  const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: glow(hex), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, opacity: op, fog: false }));
  m.scale.set(size, size, 1); m.position.set(...pos); return m;
}

// ------------------------------------------------------------------ configurations
export const CFG = {
  meadow_night: { sky: [0x040920, 0x15296a, 0x4a66b0], fog: 0x1b2d63, fogD: 0.030, ground: [0x2f7556, 0x21604a], moon: [-7, 11, -26, 0xfff1cf, 3.0], stars: 520, key: [0xb9ccff, 2.5], hemi: [0x7f98ea, 0x1f3160, 1.0], rim: [0x8aa8ff, 1.2],
    trees: { n: 16, kind: 'round', cols: [0x1e5a52, 0x25695a, 0x1c4f4a], from: 8, to: 26 }, flowers: 70, fireflies: 70, tufts: 1100 },
  forest_night: { sky: [0x030818, 0x10234a, 0x2a4676], fog: 0x0c1c40, fogD: 0.052, ground: [0x1e5240, 0x153e33], moon: [5, 10, -22, 0xe8f0ff, 2.2], stars: 300, key: [0xa9c0ff, 2.1], hemi: [0x6f88dd, 0x16264c, 0.85], rim: [0x7aa0ff, 1.1],
    trees: { n: 46, kind: 'pine', cols: [0x153f40, 0x1b5048, 0x123638], from: 3.2, to: 30 }, mushrooms: 14, fireflies: 90, tufts: 900, rays: 4 },
  river_night: { sky: [0x040a22, 0x142b66, 0x46639f], fog: 0x172c5e, fogD: 0.034, ground: [0x2d6b52, 0x225a46], moon: [6, 10, -26, 0xfff1cf, 2.8], stars: 460, key: [0xb4c8ff, 2.4], hemi: [0x7890e0, 0x1d305c, 0.95], rim: [0x8aa8ff, 1.2],
    trees: { n: 18, kind: 'round', cols: [0x1c5550, 0x24665a], from: 9, to: 26 }, water: { z0: -11, z1: -3.2, c: 0x1d4c93 }, reeds: 36, fireflies: 60, tufts: 800 },
  pond_night: { sky: [0x040a22, 0x142b66, 0x46639f], fog: 0x172c5e, fogD: 0.034, ground: [0x2d6b52, 0x225a46], moon: [-5, 10, -26, 0xfff1cf, 2.8], stars: 460, key: [0xb4c8ff, 2.4], hemi: [0x7890e0, 0x1d305c, 0.95], rim: [0x8aa8ff, 1.2],
    trees: { n: 18, kind: 'round', cols: [0x1c5550, 0x24665a], from: 9, to: 26 }, pond: { x: 0, z: -7.5, r: 5.2, c: 0x1d4c93 }, reeds: 40, lilies: 9, fireflies: 70, tufts: 800 },
  rain_night: { sky: [0x0f1830, 0x2a3a5e, 0x5a6c94], fog: 0x2a3858, fogD: 0.045, ground: [0x2c5249, 0x203f3a], wet: true, moon: [0, 12, -30, 0x9db4e8, 1.6], stars: 0, key: [0x9db4e8, 2.1], hemi: [0x7488c8, 0x1c2644, 1.15], rim: [0x6f8fe0, 0.9],
    trees: { n: 34, kind: 'pine', cols: [0x14333a, 0x1a4045], from: 4, to: 28 }, rain: 520, tufts: 700 },
  snow_night: { sky: [0x050c26, 0x1c3a78, 0x6b8ccc], fog: 0x2a4380, fogD: 0.030, ground: [0xc8d6ee, 0xaebfe0], snow: 600, moon: [-6, 11, -24, 0xffffff, 3.0], stars: 520, key: [0xc8dcff, 2.5], hemi: [0x9ab4f0, 0x4a63a0, 1.15], rim: [0x9cc0ff, 1.3],
    trees: { n: 34, kind: 'snowpine', cols: [0x1a4a4a, 0x215a52], from: 3.5, to: 28 }, aurora: true, tufts: 0 },
  dawn_hills: { sky: [0x4a5fb0, 0xf2a0a8, 0xffd9a0], fog: 0xf0b9a2, fogD: 0.022, ground: [0x6fae5a, 0x4f9150], sun: [10, 5, -30, 0xffe2a0, 5.0], stars: 0, key: [0xffd9a8, 3.0], hemi: [0xffcfb8, 0x4a6a50, 1.1], rim: [0xffb88a, 1.4],
    trees: { n: 12, kind: 'round', cols: [0x4d9a56, 0x3f8a4f, 0x5aa65a], from: 8, to: 26 }, flowers: 90, tufts: 1200, fireflies: 0 },
  autumn_dusk: { sky: [0x2b2358, 0xd0635a, 0xffb36b], fog: 0xe08a66, fogD: 0.026, ground: [0x9a6a34, 0x7e5428], sun: [-9, 4, -30, 0xffc070, 4.5], stars: 0, key: [0xffc58a, 2.6], hemi: [0xffb08a, 0x4a3a50, 1.0], rim: [0xff9a5a, 1.3],
    trees: { n: 22, kind: 'round', cols: [0xd9702a, 0xe6902f, 0xb8452a, 0xf0b040], from: 5, to: 26 }, leaves: 140, tufts: 700 },
  den: { sky: [0x1a1020, 0x1a1020, 0x1a1020], fog: 0x1a1020, fogD: 0.0, ground: [0x4a3322, 0x3a2618], interior: 'den', key: [0xffd2a0, 0.8], hemi: [0xffcf9a, 0x3a2a20, 0.9], rim: [0xffb070, 0.9], lamp: 0xffb45a },
  cave: { sky: [0x0a0a18, 0x0a0a18, 0x0a0a18], fog: 0x120f28, fogD: 0.03, ground: [0x4a4660, 0x3a3650], interior: 'cave', key: [0xb8a8ff, 0.9], hemi: [0x8a7ad0, 0x221a3a, 0.9], rim: [0x7ad0ff, 1.0], lamp: 0xffa860 },
};

// ------------------------------------------------------------------ éléments
function skyDome(c) {
  const m = new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { a: { value: col(c.sky[0]) }, b: { value: col(c.sky[1]) }, c: { value: col(c.sky[2]) } },
    vertexShader: 'varying vec3 vp; void main(){ vp = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'varying vec3 vp; uniform vec3 a; uniform vec3 b; uniform vec3 c; void main(){ float h = clamp(vp.y,0.0,1.0); vec3 col = mix(c, b, smoothstep(0.0,0.35,h)); col = mix(col, a, smoothstep(0.25,0.95,h)); gl_FragColor = vec4(col,1.0); }',
  });
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(120, 32, 16), m); mesh.renderOrder = -10; return mesh;
}
function stars(n, rnd) {
  const pos = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const th = rnd() * Math.PI * 2, y = 0.12 + rnd() * 0.88, r = Math.sqrt(1 - y * y);
    pos.set([Math.cos(th) * r * 110, y * 110, -Math.abs(Math.sin(th)) * r * 110 - 6], i * 3);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  return new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0.85, fog: false, depthWrite: false }));
}

const heightAt = (c) => (x, z) => {
  let h = 0;
  if (c.interior) return 0;
  const back = Math.max(0, -z - 9), side = Math.max(0, Math.abs(x) - 11);
  h += back * 0.17 * (1 + 0.5 * Math.sin(x * 0.35) * Math.cos(z * 0.3));
  h += side * 0.09 * (1 + 0.4 * Math.sin(z * 0.4));
  if (c.water) { const d = (z - c.water.z0) / (c.water.z1 - c.water.z0); if (d > -0.12 && d < 1.12) h -= 0.55 * Math.sin(Math.PI * Math.min(1, Math.max(0, (d + 0.12) / 1.24))); }
  if (c.pond) { const d = Math.hypot((x - c.pond.x) / 1.35, z - c.pond.z) / c.pond.r; if (d < 1.2) h -= 0.6 * (1 - d / 1.2) ** 0.6; }
  h += 0.06 * Math.sin(x * 1.3) * Math.cos(z * 1.1);
  return h;
};

function ground(c, rnd) {
  const g = new THREE.PlaneGeometry(130, 130, 150, 150); g.rotateX(-Math.PI / 2);
  const p = g.attributes.position, hf = heightAt(c);
  for (let i = 0; i < p.count; i++) p.setY(i, hf(p.getX(i), p.getZ(i)));
  g.computeVertexNormals();
  const tex = canvasTex(512, 512, (x, w, h) => {
    x.fillStyle = '#' + col(c.ground[0]).getHexString(); x.fillRect(0, 0, w, h);
    for (let i = 0; i < 5200; i++) { x.fillStyle = (i % 2 ? '#' + col(c.ground[1]).getHexString() : '#' + col(c.ground[0]).clone().lerp(col(0xffffff), 0.12).getHexString()); x.globalAlpha = 0.35; x.fillRect(rnd() * w, rnd() * h, 2 + rnd() * 5, 2 + rnd() * 5); }
    x.globalAlpha = 1;
  }, 26);
  const m = new THREE.MeshStandardMaterial({ map: tex, roughness: c.wet ? 0.35 : 0.92, metalness: c.wet ? 0.25 : 0 });
  const mesh = new THREE.Mesh(g, m); mesh.receiveShadow = true; return mesh;
}

function tree(kind, cols, rnd, scale) {
  const g = new THREE.Group();
  const trunk = new THREE.MeshStandardMaterial({ color: kind.includes('snow') ? 0x4a3a30 : 0x3e2c26, roughness: 0.95 });
  const mat = () => new THREE.MeshStandardMaterial({ color: cols[Math.floor(rnd() * cols.length)], roughness: 0.9 });
  const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.16 * scale, 0.26 * scale, 2.2 * scale, 10), trunk); tr.position.y = 1.1 * scale; tr.castShadow = true; g.add(tr);
  if (kind === 'pine' || kind === 'snowpine') {
    const m1 = mat(), snow = new THREE.MeshStandardMaterial({ color: 0xf4f9ff, roughness: 0.8 });
    for (let i = 0; i < 4; i++) {
      const r = (1.5 - i * 0.28) * scale, h = (1.7 - i * 0.12) * scale;
      const c = new THREE.Mesh(new THREE.ConeGeometry(r, h, 14), m1); c.position.y = (2.0 + i * 0.95) * scale; c.castShadow = true; g.add(c);
      if (kind === 'snowpine') { const s = new THREE.Mesh(new THREE.ConeGeometry(r * 0.78, h * 0.55, 14), snow); s.position.y = (2.0 + i * 0.95 + h * 0.28) * scale; g.add(s); }
    }
  } else {
    const m1 = mat();
    for (let i = 0; i < 4; i++) {
      const b = new THREE.Mesh(new THREE.IcosahedronGeometry((1.0 + rnd() * 0.5) * scale, 2), i ? mat() : m1);
      b.position.set((rnd() - 0.5) * 1.6 * scale, (3.0 + rnd() * 1.3) * scale, (rnd() - 0.5) * 1.4 * scale); b.scale.y = 0.85; b.castShadow = true; g.add(b);
    }
  }
  return g;
}

function addTrees(scene, c, rnd, hf) {
  const t = c.trees; if (!t) return;
  for (let i = 0; i < t.n * 2; i++) {
    const side = rnd() < 0.5 ? -1 : 1;
    const z = -(t.from + Math.pow(rnd(), 0.8) * (t.to - t.from));
    const spread = 1.3 + (-z - t.from) * 0.30 + rnd() * 2.2;          // plus on s'éloigne, plus le couloir s'élargit, mais les arbres restent dans le cadre
    let x = side * spread;
    if (Math.abs(z) < t.from + 5) x = side * (2.3 + rnd() * 2.4);
    if (c.water && z < c.water.z1 + 0.5 && z > c.water.z0 - 1) continue;
    if (c.pond && Math.hypot((x - c.pond.x) / 1.35, z - c.pond.z) < c.pond.r + 1.2) continue;
    const tr = tree(t.kind, t.cols, rnd, 0.8 + rnd() * 0.9);
    tr.position.set(x, hf(x, z), z); tr.rotation.y = rnd() * 6; scene.add(tr);
  }
}

function addTufts(scene, c, rnd, hf, n) {
  if (!n) return;
  const geo = new THREE.ConeGeometry(0.03, 0.15, 5); geo.translate(0, 0.075, 0);
  const gc = col(c.ground[1]).lerp(col(0x3a9a5a), 0.35);
  const inst = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ color: gc, emissive: gc, emissiveIntensity: 0.12, roughness: 0.9 }), Math.floor(n * 0.6));
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), s = new THREE.Vector3();
  for (let i = 0; i < Math.floor(n * 0.6); i++) {
    const x = (rnd() - 0.5) * 18, z = -14 + rnd() * 15;
    if (c.water && z < c.water.z1 + 0.3 && z > c.water.z0 - 0.5) { m4.makeScale(0, 0, 0); inst.setMatrixAt(i, m4); continue; }
    if (c.pond && Math.hypot((x - c.pond.x) / 1.35, z - c.pond.z) < c.pond.r + 0.2) { m4.makeScale(0, 0, 0); inst.setMatrixAt(i, m4); continue; }
    v.set(x, hf(x, z), z); e.set((rnd() - 0.5) * 0.4, rnd() * 6, (rnd() - 0.5) * 0.4); q.setFromEuler(e); s.setScalar(0.7 + rnd() * 1.1);
    m4.compose(v, q, s); inst.setMatrixAt(i, m4);
  }
  scene.add(inst);
}

function addFlowers(scene, c, rnd, hf, n) {
  if (!n) return;
  const cols = [0xff8fb8, 0xffe27a, 0xffffff, 0xb79bff];
  const stem = new THREE.CylinderGeometry(0.012, 0.012, 0.3, 5); stem.translate(0, 0.15, 0);
  const head = new THREE.SphereGeometry(0.06, 10, 8);
  const sm = new THREE.MeshStandardMaterial({ color: 0x2c7a4a }), hm = cols.map((k) => new THREE.MeshStandardMaterial({ color: k, emissive: col(k), emissiveIntensity: 0.35, roughness: 0.6 }));
  for (let i = 0; i < n; i++) {
    const x = (rnd() - 0.5) * 18, z = -10 + rnd() * 16;
    if (Math.abs(x) < 1.6 && z > -1.5 && z < 2) continue;
    const g = new THREE.Group(); g.position.set(x, hf(x, z), z);
    g.add(new THREE.Mesh(stem, sm)); const h = new THREE.Mesh(head, hm[i % hm.length]); h.position.y = 0.32; g.add(h); scene.add(g);
  }
}

function addMushrooms(scene, c, rnd, hf, n) {
  const stem = new THREE.MeshStandardMaterial({ color: 0xf3e9d8 }), caps = [0xe0503e, 0xf2a43a, 0xb78cf0].map((k) => new THREE.MeshStandardMaterial({ color: k, emissive: col(k), emissiveIntensity: 0.18 }));
  for (let i = 0; i < n; i++) {
    const x = (rnd() < 0.5 ? -1 : 1) * (1.6 + rnd() * 6), z = -4 + rnd() * 9, s = 0.5 + rnd() * 0.9;
    const g = new THREE.Group(); g.position.set(x, hf(x, z), z); g.scale.setScalar(s);
    const st = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.3, 10), stem); st.position.y = 0.15; st.castShadow = true; g.add(st);
    const cp = new THREE.Mesh(new THREE.SphereGeometry(0.2, 18, 10, 0, Math.PI * 2, 0, Math.PI / 2), caps[i % 3]); cp.position.y = 0.3; cp.scale.y = 0.75; cp.castShadow = true; g.add(cp);
    scene.add(g);
  }
}

function addReeds(scene, c, rnd, hf, n) {
  if (!n) return;
  const m = new THREE.MeshStandardMaterial({ color: 0x4f8a4a, roughness: 0.8 }), br = new THREE.MeshStandardMaterial({ color: 0x6b4a30 });
  for (let i = 0; i < n; i++) {
    let x, z;
    if (c.water) { x = (rnd() - 0.5) * 22; z = c.water.z1 + 0.2 + rnd() * 0.5; } else { const a = rnd() * Math.PI * 2; x = c.pond.x + Math.cos(a) * (c.pond.r * 1.35 + rnd() * 0.4); z = c.pond.z + Math.sin(a) * (c.pond.r + rnd() * 0.4); if (z > -1.5) continue; }
    const h = 0.9 + rnd() * 0.9, g = new THREE.Group(); g.position.set(x, hf(x, z), z); g.rotation.set((rnd() - 0.5) * 0.25, 0, (rnd() - 0.5) * 0.25);
    const s = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.02, h, 5), m); s.position.y = h / 2; g.add(s);
    if (rnd() < 0.55) { const t = new THREE.Mesh(new THREE.CapsuleGeometry(0.04, 0.2, 4, 8), br); t.position.y = h; t.castShadow = true; g.add(t); }
    scene.add(g);
  }
}

function addWater(scene, c, rnd, upd) {
  let mesh;
  const mat = new THREE.MeshPhysicalMaterial({ color: (c.water || c.pond).c, roughness: 0.12, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.08, emissive: col((c.water || c.pond).c), emissiveIntensity: 0.22 });
  if (c.water) {
    const w = c.water, g = new THREE.PlaneGeometry(60, w.z1 - w.z0 + 1.2, 60, 14); g.rotateX(-Math.PI / 2); mesh = new THREE.Mesh(g, mat); mesh.position.set(0, -0.14, (w.z0 + w.z1) / 2);
  } else {
    const p = c.pond, g = new THREE.CircleGeometry(p.r, 64, 0, Math.PI * 2); g.rotateX(-Math.PI / 2); g.scale(1.35, 1, 1); mesh = new THREE.Mesh(g, mat); mesh.position.set(p.x, -0.12, p.z);
  }
  mesh.receiveShadow = true; scene.add(mesh);
  return mesh;
}

function addLilies(scene, c, rnd, n) {
  const m = new THREE.MeshStandardMaterial({ color: 0x3f9a58, roughness: 0.7 }), f = new THREE.MeshStandardMaterial({ color: 0xff9ec4, emissive: col(0xff9ec4), emissiveIntensity: 0.3 });
  for (let i = 0; i < n; i++) {
    const a = rnd() * Math.PI * 2, rr = Math.sqrt(rnd()) * c.pond.r * 0.85;
    const x = c.pond.x + Math.cos(a) * rr * 1.3, z = c.pond.z + Math.sin(a) * rr;
    const pad = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.02, 20), m); pad.position.set(x, -0.1, z); scene.add(pad);
    if (i % 3 === 0) { const fl = new THREE.Mesh(new THREE.SphereGeometry(0.11, 12, 8), f); fl.position.set(x, -0.04, z); scene.add(fl); }
  }
}

// particules animées
function particles(scene, n, color, size, area, rnd, kind) {
  const pos = new Float32Array(n * 3), base = [];
  for (let i = 0; i < n; i++) {
    const b = { x: (rnd() - 0.5) * area[0], y: area[3] + rnd() * area[1], z: area[4] + rnd() * area[2], ph: rnd() * 6.28, sp: 0.4 + rnd() * 0.9, am: 0.3 + rnd() * 0.6 };
    base.push(b); pos.set([b.x, b.y, b.z], i * 3);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const m = new THREE.PointsMaterial({ color, size, map: glow(color), transparent: true, blending: kind === 'snow' ? THREE.NormalBlending : THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true });
  const pts = new THREE.Points(g, m); pts.frustumCulled = false; scene.add(pts);
  return { pts, base, kind, area };
}
function stepParticles(P, t) {
  const p = P.pts.geometry.attributes.position, A = P.area;
  P.base.forEach((b, i) => {
    let x = b.x, y = b.y, z = b.z;
    if (P.kind === 'fly') { x += Math.sin(t * b.sp + b.ph) * b.am; y += Math.sin(t * b.sp * 1.3 + b.ph * 2) * b.am * 0.5; z += Math.cos(t * b.sp * 0.8 + b.ph) * b.am; }
    else { const fall = ((b.y - t * b.sp * (P.kind === 'leaf' ? 0.55 : 0.5) + 1000 * A[1]) % A[1] + A[1]) % A[1]; y = A[3] + fall; x += Math.sin(t * b.sp + b.ph) * (P.kind === 'leaf' ? 1.2 : 0.35); z += Math.cos(t * 0.7 + b.ph) * 0.3; }
    p.setXYZ(i, x, y, z);
  });
  p.needsUpdate = true;
}
function rainLines(scene, n, rnd) {
  const g = new THREE.BufferGeometry(), pos = new Float32Array(n * 6), base = [];
  for (let i = 0; i < n; i++) base.push({ x: (rnd() - 0.5) * 26, z: -12 + rnd() * 22, y: rnd() * 12, sp: 9 + rnd() * 4 });
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const l = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: 0xb4c8ff, transparent: true, opacity: 0.5 })); l.frustumCulled = false; scene.add(l);
  return { l, base };
}
function stepRain(R, t) {
  const p = R.l.geometry.attributes.position;
  R.base.forEach((b, i) => { const y = (((b.y - t * b.sp) % 12) + 12) % 12; p.setXYZ(i * 2, b.x, y, b.z); p.setXYZ(i * 2 + 1, b.x - 0.06, y + 0.55, b.z); });
  p.needsUpdate = true;
}

// ------------------------------------------------------------------ intérieurs : terrier et grotte
function interior(scene, c, rnd) {
  const out = { lights: [] };
  const wallMat = new THREE.MeshStandardMaterial({ color: c.interior === 'den' ? 0x6e4a30 : 0x5a5478, roughness: 1, side: THREE.BackSide });
  const wall = new THREE.Mesh(new THREE.SphereGeometry(11, 48, 32), wallMat); wall.scale.set(1.15, 0.52, 1); wall.position.set(0, 2.2, -2.5); wall.receiveShadow = true; scene.add(wall);
  const floor = new THREE.Mesh(new THREE.CircleGeometry(11, 48), new THREE.MeshStandardMaterial({ color: c.ground[0], roughness: 0.95 }));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  const rug = new THREE.Mesh(new THREE.CircleGeometry(2.2, 48), new THREE.MeshStandardMaterial({ color: c.interior === 'den' ? 0x7a3a34 : 0x38305a, roughness: 1 })); rug.rotation.x = -Math.PI / 2; rug.position.set(0, 0.012, 0.4); rug.receiveShadow = true; scene.add(rug);
  if (c.interior === 'den') {
    // racines, fenêtre ronde de lune, lanterne, étagère, lit de foin
    const rootM = new THREE.MeshStandardMaterial({ color: 0x4a2f1e, roughness: 1 });
    for (let i = 0; i < 12; i++) {
      const a = -1.2 + (i / 11) * 2.4 + (rnd() - 0.5) * 0.2, curve = new THREE.CatmullRomCurve3([new THREE.Vector3(Math.sin(a) * 9, 5.6, -Math.cos(a) * 9 - 2), new THREE.Vector3(Math.sin(a) * 8.4 + (rnd() - 0.5) * 0.8, 3.5, -Math.cos(a) * 8.4 - 2), new THREE.Vector3(Math.sin(a) * 9.4, 1.6 + rnd(), -Math.cos(a) * 9.4 - 2)]);
      const r = new THREE.Mesh(new THREE.TubeGeometry(curve, 12, 0.07 + rnd() * 0.08, 6), rootM); r.castShadow = true; scene.add(r);
    }
    const win = new THREE.Mesh(new THREE.CircleGeometry(1.1, 40), new THREE.MeshBasicMaterial({ color: 0x7f98d8 })); win.position.set(-3.2, 3.4, -8.3); scene.add(win);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(1.1, 0.1, 12, 40), rootM); ring.position.copy(win.position); scene.add(ring);
    scene.add(sprite(0x9fb8ff, 7, [-3.2, 3.4, -8.1], 0.55));
    const bed = new THREE.Mesh(new THREE.TorusGeometry(1.1, 0.35, 14, 30), new THREE.MeshStandardMaterial({ color: 0xe4c46a, roughness: 1 })); bed.rotation.x = -Math.PI / 2; bed.position.set(4.2, 0.3, -5); bed.scale.set(1, 1, 1); bed.castShadow = true; scene.add(bed);
    const shelf = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.14, 0.7), rootM); shelf.position.set(3.3, 3.0, -8.2); scene.add(shelf);
    for (let i = 0; i < 6; i++) { const j = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.4 + rnd() * 0.2, 14), new THREE.MeshPhysicalMaterial({ color: [0xff9a3c, 0x7ad06a, 0xd06ab0, 0xffe27a][i % 4], roughness: 0.2, emissive: col([0xff9a3c, 0x7ad06a, 0xd06ab0, 0xffe27a][i % 4]), emissiveIntensity: 0.3 })); j.position.set(1.9 + i * 0.55, 3.28, -8.1); scene.add(j); }
  } else {
    // stalactites, cristaux lumineux
    const rock = new THREE.MeshStandardMaterial({ color: 0x6a6488, roughness: 1 });
    for (let i = 0; i < 26; i++) { const s = 0.3 + rnd() * 0.5; const k = new THREE.Mesh(new THREE.ConeGeometry(s, 1.4 + rnd() * 2.2, 8), rock); k.rotation.x = Math.PI; k.position.set((rnd() - 0.5) * 20, 5 - rnd() * 0.5, -2 - rnd() * 7); k.castShadow = true; scene.add(k); }
    const cry = [0x6ad8ff, 0xff7ad8, 0x8aff9a];
    for (let i = 0; i < 18; i++) { const k = cry[i % 3], m = new THREE.Mesh(new THREE.ConeGeometry(0.16 + rnd() * 0.15, 0.8 + rnd() * 1.2, 6), new THREE.MeshPhysicalMaterial({ color: k, emissive: col(k), emissiveIntensity: 1.4, roughness: 0.15, transparent: true, opacity: 0.92 })); const x = (rnd() < 0.5 ? -1 : 1) * (2.4 + rnd() * 6), z = -2 - rnd() * 6; m.position.set(x, 0.5, z); m.rotation.z = (rnd() - 0.5) * 0.5; scene.add(m); if (i % 4 === 0) scene.add(sprite(k, 2.6, [x, 0.9, z], 0.8)); }
    for (let i = 0; i < 14; i++) { const s = 0.4 + rnd() * 0.7, b = new THREE.Mesh(new THREE.IcosahedronGeometry(s, 1), rock); b.position.set((rnd() < 0.5 ? -1 : 1) * (4 + rnd() * 5), s * 0.5, -3 - rnd() * 7); b.castShadow = true; scene.add(b); }
  }
  return out;
}

// ------------------------------------------------------------------ assemblage
export function construire(name, seed) {
  const c = CFG[name] || CFG.meadow_night, rnd = prng(seed * 7919 + name.length * 131);
  const scene = new THREE.Scene(), upd = [];
  scene.background = col(c.sky[0]);
  scene.fog = new THREE.FogExp2(c.fog, c.fogD);
  scene.add(skyDome(c));
  const hf = heightAt(c);
  if (c.stars) scene.add(stars(c.stars, rnd));
  if (c.moon) { const [x, y, z, k, s] = c.moon; scene.add(sprite(k, s * 4.2, [x, y, z], 0.55)); const d = new THREE.Mesh(new THREE.CircleGeometry(s * 0.62, 40), new THREE.MeshBasicMaterial({ color: k, fog: false })); d.position.set(x, y, z + 0.1); scene.add(d); }
  if (c.sun) { const [x, y, z, k, s] = c.sun; scene.add(sprite(k, s * 5, [x, y, z], 0.7)); const d = new THREE.Mesh(new THREE.CircleGeometry(s * 0.5, 40), new THREE.MeshBasicMaterial({ color: 0xfff4d0, fog: false })); d.position.set(x, y, z + 0.1); scene.add(d); }
  if (c.interior) { interior(scene, c, rnd); }
  else {
    scene.add(ground(c, rnd));
    addTrees(scene, c, rnd, hf);
    addTufts(scene, c, rnd, hf, c.tufts);
    addFlowers(scene, c, rnd, hf, c.flowers);
    addMushrooms(scene, c, rnd, hf, c.mushrooms || 0);
    if (c.water || c.pond) { const w = addWater(scene, c, rnd); upd.push((t) => { const p = w.geometry.attributes.position; if (c.water) for (let i = 0; i < p.count; i++) p.setY(i, 0.025 * Math.sin(p.getX(i) * 0.9 + t * 1.4) * Math.cos(p.getZ(i) * 1.1 + t)); p.needsUpdate = true; }); addReeds(scene, c, rnd, hf, c.reeds || 0); }
    if (c.pond) addLilies(scene, c, rnd, c.lilies || 0);
    if (c.moon && (c.water || c.pond)) { const m = c.moon; const zc = c.water ? (c.water.z0 + c.water.z1) / 2 : c.pond.z; scene.add(sprite(m[3], 5, [m[0] * 0.25, 0.1, zc], 0.45)); }
  }
  if (c.fireflies || c.interior) {
    const n = c.interior ? 26 : c.fireflies;
    const P = particles(scene, n, c.interior === 'cave' ? 0x7affd8 : 0xd8ff7a, c.interior ? 0.22 : 0.3, c.interior ? [14, 4, 8, 0.6, -6] : [22, 3.5, 16, 0.4, -10], rnd, 'fly'); upd.push((t) => stepParticles(P, t));
  }
  if (c.rain) { const R = rainLines(scene, c.rain, rnd); upd.push((t) => stepRain(R, t)); }
  if (c.snow) { const P = particles(scene, c.snow, 0xffffff, 0.16, [24, 12, 22, 0, -12], rnd, 'snow'); upd.push((t) => stepParticles(P, t)); }
  if (c.leaves) { const P = particles(scene, c.leaves, 0xff9a3a, 0.22, [24, 10, 20, 0, -10], rnd, 'leaf'); upd.push((t) => stepParticles(P, t)); }
  if (c.rays) for (let i = 0; i < c.rays; i++) { const ray = new THREE.Mesh(new THREE.ConeGeometry(1.6, 14, 20, 1, true), new THREE.MeshBasicMaterial({ color: 0xaac8ff, transparent: true, opacity: 0.045, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide })); ray.position.set(-8 + i * 5 + rnd() * 2, 7, -8 - rnd() * 8); ray.rotation.z = 0.25; scene.add(ray); }
  if (c.aurora) { for (let i = 0; i < 3; i++) { const a = new THREE.Mesh(new THREE.PlaneGeometry(60, 9), new THREE.MeshBasicMaterial({ color: [0x5affc0, 0x7a8aff, 0x9affd0][i], transparent: true, opacity: 0.10, blending: THREE.AdditiveBlending, depthWrite: false, fog: false })); a.position.set(-4 + i * 4, 14 + i * 2, -45 - i * 3); a.rotation.z = -0.1 + i * 0.07; scene.add(a); } }
  // lumières
  const key = new THREE.DirectionalLight(c.key[0], c.key[1]); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); const sc = key.shadow.camera; sc.left = -7; sc.right = 7; sc.top = 7; sc.bottom = -7; sc.near = 1; sc.far = 40; key.shadow.bias = -0.0004; key.shadow.normalBias = 0.03;
  scene.add(key, key.target);
  const hemi = new THREE.HemisphereLight(c.hemi[0], c.hemi[1], c.hemi[2]); scene.add(hemi);
  const rim = new THREE.DirectionalLight(c.rim[0], c.rim[1]); rim.position.set(-5, 4, -8); scene.add(rim);
  if (c.lamp) { const L = new THREE.PointLight(c.lamp, c.interior === 'cave' ? 10 : 8, 14, 1.7); L.position.set(0, 3.4, 1.2); scene.add(L); const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.22, 18, 14), new THREE.MeshBasicMaterial({ color: c.lamp })); bulb.position.copy(L.position); scene.add(bulb); scene.add(sprite(c.lamp, 3.4, [L.position.x, L.position.y, L.position.z], 0.7)); }
  else { const warm = new THREE.PointLight(0xffd9a0, 4, 9, 1.8); warm.position.set(1.4, 1.6, 3.2); scene.add(warm); }
  return { scene, key, upd, cfg: c, hf };
}
