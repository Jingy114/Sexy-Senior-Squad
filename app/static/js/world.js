//let file_data = readFile("../countries/country_data.json")

// let file = open("../countries/country_data.json");
//
// let file_data = file.read();

console.log(file_data);
let world_data = JSON.parse(file_data);
console.log(world_data);

let projection = d3.geoOrthographic();

let thingy = d3.geoPath().projection(projection); //Have to look into exactly what this step creates

let world = d3.select('#globe g.map').selectAll('path').data(world_data.features);

world.enter().append('path').attr('d', thingy);
