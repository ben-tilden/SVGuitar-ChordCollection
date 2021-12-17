const Benchmark = require('benchmark');

const parseJSONNested = require('./nestedAlgo');
const parseJSONString = require('./stringAlgo');
const parseJSONObject = require('./objectAlgo');

const chordsDBNested = require('./completeChordsFormattedNested');
const chordsDBString = require('./completeChordsFormattedString');
const chordsDBObject = require('./completeChordsFormattedObject');

const suite = new Benchmark.Suite;

// add tests
suite.add('Nested', () => parseJSONNested(chordsDBNested))
    .add('String', () => parseJSONString(chordsDBString))
    .add('Object', () => parseJSONObject(chordsDBObject))
    // add listeners
    .on('cycle', function(event) {
        console.log(String(event.target));
    })
    .on('complete', function() {
        console.log('Fastest is ' + this.filter('fastest').map('name'));
    })
    // run async
    .run({ 'async': true });
