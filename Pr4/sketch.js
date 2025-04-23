// this code should be runned in p5.js
let sigma = 10;
let rho = 28;
let beta = 8 / 3;
let dt = 0.01;
let maxPoints = 100;

let attractors = [];
let num = 20;

function setup() {
  createCanvas(600, 400, WEBGL);
  frameRate(60);

  for (let i = 0; i < num; i++) {
    let init = (i + 1) * 0.05;
    let c = color((i / num) * 255, 100, 255);
    attractors.push(new Attractor(init, init, init, c));
  }
}

function draw() {
  background(30);
  orbitControl();
  scale(5);

  for (let a of attractors) {
    a.update();
    a.display();
  }
}

class Attractor {
  constructor(x, y, z, c) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.history = [];
    this.c = c;
  }

  update() {
    let dx = sigma * (this.y - this.x) * dt;
    let dy = (this.x * (rho - this.z) - this.y) * dt;
    let dz = (this.x * this.y - beta * this.z) * dt;

    this.x += dx;
    this.y += dy;
    this.z += dz;

    this.history.push(createVector(this.x, this.y, this.z));
  }

  display() {
    noFill();
    stroke(this.c);
    beginShape();
    for (let v of this.history) {
      vertex(v.x, v.y, v.z);
    }
    endShape();
  }
}
