function get_data(callback) {
  fetch('../static/data/country_data.json')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      callback(data);
    });
}

let country_list = [];

function run(info) {
  let world_data = info;

  let projection = d3.geoOrthographic();

  let thingy =  d3.geoPath().projection(projection); //Have to look into exactly what this step creates

  let world =  d3.select('#globe g.map')
    .selectAll('path')
    .data(world_data.features)
    .enter()
    .append('path')
    .attr('d', thingy)
    .attr("id", function(d) {
      country_with_spaces = d.properties.ADMIN;
      country = country_with_spaces.replaceAll(" ", "");
      country_list.push(country);
      return country;
    });

    console.log(country_list);
    update_colors();
}

function update_colors() {
  for (let i = 0; i<country_list.length; i++) {
    let country_name = country_list[i];
    let country = d3.select('#globe g.map')
      .select('#'+country_name)
      .style("fill", country_color(country_name));
  }
}

function country_color(country_name) {
  return 'red';
}

get_data(run);
//update_colors();
