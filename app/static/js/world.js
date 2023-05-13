function get_data(callback) {
  fetch('../static/data/country_data.json')
    .then(response => response.json())
    .then(data => {
      //console.log(data);
      callback(data);
    });
}

let country_list = [];
let projection;
let map;
let x,y,z=0;

function setup(info) {
  //Get data from callback 'get_data()'
  let world_data = info;

  //Generate Countries
  projection = d3.geoOrthographic();
  map = d3.geoPath().projection(projection);
  let world = d3.select('#globe g.map')
    .selectAll('path')
    .data(world_data.features)
    .enter()
    .append('path')
    .attr('d', map)
    .attr("id", function(d) {
      country_with_spaces = d.properties.ADMIN;
      country = country_with_spaces.replaceAll(" ", "_");
      country_list.push(country);
      return country;
    });

    //Setup Popover Labels for Countries
    for (let i = 0; i<country_list.length; i++) {
      let country_name = country_list[i];
      let country_js = document.getElementById(country_name);
      country_js.addEventListener("mouseover", function(){
        let country_true_name = country_name.replaceAll("_", " ");
        console.log(country_true_name); //Will be used for popover
      });
    }

    //Initialize Colors
    update_colors();

    x = -50;

    //rotate_to(x,y,z);

    //Button testing rotate stuff
    let button = document.getElementById('rotate');
    button.addEventListener("click", rotate_test);

    //Mouse rotate stuff
    let moveable_globe = document.getElementById('map');
    //moveable_globe.addEventListener("mousemove", rotate_to); //+mousedown + mousemove/mouseover?
    //Currently only triggers on the borders themselves
}

//Colors each country according to 'country_color()'
function update_colors() {
  for (let i = 0; i<country_list.length; i++) {
    let country_name = country_list[i];
    let country_d3 = d3.select('#globe g.map')
      .select('#'+country_name)
      .style("fill", country_color(country_name));
  }
}


function country_color(country_name) {
  return 'red';
}

var rotate_test = function(){
  projection.rotate([90,0,0]);
  d3.select('svg')
    .selectAll("path")
    .attr('d', map);
  //console.log(rotation_array)
}

let sensitity = 1/10;

var rotate_to = function(e){
  let dx = event.offsetX*sensitity - x;
  x = event.offsetX*sensitity;
  let dy = event.offsetY*sensitity - y;
  y = event.offsetY*sensitity;
  //console.log(x+" ,"+y);
  projection.rotate([dx,dy,z]);
  d3.select('svg')
    .selectAll("path")
    .attr('d', map);
}

get_data(setup);
