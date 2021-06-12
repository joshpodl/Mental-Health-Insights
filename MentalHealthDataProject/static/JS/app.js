// Make sure data is reading properly

var lineData1 = phyData.slice(1,-1);
var lineData2 = mentData.slice(1,-1);
var barData = industryData.slice(1,-1);
var pieData = knowData.slice(1,-1);

// console.log(lineData1);
// console.log(lineData2);
// console.log(barData);
// console.log(pieData);

var line1 = JSON.parse(lineData1);
var line2 = JSON.parse(lineData2);
var bar = JSON.parse(barData);
var pie = JSON.parse(pieData);

// console.log(line1);
// console.log(line2);
// console.log(bar);
// console.log(pie);


// Extract data for traces
var years = line1.map(function(data) {
    return data.year;
  });
console.log(years);

var physical = line1.map(function(data) {
    return data.avg_physical_importance;
});
console.log(physical);

var mental = line2.map(function(data) {
    return data.avg_mental_importance;
});
console.log(mental);

var industry= bar.map(function(data) {
    return data.avg_industry_support;
});
console.log(industry);

var know_yes = pie.map(function(data) {
    return data.count_x;
});
console.log(know_yes);

var know_no = pie.map(function(data) {
    return data.count_y;
});
console.log(know_no);

// Multiple line graph: physical data and mental data

// Create traces
var trace1 = {
    x: years,
    y: physical,
    name: "physical",
    type: "scatter"
};

var trace2 = {
    x: years,
    y: mental,
    name: "mental",
    type: "line"
};

var multiLine = [trace1, trace2];

// Create layout
var layout = {
    title: `Importance of Physical Health vs Importance of Mental Health`,
    yaxis: {title: 'Average Rating', range: [1,10]},
    xaxis: {title: 'Year', range: [2016, 2021]},
    font: {size: 8},
};

Plotly.newPlot("line", multiLine, layout);

// Bar graph: industry data

// Create trace
var trace = {
    x: years,
    y: industry,
    type: "bar"
};

var bar = [trace];

var layout = {
    title: `Industry Support with Mental Health Resources`,
    yaxis: {title: 'Average Rating', range: [0,5]},
    xaxis: {title: 'Year', showticklabels: false},
    font: {size: 8}   
};

Plotly.newPlot("bar", bar, layout);

// Pie chart: know options data

// Organize data
var pie1 = [know_yes[0], know_no[0]];
var pie2 = [know_yes[1], know_no[1]];
var pie3 = [know_yes[2], know_no[2]];
var pie4 = [know_yes[3], know_no[3]];
var labels = ["yes", "no"];

// Plot
function init() {
    var data = [{
      values: pie1,
      labels: labels,
      type: "pie"
    }];
    Plotly.newPlot("pie", data);
};

d3.selectAll("#selDataset").on("change", getData);

function getData() {
    var dropdownMenu = d3.select("#selDataset");
    var dataset = dropdownMenu.property("value");
    var data = []

    if (dataset == '2017') {
        values = pie1;
    }
    
    else if (dataset == '2018') {
        values = pie2;
    }

    else if (dataset == '2019') {
       values = pie3;
    }

    else if (dataset == '2020') {
        values = pie4;
    }

    updatePlotly(values);
};

function updatePlotly(newData) {
    Plotly.restyle("pie", "values", [newData])
};

init()