// Ждем загрузки DOM
// ФОРМУЛА СЕРДЦА (параметрическая)
// x = 16 * sin³(t)
// y = 13 * cos(t) - 5 * cos(2t) - 2 * cos(3t) - cos(4t)

const heartVertices = [];
const targetVertices = [];
const numParticles = 3000; // Количество частиц

// Генерируем частицы по формуле сердца
for (let i = 0; i < numParticles; i += 0.1) {
    const t = (Math.PI * 2 * i) / numParticles;
    
    // Формула сердца
    const x = 16 * Math.pow(Math.sin(t), 3);
    const y = (13 * Math.cos(t) - 5 * Math.cos(2*t) - 2 * Math.cos(3*t) - Math.cos(4*t));
    
    // Масштабируем
    const scale = 12;
    const finalX = x * scale;
    const finalY = y * scale;
    
    // Добавляем случайность для объема (толщина сердца)
    const randomOffset = () => (Math.random() - 0.5) * 15;
    
    const vertex = new THREE.Vector3(
        finalX + randomOffset(),
        finalY + randomOffset(),
        randomOffset() * 2
    );
    
    heartVertices.push(vertex);
    
    // Целевая позиция (для анимации сборки)
    targetVertices.push(new THREE.Vector3(finalX, finalY, 0));
}

// Создаем сцену
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);

// Камера
const camera = new THREE.PerspectiveCamera(
    75, 
    window.innerWidth / window.innerHeight, 
    0.1, 
    2000
);
camera.position.z = 400;

// Рендерер
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// Создаем геометрию частиц
const particlesGeometry = new THREE.BufferGeometry();
const positionsArray = new Float32Array(heartVertices.length * 3);

heartVertices.forEach((vertex, i) => {
    positionsArray[i * 3] = vertex.x;
    positionsArray[i * 3 + 1] = vertex.y;
    positionsArray[i * 3 + 2] = vertex.z;
});

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positionsArray, 3));

// Материал частиц (розовый с свечением)
const particlesMaterial = new THREE.PointsMaterial({
    color: 0x14ffc4,
    size: 3,
    transparent: true,
    opacity: 0.9,
    blending: THREE.AdditiveBlending,
    depthWrite: false
});

// Создаем систему частиц
const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

// АНИМАЦИЯ БИЕНИЯ СЕРДЦА 💓
function heartbeat() {
    const tl = gsap.timeline({ repeat: -1 });
    
    // Сжатие
    tl.to(particlesMesh.scale, {
        x: 0.9,
        y: 0.9,
        z: 0.9,
        duration: 0.15,
        ease: "power2.in"
    })
    // Расширение (удар)
    .to(particlesMesh.scale, {
        x: 1.1,
        y: 1.1,
        z: 1.1,
        duration: 0.15,
        ease: "power2.out"
    })
    // Возврат
    .to(particlesMesh.scale, {
        x: 1,
        y: 1,
        z: 1,
        duration: 0.3,
        ease: "elastic.out(1, 0.5)"
    })
    // Пауза между ударами
    .to({}, { duration: 0.5 });
}

heartbeat();

// Медленное вращение
gsap.to(particlesMesh.rotation, {
    y: Math.PI * 2,
    duration: 30,
    repeat: -1,
    ease: "none"
});

// Анимация мерцания частиц
const positions = particlesGeometry.attributes.position.array;
for (let i = 0; i < heartVertices.length; i++) {
    gsap.to(particlesMaterial, {
        opacity: 0.6 + Math.random() * 0.4,
        duration: 1 + Math.random() * 2,
        repeat: -1,
        yoyo: true,
        delay: Math.random() * 2,
        ease: "sine.inOut"
    });
}

// Рендеринг
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

animate();

// Адаптация под размер окна
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});