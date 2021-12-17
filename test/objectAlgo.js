
const parseJSONObject = (json) => {
    for (const chordName in json) {
        for (const variation of json[chordName]) {
            const convertedObject = Object.entries(variation['fingers'])
                .map((entry) => [parseInt(entry[0]), ...entry[1]]);
            // console.log(`title: ${variation['title']}`);
            // console.log(`fingers: ${JSON.stringify(convertedObject)}`);
            // console.log(`barres: ${JSON.stringify(variation['barres'])}`);
            // console.log(`position: ${variation['position']}`);
            // console.log('----------------------------------');
        }
    }
}

module.exports = parseJSONObject;
