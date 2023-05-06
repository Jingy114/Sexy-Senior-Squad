//let world_data = get from Natural Earth

"../countries/ne_50m_admin_0_countries.shx".json()

let projection = d3.geoOrthographic();

let thingy = d3.geoPath().projection(projection); //Have to look into exactly what this step creates

let world = d3.select('#globe g.map').selectAll('path').data(geojson.features);

world.enter().append('path').attr('d', thingy);
