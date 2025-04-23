let config = {
  numPopulations: 3,
  populationSize: 10,
  geneLength: 10,
  generations: 20,
  mutationRate: 0.01
};

let populations = [];

function setup() {
  createCanvas(4000, 650);
  textFont("comfortaa");
  for (let i = 0; i < config.numPopulations; i++) {
    populations.push(new Population(i));
  }
  frameRate(1);
}

function draw() {
  background(50, 150, 50);
  for (let pop of populations) {
    pop.update();
    pop.display();
  }
}

function drawCow(x, y, size, fitness) {
  push();
  translate(x, y);
  scale(size / 100);

  fill(255);
  noStroke();
  ellipse(0, 0, 100, 100);

  fill(0);
  ellipse(-35, -10, 15, 20);
  ellipse(35, -10, 15, 20);

  fill(180);
  ellipse(-20, -35, 12, 12);
  ellipse(20, -35, 12, 12);

  fill(0);
  ellipse(-15, -10, 6, 6);
  ellipse(15, -10, 6, 6);

  fill(235, 160, 170);
  ellipse(0, 20, 45, 30);

  fill(0);
  ellipse(-8, 20, 4, 4);
  ellipse(8, 20, 4, 4);

  pop();
}

class Population {
  constructor(index) {
    this.index = index;
    this.generation = 0;
    this.individuals = generatePopulation(config.populationSize, config.geneLength);
    this.width = width / config.numPopulations;
    this.xOffset = this.index * this.width;
    this.fitnessHistory = [];
  }

  update() {
    if (this.generation >= config.generations) return;

    const oldIndividuals = [...this.individuals];
    const fitnessScores = this.individuals.map(ind => fitness(ind));
    const newGen = [];

    for (let i = 0; i < config.populationSize / 2; i++) {
      const p1 = selectParent(this.individuals, fitnessScores);
      const p2 = selectParent(this.individuals, fitnessScores);
      let [c1, c2] = crossover(p1, p2);
      c1 = mutate(c1, config.mutationRate);
      c2 = mutate(c2, config.mutationRate);
      newGen.push(c1, c2);
    }

    this.individuals = newGen;
    this.generation++;
    this.fitnessHistory.push(Math.max(...fitnessScores));
  }

  display() {
    const fitnessScores = this.individuals.map(ind => fitness(ind));
    const maxFit = Math.max(...fitnessScores);
    const avgFit = fitnessScores.reduce((a, b) => a + b, 0) / fitnessScores.length;

    for (let i = 0; i < this.individuals.length; i++) {
      const x = this.xOffset + (i % 5) * 130 + 60;
      const y = Math.floor(i / 5) * 100 + 60;
      const fit = fitnessScores[i];
      let size = map(fit, 0, maxFit, 30, 100);
      drawCow(x, y, size, fit);
    }

    fill(255);
    textSize(12);
    textAlign(LEFT, TOP);
    text(`🐄 Популяція ${this.index + 1}`, this.xOffset + 10, height - 120);
    text(`Покоління: ${this.generation}`, this.xOffset + 10, height - 100);
    text(`Найкраща: ${maxFit}`, this.xOffset + 10, height - 80);
    text(`Середня: ${avgFit.toFixed(1)}`, this.xOffset + 10, height - 60);
    text(`Найкращі за покоління: ${this.fitnessHistory.join(", ")}`, this.xOffset + 10, height - 40);
  }
}

function generatePopulation(size, geneLength) {
  return Array.from({ length: size }, () =>
    Array.from({ length: geneLength }, () => (Math.random() < 0.5 ? 0 : 1))
  );
}

function binaryToDecimal(binary) {
  return binary.reduce((sum, bit, i) => sum + bit * Math.pow(2, binary.length - i - 1), 0);
}

function fitness(individual) {
  const x = binaryToDecimal(individual);
  return x * x;
}

function selectParent(population, fitnessScores) {
  const tournamentSize = 3;
  const tournament = [];
  for (let i = 0; i < tournamentSize; i++) {
    const idx = Math.floor(Math.random() * population.length);
    tournament.push({ individual: population[idx], fitness: fitnessScores[idx] });
  }
  return tournament.sort((a, b) => b.fitness - a.fitness)[0].individual;
}

function crossover(p1, p2) {
  const point = Math.floor(Math.random() * p1.length);
  return [
    p1.slice(0, point).concat(p2.slice(point)),
    p2.slice(0, point).concat(p1.slice(point))
  ];
}

function mutate(individual, rate) {
  return individual.map(bit => (Math.random() < rate ? 1 - bit : bit));
}
