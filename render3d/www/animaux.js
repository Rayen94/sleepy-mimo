// Personnages 3D « jouets » : renard, chouette, hérisson, lapin, loutre, faon, castor, tortue.
// Tout est fabriqué avec des formes simples (sphères, cônes) et animé par une fonction pure du temps.
import * as THREE from 'three';

const SPH = new THREE.SphereGeometry(1, 44, 30);
const CONE = new THREE.ConeGeometry(1, 1, 28, 1);
const CYL = new THREE.CylinderGeometry(1, 1, 1, 24);
const BOX = new THREE.BoxGeometry(1, 1, 1);

const col = (c) => new THREE.Color(c);
function fur(c, o = {}) {
  return new THREE.MeshPhysicalMaterial({
    color: col(c), roughness: 0.8, metalness: 0,
    sheen: 1, sheenRoughness: 0.55, sheenColor: col(c).lerp(col(0xffffff), 0.55), ...o,
  });
}
const glossy = (c, r = 0.18) => new THREE.MeshPhysicalMaterial({ color: col(c), roughness: r, metalness: 0, clearcoat: 0.8, clearcoatRoughness: 0.15 });
const flat = (c) => new THREE.MeshBasicMaterial({ color: col(c) });

function mesh(parent, geo, mat, p = [0, 0, 0], s = [1, 1, 1], r = [0, 0, 0], cast = true) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(...p); m.scale.set(...s); m.rotation.set(...r);
  m.castShadow = cast; m.receiveShadow = false;
  parent.add(m);
  return m;
}
const sph = (parent, mat, p, s, r, cast) => mesh(parent, SPH, mat, p, s, r, cast);
const cone = (parent, mat, p, s, r) => mesh(parent, CONE, mat, p, s, r);

// ---------------------------------------------------------------- fiches des espèces
// body : [rx, ry, rz], head : rayon, legs : longueur des pattes
const SPEC = {
  fox:      { body: 0xe8782e, belly: 0xfff0dc, dark: 0x3a2418, head: 0.50, bodyH: 0.62, legs: 0.30, h: 1.0 },
  owl:      { body: 0x9a7552, belly: 0xe9d3ac, dark: 0x4a3322, head: 0.50, bodyH: 0.60, legs: 0.18, h: 1.0 },
  hedgehog: { body: 0x7b5a45, belly: 0xf1d9b5, dark: 0x3b2a22, head: 0.42, bodyH: 0.52, legs: 0.20, h: 0.9 },
  bunny:    { body: 0xf0ebe3, belly: 0xffffff, dark: 0x8a7f78, head: 0.47, bodyH: 0.60, legs: 0.28, h: 1.0 },
  otter:    { body: 0x8c5e3c, belly: 0xe8cfa6, dark: 0x3b2417, head: 0.46, bodyH: 0.60, legs: 0.28, h: 1.0 },
  fawn:     { body: 0xd09a63, belly: 0xfff2dc, dark: 0x4a3322, head: 0.42, bodyH: 0.8, legs: 0.42, h: 1.0 },
  beaver:   { body: 0x8e5c34, belly: 0xdcb98a, dark: 0x3d2515, head: 0.47, bodyH: 0.60, legs: 0.26, h: 1.0 },
  turtle:   { body: 0x7fb26a, belly: 0xf2e3b0, dark: 0x3f6b3a, head: 0.33, bodyH: 0.46, legs: 0.14, h: 0.78 },
};

export const ESPECES = Object.keys(SPEC);

