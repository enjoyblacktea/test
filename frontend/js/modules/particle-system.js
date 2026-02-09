/**
 * Particle System for Zhuyin Practice App
 * Implements canvas-based particle effects with object pooling for performance
 * @module particle-system
 */

/**
 * Particle class representing a single particle
 */
class Particle {
    constructor() {
        this.reset();
    }

    /**
     * Reset particle to inactive state
     */
    reset() {
        this.active = false;
        this.x = 0;
        this.y = 0;
        this.vx = 0;
        this.vy = 0;
        this.color = '#000000';
        this.opacity = 1;
        this.lifetime = 1;
        this.age = 0;
        this.size = 3;
    }

    /**
     * Update particle physics and aging
     * @param {number} deltaTime - Time since last frame in seconds
     * @param {number} gravity - Gravity acceleration
     */
    update(deltaTime, gravity = 0.3) {
        if (!this.active) return;

        // Update position
        this.x += this.vx * deltaTime * 60;
        this.y += this.vy * deltaTime * 60;

        // Apply gravity
        this.vy += gravity * deltaTime * 60;

        // Age particle
        this.age += deltaTime;
        this.opacity = Math.max(0, 1 - (this.age / this.lifetime));

        // Deactivate if dead
        if (this.opacity <= 0) {
            this.active = false;
        }
    }

    /**
     * Render particle on canvas
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     */
    render(ctx) {
        if (!this.active) return;

        ctx.save();
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

/**
 * ParticleSystem class managing all particle effects
 */
export class ParticleSystem {
    /**
     * Create a particle system
     * @param {HTMLCanvasElement} canvas - Canvas element for rendering
     */
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.pool = [];
        this.maxParticles = 300;
        this.lastTime = performance.now();
        this.running = false;

        // Initialize canvas size
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());

        // Initialize object pool
        this.initializePool(100);

        // Start render loop
        this.start();
    }

    /**
     * Resize canvas to fill viewport
     */
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    /**
     * Initialize object pool with pre-allocated particles
     * @param {number} count - Number of particles to pre-allocate
     */
    initializePool(count) {
        for (let i = 0; i < count; i++) {
            this.pool.push(new Particle());
        }
    }

    /**
     * Borrow a particle from the pool
     * @returns {Particle} Particle object
     */
    borrowParticle() {
        // Try to find inactive particle in pool
        let particle = this.pool.find(p => !p.active);

        // If no inactive particle found, create new one (if under limit)
        if (!particle && this.particles.length < this.maxParticles) {
            particle = new Particle();
            this.pool.push(particle);
        }

        return particle;
    }

    /**
     * Return particle to pool (mark as inactive)
     * @param {Particle} particle - Particle to return
     */
    returnParticle(particle) {
        particle.reset();
    }

    /**
     * Emit fireworks particles (celebratory effect for word completion)
     * @param {number} x - X coordinate
     * @param {number} y - Y coordinate
     * @param {Object} options - Configuration options
     * @param {string} options.color - Base color
     * @param {number} options.count - Number of particles (20-40)
     * @param {number} options.velocity - Initial velocity multiplier
     */
    emitFireworks(x, y, options = {}) {
        const {
            color = null,
            count = 30,
            velocity = 1.5
        } = options;

        // Color palette for fireworks
        const colors = color ? [color] : ['#d97706', '#dc2626', '#059669', '#d97706'];

        for (let i = 0; i < count; i++) {
            const particle = this.borrowParticle();
            if (!particle) break;

            // Radial pattern
            const angle = (Math.PI * 2 * i) / count;
            const speed = (Math.random() * 3 + 2) * velocity;

            particle.active = true;
            particle.x = x;
            particle.y = y;
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed;
            particle.color = colors[Math.floor(Math.random() * colors.length)];
            particle.opacity = 1;
            particle.lifetime = Math.random() * 0.5 + 1.5; // 1.5-2 seconds
            particle.age = 0;
            particle.size = Math.random() * 3 + 2;

            this.particles.push(particle);
        }

        // Enforce max particle limit
        this.enforceParticleLimit();
    }

    /**
     * Emit ink drop particles (subtle effect for correct input)
     * @param {number} x - X coordinate
     * @param {number} y - Y coordinate
     * @param {Object} options - Configuration options
     * @param {number} options.count - Number of particles (5-10)
     * @param {number} options.velocity - Initial velocity multiplier
     */
    emitInkDrops(x, y, options = {}) {
        const {
            count = 8,
            velocity = 1.0
        } = options;

        // Ink colors (dark)
        const colors = ['#1a1a1a', '#059669', '#4a5568'];

        for (let i = 0; i < count; i++) {
            const particle = this.borrowParticle();
            if (!particle) break;

            // Splash pattern (outward then fall)
            const angle = Math.random() * Math.PI * 2;
            const speed = (Math.random() * 2 + 1) * velocity;

            particle.active = true;
            particle.x = x;
            particle.y = y;
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed - 2; // Initial upward velocity
            particle.color = colors[Math.floor(Math.random() * colors.length)];
            particle.opacity = Math.random() * 0.3 + 0.6; // 0.6-0.9
            particle.lifetime = Math.random() * 0.3 + 0.7; // 0.7-1.0 seconds
            particle.age = 0;
            particle.size = Math.random() * 2 + 1;

            this.particles.push(particle);
        }

        // Enforce max particle limit
        this.enforceParticleLimit();
    }

    /**
     * Enforce maximum particle limit by removing oldest particles
     */
    enforceParticleLimit() {
        while (this.particles.length > this.maxParticles) {
            const oldParticle = this.particles.shift();
            if (oldParticle) {
                this.returnParticle(oldParticle);
            }
        }
    }

    /**
     * Update all active particles
     * @param {number} deltaTime - Time since last frame in seconds
     */
    update(deltaTime) {
        // Update particles and remove dead ones
        this.particles = this.particles.filter(particle => {
            particle.update(deltaTime);
            if (!particle.active) {
                this.returnParticle(particle);
                return false;
            }
            return true;
        });
    }

    /**
     * Render all active particles
     */
    render() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Render all particles
        for (const particle of this.particles) {
            particle.render(this.ctx);
        }
    }

    /**
     * Main animation loop
     */
    loop() {
        if (!this.running) return;

        const currentTime = performance.now();
        const deltaTime = (currentTime - this.lastTime) / 1000;
        this.lastTime = currentTime;

        this.update(deltaTime);
        this.render();

        requestAnimationFrame(() => this.loop());
    }

    /**
     * Start the particle system
     */
    start() {
        if (this.running) return;
        this.running = true;
        this.lastTime = performance.now();
        this.loop();
    }

    /**
     * Stop the particle system
     */
    stop() {
        this.running = false;
    }

    /**
     * Get current active particle count
     * @returns {number} Number of active particles
     */
    getActiveCount() {
        return this.particles.length;
    }
}
