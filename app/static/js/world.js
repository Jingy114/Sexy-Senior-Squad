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

  let country_list = [];

  let world =  d3.select('#globe g.map')
    .selectAll('path')
    .data(world_data.features)
    .enter()
    .append('path')
    .attr('d', thingy)
    .attr("id", function(d) {
      country = d.properties.ADMIN;
      country_list.push(country);
      return country;
    });
  }
}

function update_colors() {

}


    console.log(country_list);
  for (let i = 0; i<country_list.length; i++) {
    let country = d3.select('#globe g.map')
      .selectAll('path').filter(d => d.properties.ADMIN == country?) //Less efficient way but will be used for now until I can set IDs to each country
      .style("fill", country_color("a"));
  }
}

function country_color(country_name) {
  console.log(country_name);
  return 'red';
}

getData(run);
