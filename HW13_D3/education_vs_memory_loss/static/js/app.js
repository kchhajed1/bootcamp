d3.select(window).on("resize", makeResponsive);
makeResponsive();

function makeResponsive() {
  var svgArea = d3.select(".chart")
                  .select("svg");
  if (!svgArea.empty()) {
    svgArea.remove();
  }
  
  var svgWidth = window.innerWidth;
  var svgHeight = window.innerHeight;

  var margin = {
    top: 50,
    right: 100,
    bottom: 130,
    left: 100
  };

  var width = svgWidth - margin.left - margin.right;
  var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper.
  var svg = d3.select(".chart")
              .append("svg")
              .attr("width", svgWidth)
              .attr("height", svgHeight);

  var chartGroup = svg.append("g")
                      .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Import Data
d3.csv("static/js/mind_data.csv", function (err, mind_data) {
  if (err) throw err;

  // Step 1: Parse Data/Cast as numbers
   // ==============================
  mind_data.forEach(function (data) {
    data.memory = +data.memory;
    data.hs = +data.hs;
  });

  // Step 2: Create scale functions
  // ==============================
  var xLinearScale = d3.scaleLinear()
    .domain([0, d3.max(mind_data, d => d.memory) + 4])
    .range([0, width]);

  var yLinearScale = d3.scaleLinear()
    .domain([0, d3.max(mind_data, d => d.hs) + 5] )
    .range([height, 0]);

  // Step 3: Create axis functions
  // ==============================
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Step 4: Append Axes to the chart
  // ==============================
  chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

  chartGroup.append("g")
    .call(leftAxis);

   // Step 5: Create Circles
  // ==============================
  var dataset = chartGroup.selectAll("circle")
  .data(mind_data)
  .enter()
  
  var circlesGroup = dataset.append("circle")
  .attr("cx", d => xLinearScale(d.memory))
  .attr("cy", d => yLinearScale(d.hs))
  .attr("r", "15")
  .attr("fill", "rgb(41, 128, 185)")
  .attr("opacity", ".5")
  
var text1 = dataset.append("text")
    .attr("dx", function(d){ return xLinearScale(d.memory);})
    .attr("dy", function(d){ return yLinearScale(d.hs);})
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "central")
    .text(function(d){ return (d.state);})
    .attr("class", "bubbleText");  

  // Step 6: Initialize tool tip
  // ==============================
  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -60])
    .html(function (d) {
      return (`${d.name}<br>High School: ${d.hs}<br>Memory: ${d.memory}`);
    });

  // Step 7: Create tooltip in the chart
  // ==============================
  chartGroup.call(toolTip);

  // Step 8: Create event listeners to display and hide the tooltip
  // ==============================
  circlesGroup.on("mouseover", function (data) {
      toolTip.show(data);
    })
    // onmouseout event
    .on("mouseout", function (data, index) {
      toolTip.hide(data);
    });

  // Create axes labels
  chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 40)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("class", "axisText")
    .text("Percent Population, High School Education ")
    
  chartGroup.append("text")
    .attr("transform", `translate(${width/2}, ${height + margin.top + 00})`)
    .attr("class", "axisText")
    .text("Percent Experiencing Memory Loss");
    
  chartGroup.append("text")
      .attr("transform", `translate(${width/2})`)
      .attr("class", "titleText")
      .text("High School Education v. Memory Loss");
    
// Add analysis.
d3.select(".text")
.html(`
<strong>ANALYSIS</strong><br><br>Data from 2014 was extracted from two databases: the U.S. Census Bureau's American Community Survey, and the Behavioral Risk Factor Surveillance System (BRFSS).  Data for the percent population attaining high school were obtained from the Census Bureau.  
Data for the percent survey respondents indicating serious difficulty concentrating, remembering, or making decisions were obtained from the (BRFSS).<br><br>
Data points represent values for each state; each state is indicated by its abbreviation.  More information for each data point can be obtained by hovering over each circle. Overall, the data indicate that with increased education levels, cognitive defect is less likely.  This indicates that the correlation between a high school interaction and mental defect is moderate. <br><br><hr><br<br><br>`);
    
})};