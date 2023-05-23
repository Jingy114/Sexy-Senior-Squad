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

let country_true_name = "N/A";
let would_be_country_true_name = "N/A";
let country_hold = false;

let operation = "Multiplied By";
let datasets = ["Data c", "Data d", "Data f"];

//let data = [];

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
      would_be_country_true_name = country_name.replaceAll("_", " ");
      console.log(would_be_country_true_name);
      if (country_hold == false) {
        country_true_name = would_be_country_true_name;
        //console.log(country_true_name); //Will be used for popover
        let selected_country_display = document.getElementById("selected_country");
        // let selected_country_display_text = document.createTextNode(country_true_name);
        // selected_country_display.appendChild(selected_country_display_text);
        selected_country_display.innerHTML = country_true_name;
      }
    });
  }

  //Country hold on click
  let svg = document.getElementById('svg');
  svg.addEventListener('click', save_current);

  //Remove loading notif
  let loading_screen = document.getElementById('load');
  loading_screen.remove();

  //Initialize Colors
  update_colors([]); // data elements

  //rotate_to(x,y,z);

  //Button rotate functions
  document.getElementById('rotate_left').addEventListener("click", rotate_left);
  document.getElementById('rotate_right').addEventListener("click", rotate_right);
  document.getElementById('rotate_up').addEventListener("click", rotate_up);
  document.getElementById('rotate_down').addEventListener("click", rotate_down);

  //Mouse rotate stuff
  let moveable_globe = document.getElementById('map');
  //moveable_globe.addEventListener("mousemove", rotate_to); //+mousedown + mousemove/mouseover?
  //Currently only triggers on the borders themselves
}

//Colors each country according to 'country_color()'
function update_colors(data) {
  console.log(data);
  for (let i = 0; i < country_list.length; i++) {
    let country_name = country_list[i];
    let country_d3 = d3.select('#globe g.map')
      .select('#' + country_name)
      .style("fill", country_color(country_name, data));
  }
}

function country_color(country_name, data) {
  //console.log(select_data("test.db", "*", "USA"))
  if (data.length != 0){
    return 'green';
  }
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
    // HAVE TO TURN THESE TO FORMS
    let new_list_elem_form = document.createElement('form');
    new_list_elem_form.action = "/form-submit";
    new_list_elem_form.setAttribute("onsubmit", "process_data(this); return false;");
    let new_list_elem_input = document.createElement('input');
    new_list_elem_input.type = "submit";
    new_list_elem_input.value = dataset;

    //action="/form-submit" onsubmit="process_data(this); return false;"
    //let new_list_elem_text = document.createTextNode(dataset);
    //new_list_elem_input.appendChild(new_list_elem_text);
    new_list_elem_form.appendChild(new_list_elem_input);
    new_list_elem.appendChild(new_list_elem_form);
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

function select_function(chosen_operation) {
  let operation_display = document.getElementById("operation");
  operation_display.innerHTML = chosen_operation;
  operation = chosen_operation;
}

function run_data_function(form) {
  console.log("test");
}

let sens = 45;

var rotate_left = function() {
  x += sens;
  rotate_globe();
}

var rotate_right = function() {
  x -= sens;
  rotate_globe();
}

var rotate_up = function() {
  y -= sens;
  rotate_globe();
}

var rotate_down = function() {
  y += sens;
  rotate_globe();
}

function rotate_globe(){
  projection.rotate([x, y, 0]);
  d3.select('svg')
    .selectAll("path")
    .attr('d', map);
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

var save_current = function(e) {
  if (country_true_name == 'N/A') {
    return false;
  }
  let hold_indication = document.getElementById('selected_hold');
  let country_name = country_true_name.replaceAll(" ", "_");
  let country_d3 = d3.select('#globe g.map')
    .select('#' + country_name);
  if (country_hold == true) {
    country_hold = false;
    hold_indication.innerHTML = "false";
    country_true_name = would_be_country_true_name;
    let selected_country_display = document.getElementById("selected_country");
    selected_country_display.innerHTML = country_true_name;
    country_d3.style("fill", country_color(country_name, []));
    return false;
  }
  country_hold = true;
  //Show data
  hold_indication.innerHTML = "true";
  country_d3.style("fill", "#257AFD");
  return true;
}

function process_data(formElement) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === this.DONE) {
        console.log('test!');
        let data = xhttp.responseText;
        update_colors(data);
      }
    };
    xhttp.open(formElement.method, formElement.action, true);

    //update_colors();
    var data_form = new FormData(formElement);
    return false;
}


//load_screen();
build_lists();
get_data(setup);
