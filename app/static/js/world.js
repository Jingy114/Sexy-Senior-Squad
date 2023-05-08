//let file_data = readFile("../countries/country_data.json")

// let file = open("../countries/country_data.json");
//


async function getData() {
  let data = await fetch('../static/countries/country_data.json');
  let info = await data.text();
  return info;
}

async function run() {
  let file_data = ```
  { "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
      "properties": {"prop0": "value0"}
      },
    { "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
          ]
        },
      "properties": {
        "prop0": "value0",
        "prop1": 0.0
        }
      },
    { "type": "Feature",
       "geometry": {
         "type": "Polygon",
         "coordinates": [
           [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
             [100.0, 1.0], [100.0, 0.0] ]
           ]

       },
       "properties": {
         "prop0": "value0",
         "prop1": {"this": "that"}
         }
       }
    ]
  }```;//await getData();
  let world_data = await JSON.parse(file_data);
  console.log(world_data);

  let projection = d3.geoOrthographic();

  let thingy = d3.geoPath().projection(projection); //Have to look into exactly what this step creates

  let world = d3.select('#globe g.map').selectAll('path').data(world_data.features);

  world.enter().append('path').attr('d', thingy);
}

run();
