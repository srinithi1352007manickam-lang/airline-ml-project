/**
 * Srinithi - 3D Portfolio Scene Engine
 * Three.js WebGL Interactive Scene with Smooth Fallback Canvas 3D Engine
 */

(function () {
  'use strict';

  const container = document.getElementById('bg-canvas-container');
  if (!container) return;

  let mouseX = 0;
  let mouseY = 0;
  let targetX = 0;
  let targetY = 0;

  const windowHalfX = window.innerWidth / 2;
  const windowHalfY = window.innerHeight / 2;

  // Listen to mouse movement for 3D parallax
  document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX - windowHalfX) * 0.001;
    mouseY = (e.clientY - windowHalfY) * 0.001;
  });

  // Device orientation support for mobile
  if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', (e) => {
      if (e.gamma && e.beta) {
        mouseX = (e.gamma / 45) * 0.5;
        mouseY = (e.beta / 45) * 0.5;
      }
    });
  }

  // Check for Three.js availability
  if (typeof THREE !== 'undefined') {
    initThreeScene();
  } else {
    // Dynamic wait or fallback
    let tries = 0;
    const checkInterval = setInterval(() => {
      tries++;
      if (typeof THREE !== 'undefined') {
        clearInterval(checkInterval);
        initThreeScene();
      } else if (tries > 10) {
        clearInterval(checkInterval);
        initFallback3DCanvas();
      }
    }, 150);
  }

  /* ------------------------------------------------------------------------
     THREE.JS WEBGL IMPLEMENTATION
     ------------------------------------------------------------------------ */
  function initThreeScene() {
    container.innerHTML = '';
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x060813, 0.0012);

    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 2000);
    camera.position.z = 450;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 1. Particle Nebula Galaxy
    const particleCount = 1800;
    const particleGeometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const color1 = new THREE.Color(0x00f0ff); // Cyan
    const color2 = new THREE.Color(0x9d4edd); // Purple
    const color3 = new THREE.Color(0x10b981); // Emerald

    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      // Cylindrical / spherical spread
      const radius = 150 + Math.random() * 700;
      const theta = Math.random() * Math.PI * 2;
      const phi = (Math.random() - 0.5) * Math.PI;

      positions[i3] = radius * Math.cos(phi) * Math.sin(theta);
      positions[i3 + 1] = radius * Math.sin(phi) + (Math.random() - 0.5) * 200;
      positions[i3 + 2] = radius * Math.cos(phi) * Math.cos(theta) - 100;

      // Mix colors
      const mixedColor = color1.clone();
      const rand = Math.random();
      if (rand > 0.6) {
        mixedColor.lerp(color2, Math.random());
      } else if (rand > 0.3) {
        mixedColor.lerp(color3, Math.random());
      }

      colors[i3] = mixedColor.r;
      colors[i3 + 1] = mixedColor.g;
      colors[i3 + 2] = mixedColor.b;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Particle Material
    const particleMaterial = new THREE.PointsMaterial({
      size: 2.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    // 2. Central 3D Futuristic Wireframe Crystal Geometry
    const crystalGroup = new THREE.Group();
    crystalGroup.position.set(220, 20, 0); // Offset to sit beside hero text on desktop

    // Dual layer: solid glass core + wireframe shell
    const icoGeometry = new THREE.IcosahedronGeometry(75, 1);
    const wireMaterial = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.4
    });
    const wireMesh = new THREE.Mesh(icoGeometry, wireMaterial);
    crystalGroup.add(wireMesh);

    const innerGeometry = new THREE.IcosahedronGeometry(58, 0);
    const innerMaterial = new THREE.MeshPhongMaterial({
      color: 0x0a1030,
      emissive: 0x140f35,
      specular: 0x00f0ff,
      shininess: 90,
      transparent: true,
      opacity: 0.85
    });
    const innerMesh = new THREE.Mesh(innerGeometry, innerMaterial);
    crystalGroup.add(innerMesh);

    // 3. Orbital Concentric Rings
    const ringGeo1 = new THREE.TorusGeometry(110, 0.8, 16, 100);
    const ringMat1 = new THREE.MeshBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.35 });
    const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
    ring1.rotation.x = Math.PI / 3;
    crystalGroup.add(ring1);

    const ringGeo2 = new THREE.TorusGeometry(125, 0.6, 16, 100);
    const ringMat2 = new THREE.MeshBasicMaterial({ color: 0x9d4edd, transparent: true, opacity: 0.3 });
    const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
    ring2.rotation.y = Math.PI / 4;
    crystalGroup.add(ring2);

    scene.add(crystalGroup);

    // 4. Subtle Floating Nodes
    const nodeCount = 12;
    const nodes = [];
    const nodeGeo = new THREE.OctahedronGeometry(4, 0);
    const nodeMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff });

    for (let i = 0; i < nodeCount; i++) {
      const node = new THREE.Mesh(nodeGeo, nodeMat);
      const angle = (i / nodeCount) * Math.PI * 2;
      const dist = 140 + Math.random() * 20;
      node.position.set(Math.cos(angle) * dist, (Math.random() - 0.5) * 50, Math.sin(angle) * dist);
      crystalGroup.add(node);
      nodes.push({ mesh: node, speed: 0.005 + Math.random() * 0.01, angle });
    }

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f0ff, 2.5, 600);
    pointLight.position.set(200, 100, 200);
    scene.add(pointLight);

    const purpleLight = new THREE.PointLight(0x9d4edd, 2, 500);
    purpleLight.position.set(-200, -100, 100);
    scene.add(purpleLight);

    // Responsive position adaptation
    function adaptPosition() {
      if (window.innerWidth < 992) {
        crystalGroup.position.set(0, 160, -80);
        crystalGroup.scale.set(0.75, 0.75, 0.75);
      } else {
        crystalGroup.position.set(240, 20, 0);
        crystalGroup.scale.set(1, 1, 1);
      }
    }
    adaptPosition();

    // Animation Loop
    let clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Smooth camera parallax
      targetX += (mouseX * 80 - targetX) * 0.05;
      targetY += (-mouseY * 80 - targetY) * 0.05;
      camera.position.x = targetX;
      camera.position.y = targetY;
      camera.lookAt(scene.position);

      // Rotate particles slowly
      particles.rotation.y = elapsedTime * 0.02;
      particles.rotation.x = Math.sin(elapsedTime * 0.01) * 0.05;

      // Crystal animations
      wireMesh.rotation.x = elapsedTime * 0.15;
      wireMesh.rotation.y = elapsedTime * 0.2;
      innerMesh.rotation.x = -elapsedTime * 0.12;
      innerMesh.rotation.y = -elapsedTime * 0.18;

      ring1.rotation.z = elapsedTime * 0.1;
      ring2.rotation.x = elapsedTime * 0.08;

      // Node movements
      nodes.forEach((n) => {
        n.angle += n.speed;
        n.mesh.position.x = Math.cos(n.angle) * 140;
        n.mesh.position.z = Math.sin(n.angle) * 140;
        n.mesh.rotation.y += 0.02;
      });

      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      adaptPosition();
    });
  }

  /* ------------------------------------------------------------------------
     FALLBACK 3D CANVAS PARTICLES & GEOMETRY (Zero Dependency / Offline)
     ------------------------------------------------------------------------ */
  function initFallback3DCanvas() {
    container.innerHTML = '';
    const canvas = document.createElement('canvas');
    canvas.id = 'three-canvas';
    container.appendChild(canvas);
    const ctx = canvas.getContext('2d');

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const count = Math.min(100, Math.floor(width / 12));

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        z: Math.random() * 400 + 100,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        size: Math.random() * 2 + 1,
        color: Math.random() > 0.4 ? 'rgba(0, 240, 255,' : 'rgba(157, 78, 221,'
      });
    }

    let angle = 0;

    function render() {
      ctx.clearRect(0, 0, width, height);
      angle += 0.003;

      // Draw interactive connections
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx + mouseX * 2;
        p.y += p.vy - mouseY * 2;

        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        const alpha = 0.5 + Math.sin(angle + i) * 0.3;
        ctx.fillStyle = p.color + alpha + ')';
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
          if (dist < 110) {
            ctx.strokeStyle = `rgba(0, 240, 255, ${0.15 * (1 - dist / 110)})`;
            ctx.lineWidth = 0.6;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(render);
    }
    render();
  }
})();
