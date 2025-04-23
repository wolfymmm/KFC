const config = {
  populationSize: 10,
  geneLength: 10,
  generations: 20,
  mutationRate: 0.01,
  tournamentSize: 3
};

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
  const tournament = [];
  for (let i = 0; i < config.tournamentSize; i++) {
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

function nextGeneration(population, fitnessScores) {
  const sorted = population.map((ind, i) => ({ ind, fit: fitnessScores[i] }))
                         .sort((a, b) => b.fit - a.fit);

  const elite = sorted.slice(0, 2).map(e => e.ind); // Еліта
  const newGen = [...elite];

  while (newGen.length < config.populationSize) {
    const p1 = selectParent(population, fitnessScores);
    const p2 = selectParent(population, fitnessScores);
    let [c1, c2] = crossover(p1, p2);
    c1 = mutate(c1, config.mutationRate);
    c2 = mutate(c2, config.mutationRate);
    newGen.push(c1);
    if (newGen.length < config.populationSize) newGen.push(c2);
  }

  return newGen;
}

function runGA() {
  let population = generatePopulation(config.populationSize, config.geneLength);
  let best = null;

  for (let generation = 0; generation < config.generations; generation++) {
    const fitnessScores = population.map(fitness);
    const maxFit = Math.max(...fitnessScores);
    const bestIndex = fitnessScores.indexOf(maxFit);
    best = population[bestIndex];

    console.log(`Покоління ${generation + 1}: Найкраща придатність = ${maxFit}\n`);
    population = nextGeneration(population, fitnessScores);
  }

  console.log("\nНайкраща особина:", best);
  console.log("Значення x:", binaryToDecimal(best));
  console.log("Придатність:", fitness(best));
}

runGA();

// ЮНІТ-ТЕСТИ
console.assert(generatePopulation(5, 8).length === 5, "Помилка генерації популяції");
console.assert(typeof fitness([1,0,1]) === "number", "Fitness має бути числом");
console.assert(selectParent(generatePopulation(5, 4), [1,2,3,4,5]).length === 4, "selectParent повертає некоректну особину");
console.assert(crossover([1,1,1,1], [0,0,0,0]).length === 2, "Кросовер має повертати двох нащадків");
console.assert(mutate([1,1,1,1], 1).includes(0), "Мутація не працює при 100%");