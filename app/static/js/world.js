//let file_data = readFile("../countries/country_data.json")

// let file = open("../countries/country_data.json");
//


function getData(callback) {
  fetch('../static/countries/country_data.json')
    .then(response => response.json())
    .then(data => {
      callback(data);
    });
}

function run(info) {
  let world_data = info;

  let projection = d3.geoOrthographic();

  let thingy =  d3.geoPath().projection(projection); //Have to look into exactly what this step creates

  let world =  d3.select('#globe g.map').selectAll('path');
  console.log(world);
  world =  world.data(world_data.features);

  world.enter().append('path').attr('d', thingy);
}

getData(run);
