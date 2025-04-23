class Attractor {
  constructor(x, y, z, c) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.history = [];
    this.c = c;
  }

  update() {
    const dx = sigma * (this.y - this.x) * dt;
    const dy = (this.x * (rho - this.z) - this.y) * dt;
    const dz = (this.x * this.y - beta * this.z) * dt;

    this.x += dx;
    this.y += dy;
    this.z += dz;

    if (typeof createVector === 'function') {
      this.history.push(createVector(this.x, this.y, this.z));
    } else {
      this.history.push({ x: this.x, y: this.y, z: this.z });
    }
  }

  display() {
    if (typeof beginShape === 'function') {
      noFill();
      stroke(this.c);
      beginShape();
      for (let v of this.history) {
        vertex(v.x, v.y, v.z);
      }
      endShape();
    }
  }
}

// Глобальні змінні для тестів
if (typeof window !== 'undefined') {
  window.sigma = 10;
  window.rho = 28;
  window.beta = 8 / 3;
  window.dt = 0.01;
}