function eyes(head, o) {
  const L = {}, R = {};
  const ex = o.ex ?? 0.2, ey = o.ey ?? 0.06, ez = o.ez ?? 0.4, er = o.er ?? 0.125;
  const sclera = glossy(0xffffff, 0.12), iris = glossy(o.iris ?? 0x2a1a12, 0.1), pupil = flat(0x050505);
  const out = [];
  for (const sd of [-1, 1]) {
    const g = new THREE.Group(); g.position.set(sd * ex, ey, ez); g.rotation.y = sd * 0.35;
    const lid = new THREE.Group(); g.add(lid);
    sph(lid, sclera, [0, 0, 0], [er, er * 1.12, er * 0.7], [0, 0, 0], false);
    const ir = sph(lid, iris, [0, 0, er * 0.38], [er * 0.72, er * 0.8, er * 0.45], [0, 0, 0], false);
    sph(lid, pupil, [0, 0, er * 0.62], [er * 0.4, er * 0.46, er * 0.2], [0, 0, 0], false);
    sph(lid, flat(0xffffff), [er * 0.28, er * 0.34, er * 0.9], [er * 0.2, er * 0.2, er * 0.12], [0, 0, 0], false);
    sph(lid, flat(0xffffff), [-er * 0.25, -er * 0.3, er * 0.86], [er * 0.1, er * 0.1, er * 0.08], [0, 0, 0], false);
    head.add(g);
    out.push({ g, lid, ir, sd });
  }
  return out;
}

function mouth(head, y, z, w = 0.1) {
  const g = new THREE.Group(); g.position.set(0, y, z); head.add(g);
  const cav = sph(g, flat(0x2a0a0e), [0, 0, 0], [w, 0.02, 0.03], [0, 0, 0], false);
  const tongue = sph(g, flat(0xe56a7c), [0, -0.012, 0.012], [w * 0.55, 0.01, 0.02], [0, 0, 0], false);
  const smileL = sph(g, flat(0x2a0a0e), [-w * 0.95, 0.012, 0], [0.012, 0.012, 0.012], [0, 0, 0], false);
  const smileR = sph(g, flat(0x2a0a0e), [w * 0.95, 0.012, 0], [0.012, 0.012, 0.012], [0, 0, 0], false);
  return { g, cav, tongue, w, smileL, smileR };
}

function limb(parent, mat, p, len, rad, tipMat, tipScale = 1.25) {
  const g = new THREE.Group(); g.position.set(...p); parent.add(g);
  const seg = sph(g, mat, [0, -len / 2, 0], [rad, len / 2 + rad * 0.5, rad], [0, 0, 0]);
  if (tipMat) sph(g, tipMat, [0, -len, rad * 0.25], [rad * tipScale, rad * 0.9, rad * tipScale * 1.15]);
  return g;
}

function blush(head, x, y, z) {
  const m = new THREE.MeshBasicMaterial({ color: 0xff7f8a, transparent: true, opacity: 0.38, depthWrite: false });
  for (const sd of [-1, 1]) { const b = sph(head, m, [sd * x, y, z], [0.07, 0.045, 0.02], [0, sd * 0.5, 0], false); }
}

