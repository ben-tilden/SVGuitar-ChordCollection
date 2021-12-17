
const parseJSONNested = (json) => {
    for (const chordName in json) {
        for (const variation of json[chordName]) {
            const convertedNested = variation['fingers'];
            // console.log(`title: ${variation['title']}`);
            // console.log(`fingers: ${JSON.stringify(convertedNested)}`);
            // console.log(`barres: ${JSON.stringify(variation['barres'])}`);
            // console.log(`position: ${variation['position']}`);
            // console.log('----------------------------------');
        }
    }
}

module.exports = parseJSONNested;
