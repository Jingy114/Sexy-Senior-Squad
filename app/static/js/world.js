function getData(callback) {
  fetch('../static/data/country_data.json')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      callback(data);
    });
}

function run(info) {
  let world_data = info;

  let projection = d3.geoOrthographic();

  let thingy =  d3.geoPath().projection(projection); //Have to look into exactly what this step creates

  let world =  d3.select('#globe g.map')
    .selectAll('path')
    .data(world_data.features)
    .enter()
    .append('path')
    .attr('d', thingy);

  let country = d3.select('#globe g.map')
    .select('path')
    .style("fill", country_color("a"));
}

function country_color(country_name) {
  console.log(country_name);
  return 'red';
}

getData(run);
