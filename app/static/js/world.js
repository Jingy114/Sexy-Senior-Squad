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
let x = 0;
let y = 0;
let z = 0;

let datasets = ["Data a", "Data b", "Data c"];

function setup(info) {
  //Initilaize Selction List
  // build_list();

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
  for (let i = 0; i < country_list.length; i++) {
    let country_name = country_list[i];
    let country_js = document.getElementById(country_name);
    country_js.addEventListener("mouseover", function() {
      let country_true_name = country_name.replaceAll("_", " ");
      console.log(country_true_name); //Will be used for popover
      let selected_country_display = document.getElementById("selected_country");
      // let selected_country_display_text = document.createTextNode(country_true_name);
      // selected_country_display.appendChild(selected_country_display_text);
      selected_country_display.innerHTML = country_true_name;
    });
  }
  //Remove loading notif
  let loading_screen = document.getElementById('load');
  loading_screen.remove();

  //Initialize Colors
  update_colors();

  //rotate_to(x,y,z);

  //Button testing rotate stuff
  let button = document.getElementById('rotate');
  button.addEventListener("click", rotate_left);

  //Mouse rotate stuff
  let moveable_globe = document.getElementById('map');
  //moveable_globe.addEventListener("mousemove", rotate_to); //+mousedown + mousemove/mouseover?
  //Currently only triggers on the borders themselves
}

//Colors each country according to 'country_color()'
function update_colors() {
  for (let i = 0; i < country_list.length; i++) {
    let country_name = country_list[i];
    let country_d3 = d3.select('#globe g.map')
      .select('#' + country_name)
      .style("fill", country_color(country_name));
  }
}

function country_color(country_name) {
  return 'red';
}

//Builds selection lists based on 'databases'
async function build_lists() {
  //console.log(chosen_dataset);
  let list = document.getElementById('selection_list');
  let selector1 = document.getElementById('dataset_selector_1');
  let selector2 = document.getElementById('dataset_selector_2');
  for (let i = 0; i < datasets.length; i++) {
    let dataset = datasets[i];
    let new_list_elem = document.createElement('li');
    new_list_elem.className = "list-group-item list-group-item-action";
    let new_list_elem_link = document.createElement('a');
    new_list_elem_link.href = "load/"+dataset;
    let new_list_elem_text = document.createTextNode(dataset);
    new_list_elem_link.appendChild(new_list_elem_text);
    new_list_elem.appendChild(new_list_elem_link);
    list.appendChild(new_list_elem);
    //console.log(new_list_elem);
    let new_selector_elem = document.createElement('option');
    let new_selector_elem_text = document.createTextNode(dataset);
    new_selector_elem.value = i;
    new_selector_elem.appendChild(new_selector_elem_text);
    second_new_selector_elem = new_selector_elem.cloneNode(true);
    selector1.appendChild(new_selector_elem);
    selector2.appendChild(second_new_selector_elem);
  }
  if (datasets.length == 0) {
    let new_list_elem = document.createElement('li');
    new_list_elem.className = "list-group-item";
    let new_list_elem_text = document.createTextNode("No Datsets Loaded");
    new_list_elem.appendChild(new_list_elem_text);
    list.appendChild(new_list_elem);
  }
}

// async function load_screen(){
//   let load_screen = document.getElementById()
// }

function select_function(form) {
  let operation = form.operation.value;
  console.log(operation);
  let operation_display = document.getElementById("operation");
  console.log(operation_display);
  //operation_display.innerHtml = operation;
  //Have to see why this reloads page...........
}

var rotate_left = function() {
  x += 45;
  console.log([x, 0, 0]);
  projection.rotate([x, 0, 0]);
  d3.select('svg')
    .selectAll("path")
    .attr('d', map);
  //console.log(rotation_array)
}

let sensitity = 1 / 10;

var rotate_to = function(e) {
  let dx = event.offsetX * sensitity - x;
  x = event.offsetX * sensitity;
  let dy = event.offsetY * sensitity - y;
  y = event.offsetY * sensitity;
  //console.log(x+" ,"+y);
  projection.rotate([dx, dy, z]);
  d3.select('svg')
    .selectAll("path")
    .attr('d', map);
}

//load_screen();
build_lists();
get_data(setup);