// ---------------------------------------------------------------- fabrication
export function creer(espece) {
  const S = SPEC[espece];
  const root = new THREE.Group();
  const pivot = new THREE.Group(); root.add(pivot);
  const body = new THREE.Group(); pivot.add(body);
  const matB = fur(S.body), matBelly = fur(S.belly), matD = fur(S.dark);
  const rig = { root, pivot, body, S, espece, parts: {} };

  const legsH = S.legs;
  const by = legsH + S.bodyH * 0.55;                      // centre du corps
  const bodyR = espece === 'fawn' ? [0.38, 0.40, 0.55] : espece === 'turtle' ? [0.46, 0.34, 0.46] : espece === 'otter' ? [0.38, 0.46, 0.36] : [0.43, S.bodyH * 0.58, 0.38];
  const torso = sph(body, matB, [0, by, 0], bodyR);
  rig.parts.torso = torso;
  if (espece !== 'hedgehog' || true) sph(body, matBelly, [0, by - 0.04, bodyR[2] * 0.4], [bodyR[0] * 0.78, bodyR[1] * 0.82, bodyR[2] * 0.75], [0, 0, 0], false);

  // ---- tête
  const head = new THREE.Group();
  if (espece === 'fawn') sph(pivot, matB, [0, by + bodyR[1] * 0.75 + 0.1, 0.3], [0.2, 0.34, 0.22], [0.55, 0, 0]);
  if (espece === 'turtle') sph(pivot, matB, [0, by + 0.02, 0.42], [0.2, 0.2, 0.3], [0.4, 0, 0]);
  const headY = espece === 'fawn' ? by + bodyR[1] * 0.9 + 0.22 : espece === 'turtle' ? by + 0.12 : by + bodyR[1] * 0.75 + S.head * 0.62;
  const headZ = espece === 'fawn' ? 0.42 : espece === 'turtle' ? 0.62 : 0.05;
  head.position.set(0, headY, headZ); pivot.add(head);
  rig.head = head;
  const skull = sph(head, matB, [0, 0, 0], [S.head * 1.1, S.head * 0.96, S.head * 1.0]);
  const hr = S.head;
  let eyeOpt = { ex: hr * 0.4, ey: hr * 0.1, ez: hr * 0.8, er: hr * 0.26 };
  let mouthY = -hr * 0.36, mouthZ = hr * 0.93, mouthW = hr * 0.2;

  const earMat = matB, inner = fur(0xf2a5ae, { sheen: 0.4 });
  if (espece === 'fox') {
    for (const sd of [-1, 1]) {
      const e = cone(head, matB, [sd * hr * 0.58, hr * 0.86, -hr * 0.1], [hr * 0.38, hr * 0.95, hr * 0.22], [0.1, 0, -sd * 0.28]);
      cone(head, matD, [sd * hr * 0.58, hr * 0.8, hr * -0.02], [hr * 0.24, hr * 0.62, hr * 0.12], [0.1, 0, -sd * 0.28]);
      sph(head, matBelly, [sd * hr * 0.66, -hr * 0.28, hr * 0.5], [hr * 0.34, hr * 0.26, hr * 0.28], [0, sd * 0.5, 0]);   // joues blanches
    }
    sph(head, matBelly, [0, -hr * 0.28, hr * 0.62], [hr * 0.5, hr * 0.34, hr * 0.42]);                                     // museau
    sph(head, flat(0x0a0a0a), [0, -hr * 0.12, hr * 1.02], [hr * 0.13, hr * 0.1, hr * 0.1], [0, 0, 0], false);            // nez
    mouthY = -hr * 0.45; mouthZ = hr * 0.98; mouthW = hr * 0.17;
    // queue en panache
    const tail = new THREE.Group(); tail.position.set(0, by - 0.12, -bodyR[2] * 0.8); body.add(tail); rig.parts.tail = tail;
    sph(tail, matB, [0, 0.18, -0.34], [0.22, 0.22, 0.56], [-0.7, 0, 0]);
    sph(tail, matBelly, [0, 0.46, -0.72], [0.2, 0.2, 0.26], [-0.7, 0, 0]);
  }
  if (espece === 'owl') {
    for (const sd of [-1, 1]) {
      sph(head, fur(0xf3e2bf), [sd * hr * 0.42, hr * 0.06, hr * 0.78], [hr * 0.5, hr * 0.52, hr * 0.2], [0, sd * 0.3, 0], false);     // disque facial
      cone(head, matD, [sd * hr * 0.62, hr * 0.9, 0], [hr * 0.2, hr * 0.5, hr * 0.15], [0, 0, -sd * 0.45]);                           // aigrettes
    }
    eyeOpt = { ex: hr * 0.43, ey: hr * 0.08, ez: hr * 0.86, er: hr * 0.34, iris: 0xf3b82e };
    cone(head, glossy(0xf08a24, 0.4), [0, -hr * 0.2, hr * 1.04], [hr * 0.15, hr * 0.28, hr * 0.15], [Math.PI * 0.62, 0, 0]);       // bec
    mouthY = -hr * 0.52; mouthZ = hr * 0.9; mouthW = hr * 0.14;
  }
  if (espece === 'hedgehog') {
    for (const sd of [-1, 1]) sph(head, matD, [sd * hr * 0.75, hr * 0.55, -hr * 0.05], [hr * 0.22, hr * 0.22, hr * 0.12]);
    sph(head, fur(S.belly), [0, -hr * 0.18, hr * 0.5], [hr * 0.72, hr * 0.62, hr * 0.6]);                                           // visage clair
    sph(head, flat(0x0a0a0a), [0, -hr * 0.18, hr * 1.12], [hr * 0.12, hr * 0.1, hr * 0.1], [0, 0, 0], false);
    eyeOpt = { ex: hr * 0.36, ey: hr * 0.12, ez: hr * 0.82, er: hr * 0.25 };
    mouthY = -hr * 0.52; mouthZ = hr * 0.95; mouthW = hr * 0.15;
    // piquants sur le dos
    const spineGeo = new THREE.ConeGeometry(0.05, 0.3, 8);
    const count = 260, inst = new THREE.InstancedMesh(spineGeo, fur(0x4a3426, { sheen: 0.2 }), count);
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), sc = new THREE.Vector3(1, 1, 1);
    let r = 12345; const rnd = () => (r = (r * 1664525 + 1013904223) % 4294967296) / 4294967296;
    for (let i = 0; i < count; i++) {
      const th = rnd() * Math.PI * 2, ph = Math.acos(1 - rnd() * 1.15);       // calotte arrière/haute
      const dir = new THREE.Vector3(Math.sin(ph) * Math.cos(th), Math.cos(ph), -Math.abs(Math.sin(ph) * Math.sin(th)) - 0.1).normalize();
      v.set(dir.x * bodyR[0] * 1.02, by + dir.y * bodyR[1] * 1.02, dir.z * bodyR[2] * 1.02 - 0.02);
      q.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
      sc.setScalar(0.8 + rnd() * 0.7);
      m4.compose(v, q, sc); inst.setMatrixAt(i, m4);
    }
    inst.castShadow = true; body.add(inst);
  }
  if (espece === 'bunny') {
    rig.parts.ears = [];
    for (const sd of [-1, 1]) {
      const g = new THREE.Group(); g.position.set(sd * hr * 0.42, hr * 0.78, -hr * 0.05); head.add(g);
      sph(g, matB, [0, hr * 0.78, 0], [hr * 0.24, hr * 0.98, hr * 0.13]);
      sph(g, inner, [0, hr * 0.78, hr * 0.07], [hr * 0.14, hr * 0.78, hr * 0.06], [0, 0, 0], false);
      g.rotation.z = -sd * 0.16; rig.parts.ears.push({ g, sd });
    }
    sph(head, flat(0xf08a9a), [0, -hr * 0.08, hr * 1.0], [hr * 0.1, hr * 0.075, hr * 0.07], [0, 0, 0], false);
    sph(head, fur(0xffffff), [0, -hr * 0.3, hr * 0.82], [hr * 0.36, hr * 0.28, hr * 0.28]);
    sph(body, fur(0xffffff), [0, by - 0.1, -bodyR[2] * 0.95], [0.19, 0.19, 0.19]);                                                  // queue pompon
    mouthY = -hr * 0.4; mouthZ = hr * 0.98; mouthW = hr * 0.13;
  }
  if (espece === 'otter') {
    for (const sd of [-1, 1]) sph(head, matB, [sd * hr * 0.7, hr * 0.62, -hr * 0.05], [hr * 0.18, hr * 0.18, hr * 0.12]);
    sph(head, matBelly, [0, -hr * 0.28, hr * 0.62], [hr * 0.58, hr * 0.4, hr * 0.42]);
    sph(head, flat(0x0a0a0a), [0, -hr * 0.1, hr * 1.0], [hr * 0.14, hr * 0.1, hr * 0.1], [0, 0, 0], false);
    for (const sd of [-1, 1]) for (const k of [-1, 0, 1]) mesh(head, CYL, flat(0xf5efe4), [sd * hr * 0.55, -hr * 0.3 + k * 0.02, hr * 0.95], [0.004, hr * 0.55, 0.004], [0, 0, Math.PI / 2 + k * 0.18 * sd], false);
    mouthY = -hr * 0.5; mouthZ = hr * 0.95; mouthW = hr * 0.16;
    const tail = new THREE.Group(); tail.position.set(0, by - 0.25, -bodyR[2] * 0.8); body.add(tail); rig.parts.tail = tail;
    sph(tail, matB, [0, -0.02, -0.4], [0.14, 0.12, 0.55], [0.25, 0, 0]);
  }
  if (espece === 'fawn') {
    for (const sd of [-1, 1]) {
      sph(head, matB, [sd * hr * 1.12, hr * 0.62, -hr * 0.1], [hr * 0.62, hr * 0.2, hr * 0.1], [0, sd * 0.25, sd * 0.32]);
      sph(head, inner, [sd * hr * 1.08, hr * 0.62, -hr * 0.03], [hr * 0.44, hr * 0.12, hr * 0.06], [0, sd * 0.25, sd * 0.32], false);
      sph(head, fur(0xfff6e6), [sd * hr * 0.3, hr * 0.62, hr * 0.78], [hr * 0.08, hr * 0.06, hr * 0.04], [0, 0, 0], false);
    }
    sph(head, matBelly, [0, -hr * 0.34, hr * 0.62], [hr * 0.46, hr * 0.38, hr * 0.42]);
    sph(head, flat(0x1a1010), [0, -hr * 0.16, hr * 1.0], [hr * 0.12, hr * 0.1, hr * 0.09], [0, 0, 0], false);
    eyeOpt = { ex: hr * 0.42, ey: hr * 0.14, ez: hr * 0.82, er: hr * 0.27 };
    mouthY = -hr * 0.52; mouthZ = hr * 0.93; mouthW = hr * 0.14;
    // taches blanches
    const dots = new THREE.MeshStandardMaterial({ color: 0xfff6e6, roughness: 0.8 });
    for (let i = 0; i < 9; i++) {
      const a = (i / 9) * Math.PI * 1.4 - 0.7, rr = 0.42;
      sph(body, dots, [Math.sin(a * 1.6) * 0.22, by + 0.3 + Math.cos(a) * 0.08, -0.05 - i * 0.04], [0.045, 0.02, 0.045], [0.3, 0, 0], false);
    }
    const tail = new THREE.Group(); tail.position.set(0, by + 0.1, -bodyR[2] * 0.95); body.add(tail); rig.parts.tail = tail;
    sph(tail, fur(0xfff6e6), [0, 0, -0.04], [0.1, 0.14, 0.1]);
  }
  if (espece === 'beaver') {
    for (const sd of [-1, 1]) sph(head, matB, [sd * hr * 0.72, hr * 0.62, -hr * 0.05], [hr * 0.2, hr * 0.2, hr * 0.12]);
    sph(head, matBelly, [0, -hr * 0.3, hr * 0.62], [hr * 0.5, hr * 0.36, hr * 0.4]);
    sph(head, flat(0x120a06), [0, -hr * 0.1, hr * 1.0], [hr * 0.15, hr * 0.1, hr * 0.1], [0, 0, 0], false);
    for (const sd of [-1, 1]) mesh(head, BOX, glossy(0xfffbe8, 0.3), [sd * hr * 0.075, -hr * 0.5, hr * 0.94], [hr * 0.12, hr * 0.2, hr * 0.05], [0, 0, 0], false);
    mouthY = -hr * 0.42; mouthZ = hr * 0.96; mouthW = hr * 0.17;
    const tail = new THREE.Group(); tail.position.set(0, by - 0.3, -bodyR[2] * 0.9); body.add(tail); rig.parts.tail = tail;
    sph(tail, fur(0x4d3020), [0, 0, -0.34], [0.26, 0.07, 0.42], [0.15, 0, 0]);
  }
  if (espece === 'turtle') {
    sph(head, matB, [0, -hr * 0.1, hr * 0.5], [hr * 0.8, hr * 0.7, hr * 0.7]);
    eyeOpt = { ex: hr * 0.4, ey: hr * 0.2, ez: hr * 0.82, er: hr * 0.25 };
    mouthY = -hr * 0.4; mouthZ = hr * 0.95; mouthW = hr * 0.14;
    // carapace
    const shellMat = fur(0x6b8a3c, { sheen: 0.3, roughness: 0.55 });
    const shell = sph(body, shellMat, [0, by + 0.14, -0.1], [0.74, 0.54, 0.74]);
    const plate = glossy(0x4d6a2c, 0.35);
    for (let i = 0; i < 7; i++) {
      const a = i === 0 ? 0 : (i - 1) / 6 * Math.PI * 2, rr = i === 0 ? 0 : 0.42;
      const x = Math.cos(a) * rr, z = Math.sin(a) * rr - 0.1, y = by + 0.14 + Math.sqrt(Math.max(0.01, 1 - (x / 0.74) ** 2 - ((z + 0.1) / 0.74) ** 2)) * 0.54;
      const pl = sph(body, plate, [x, y - 0.035, z], [0.2, 0.055, 0.2], [0, 0, 0], false);
      const nrm = new THREE.Vector3(x / 0.5476, (y - (by + 0.14)) / 0.2916, (z + 0.1) / 0.5476).normalize(); pl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), nrm);
    }
  }
  blush(head, hr * 0.58, -hr * 0.18, hr * 0.7);

  // ---- yeux et bouche
  rig.eyes = eyes(head, eyeOpt);
  rig.mouth = mouth(head, mouthY, mouthZ, mouthW);

  // ---- bras et pattes
  const sx = espece === 'turtle' ? 0.42 : espece === 'fawn' ? 0.28 : 0.4;
  const armY = by + bodyR[1] * 0.45;
  const footMat = espece === 'fox' || espece === 'fawn' ? matD : matB;
  if (espece === 'owl') {
    rig.arms = [-1, 1].map((sd) => {
      const g = new THREE.Group(); g.position.set(sd * 0.4, by + 0.18, 0.02); body.add(g);
      sph(g, fur(0x80603f), [sd * 0.06, -0.26, -0.02], [0.12, 0.34, 0.2], [0, 0, sd * 0.15]);
      return { g, sd };
    });
  } else if (espece === 'turtle') {
    rig.arms = [-1, 1].map((sd) => limb(body, matB, [sd * 0.42, by - 0.1, 0.2], 0.22, 0.11, matB, 1.2)).map((g, i) => ({ g, sd: i ? 1 : -1 }));
  } else {
    rig.arms = [-1, 1].map((sd) => ({ g: limb(body, matB, [sd * sx, armY, 0.06], 0.4, 0.1, footMat === matB ? matB : matD, 1.2), sd }));
  }
  const legX = espece === 'fawn' ? 0.2 : 0.22;
  rig.legs = [-1, 1].map((sd) => {
    const g = limb(body, espece === 'fox' ? matD : matB, [sd * legX, legsH + 0.06, espece === 'fawn' ? 0.3 : 0.04], legsH + 0.06, espece === 'fawn' ? 0.095 : 0.13, espece === 'owl' ? glossy(0xf08a24, 0.4) : espece === 'fawn' ? matD : (espece === 'fox' ? matD : matB), espece === 'fawn' ? 1.4 : 1.15);
    return { g, sd };
  });
  if (espece === 'fawn') {   // pattes arrière
    rig.legs2 = [-1, 1].map((sd) => ({ g: limb(body, matB, [sd * legX, legsH + 0.1, -0.38], legsH + 0.1, 0.105, matD, 1.3), sd }));
  }
  rig.by = by;
  rig.base = { head: head.position.clone() };
  rig.scaleH = S.h;
  return rig;
}

