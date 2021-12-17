
const parseJSONString = (json) => {
    for (const chordName in json) {
        for (const variation of json[chordName]) {
            const convertedString = JSON.parse(variation['fingers']);
            // console.log(`title: ${variation['title']}`);
            // console.log(`fingers: ${JSON.stringify(convertedString)}`);
            // console.log(`barres: ${JSON.stringify(variation['barres'])}`);
            // console.log(`position: ${variation['position']}`);
            // console.log('----------------------------------');
        }
    }
}

module.exports = parseJSONString;
