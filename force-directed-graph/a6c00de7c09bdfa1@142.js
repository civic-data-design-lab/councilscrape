// https://observablehq.com/@d3/force-directed-graph@142

export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["2020_articles.json",new URL("./files/2020_nodes2.txt",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function(md){return(
md`# 2020 NYC Article Topics
 
This visualization displays the most prominent topics from 2020 in New York City, as scraped from the New York Times and then topic modelled. The links indicate when the same article span multiple topics. The topic-color correlation is as follows:

Gray:  Foie Gras Ban, Orange: Primaries, Blue: Coronavirus, Red: BLM Police Protests, Purple: BLM Defunding the Police, Green:  Plastic Bag Ban, Brown: Medallion City Council Task Force, Pink: ICE`
)});
  main.variable(observer("chart")).define("chart", ["data","d3","width","height","color","drag","invalidation"], function(data,d3,width,height,color,drag,invalidation)
{
  const links = data.links.map(d => Object.create(d));
  const nodes = data.nodes.map(d => Object.create(d));

  var x = d3.scaleOrdinal()
  .domain(["Foie Gras Ban","Primaries", "Coronavirus", "BLM Police Protest", "BLM Defunding Police","Plastic Bag Ban","Medallion City Council Task Force","ICE"])
  .range([0, 100, 200, 300, 400, 500, 600, 700])


  const simulation = d3.forceSimulation(nodes)
      .force("x", d3.forceX().strength(0.2).x( function(d){ return x(d.topic) } ))
      .force("y", d3.forceY().strength(0.2).y( height/2 ))
      .force("link", d3.forceLink(links).id(d => d.id).strength(0.05))
      .force("charge", d3.forceManyBody().strength(-20))
      .force("center", d3.forceCenter(width / 2, height / 2));

  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

  const link = svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line")
      .attr("stroke-width", d => Math.sqrt(d.value));

  const node = svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
      .attr("r", 5)
      .attr("fill", color)
      .call(drag(simulation));

  node.append("title")
      .text(d => d.id);

  simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
  });


  invalidation.then(() => simulation.stop());

  return svg.node();
}
);
  main.variable(observer("data")).define("data", ["FileAttachment"], function(FileAttachment){return(
FileAttachment("2020_articles.json").json()
)});
  main.variable(observer("height")).define("height", function(){return(
600
)});
  main.variable(observer("color")).define("color", ["d3"], function(d3)
{
  const scale = d3.scaleOrdinal(d3.schemeCategory10);
  return d => scale(d.topic);
}
);
  main.variable(observer("drag")).define("drag", ["d3"], function(d3){return(

simulation => {

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  
  
  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }
  
  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
  
  
  return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}


)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@5")
)});
  return main;
}
