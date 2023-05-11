function get_data(callback) {
  fetch('../static/data/country_data.json')
    .then(response => response.json())
    .then(data => {
      //console.log(data);
      callback(data);
    });
}

let country_list = [];
let rotation_array = [0, 0, 0];
let projection;

function setup(info) {
  let world_data = info;

  projection = d3.geoOrthographic()
    .rotate(rotation_array);
    //.fitExtent([[0,0], [500,500]]);

  let map = d3.geoPath().projection(projection);

  let world = d3.select('#globe g.map')
    .selectAll('path')
    .data(world_data.features)
    .enter()
    .append('path')
    .attr('d', map)
    .attr("id", function(d) {
      country_with_spaces = d.properties.ADMIN;
      country = country_with_spaces.replaceAll(" ", "");
      country_list.push(country);
      return country;
    });

    //console.log(country_list);
    update_colors();

    //Button testing rotate stuff
    let button = document.getElementById('rotate');
    button.addEventListener("click", rotate_test);
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

get_data(setup);
//update_colors();

var rotate_test = function(){
  rotation_array[0] += 90;
  projection.rotate(rotation_array);
  let map = d3.geoPath().projection(projection);
  let world = d3.select('#globe g.map')
    .attr('d', map);
  console.log(rotation_array)
  get_data(setup);
}
