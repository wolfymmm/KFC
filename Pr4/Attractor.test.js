describe('Attractor', function () {
  it('створюється з правильними координатами', function () {
    const a = new Attractor(1, 2, 3, 'red');
    expect(a.x).to.equal(1);
    expect(a.y).to.equal(2);
    expect(a.z).to.equal(3);
    expect(a.c).to.equal('red');
    expect(a.history).to.be.an('array').that.is.empty;
  });

  it('update() змінює координати і додає до history', function () {
    const a = new Attractor(1, 1, 1, 'blue');
    const prevLength = a.history.length;

    a.update();

    expect(a.x).to.not.equal(1); // x має змінитися
    expect(a.history.length).to.equal(prevLength + 1); // history додався
    const last = a.history[a.history.length - 1];
    expect(last).to.have.all.keys('x', 'y', 'z'); // перевіримо структуру об'єкта
  });
});