// ---------------------------------------------------------------- animation
// a : { f, jump, tilt, mouth, blink, walk, wave, look, moving, x }   t : temps (s)   cam : position caméra
export function animer(rig, a, t, idx = 0) {
  const { pivot, head, S } = rig;
  const f = a.f || 1, ph = idx * 1.37;
  const breathe = Math.sin(t * 2.4 + ph);
  const talk = a.mouth || 0;
  // corps : 3/4 face, tourné vers la direction regardée
  const yaw = f * (a.moving ? 1.05 : 0.5);
  pivot.rotation.set(0, yaw, -(a.tilt || 0) * f * 0.012);
  const bob = a.moving ? Math.abs(Math.sin(a.walk * Math.PI * 2 * 2)) * 0.07 : 0.012 * breathe;
  pivot.position.y = (a.jump || 0) / 160 + bob;
  rig.body.scale.set(1 + 0.012 * breathe, 1 + 0.02 * breathe, 1 + 0.012 * breathe);
  // tête : se tourne vers le spectateur, hoche en parlant
  const look = a.look || 0;
  head.rotation.set(0.05 + talk * 0.07 + 0.02 * Math.sin(t * 1.7 + ph), -f * 0.22 + look * 0.18 + 0.03 * Math.sin(t * 1.1 + ph), (a.tilt || 0) * f * 0.012 + 0.02 * Math.sin(t * 1.3 + ph));
  // yeux
  for (const e of rig.eyes) {
    const lidY = a.blink ? 0.08 : 1 + 0.04 * Math.sin(t * 0.9);
    e.lid.scale.set(1, lidY, 1);
    e.ir.position.x = (look * 0.02 + 0.006 * Math.sin(t * 0.7 + ph)) * (rig.S.head / 0.5);
  }
  // bouche
  const m = rig.mouth, open = Math.min(1, talk * 1.1);
  m.cav.scale.set(m.w * (0.75 + 0.35 * open), 0.014 + 0.085 * open, 0.03);
  m.cav.position.y = -0.012 * open;
  m.tongue.visible = open > 0.35; m.tongue.scale.set(m.w * 0.5, 0.012 + 0.03 * open, 0.02);
  m.smileL.visible = m.smileR.visible = open < 0.15;
  const sm = 0.012 + 0.006 * (1 - open);
  m.smileL.position.y = m.smileR.position.y = 0.012 + 0.006 * (1 - open);
  // bras, pattes
  const w = a.wave || 0, ws = a.moving ? Math.sin(a.walk * Math.PI * 4) : 0;
  rig.arms.forEach((ar, i) => {
    const sd = ar.sd;
    ar.g.rotation.z = sd * (0.1 + 0.05 * breathe) + (sd === (f > 0 ? 1 : -1) ? -sd * w * 1.2 : 0);
    ar.g.rotation.x = ws * 0.7 * (i ? -1 : 1) + (a.moving ? 0 : 0.03 * Math.sin(t * 2 + i));
  });
  rig.legs.forEach((lg, i) => { lg.g.rotation.x = ws * 0.7 * (i ? 1 : -1); });
  if (rig.legs2) rig.legs2.forEach((lg, i) => { lg.g.rotation.x = ws * 0.7 * (i ? -1 : 1); });
  // oreilles de lapin, queues
  if (rig.parts.ears) rig.parts.ears.forEach((e) => { e.g.rotation.z = -e.sd * (0.16 + 0.05 * Math.sin(t * 1.6 + e.sd)) - (a.jump ? e.sd * 0.15 : 0); e.g.rotation.x = -0.08 + 0.04 * Math.sin(t * 2.2 + e.sd) - (a.jump ? 0.2 : 0); });
  if (rig.parts.tail) rig.parts.tail.rotation.y = 0.25 * Math.sin(t * 3 + ph) * (rig.espece === 'fox' ? 1.2 : 0.7);
}
