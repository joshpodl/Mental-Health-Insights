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
    xaxis: {title: 'Year'},
    font: {size: 8},
};

Plotly.newPlot("bar", bar, layout);

// Pie chart: know options data

// Populate dropdown
function dropdown(){
    var drop = d3.select("#selDataset")
    years.forEach((data)=>{
            drop.append("option")
            .text(data)
            .property("value", data);
        });
        var sample = years[0];
        plots(sample);
};
dropdown();

// // Create bar chart and bubble chart
// function plots(sampleID){
//     d3.json("samples.json").then((sampledata)=>{
//         var samples = sampledata.samples;
//         var dataArray = samples.filter(row=>row.id==sampleID);
//         console.log(dataArray);
//         var sample = dataArray[0];
//         var otu_ids = sample.otu_ids;
//         var sample_values = sample.sample_values;
//         var otu_labels = sample.otu_labels;

//         // Bar chart
//         var barData = [{
//             x: sample_values.slice(0,10).reverse(),
//             y: otu_ids.slice(0,10).map(otu_ids=>`OTU${otu_ids}`).reverse(),
//             text: otu_labels.slice(0,10).reverse(),
//             type: "bar",
//             orientation: "h"
//         }];
//         Plotly.newPlot("bar", barData);

//         // Bubble chart
//         var bubbleData = [{
//             x: otu_ids,
//             y: sample_values,
//             mode: "markers",
//             marker: {
//                 size: sample_values,
//                 color: otu_ids},
//             text: otu_labels 
//         }];
//         Plotly.newPlot("bubble", bubbleData);
//     });
// };

// // Have metadata and plots appear when an ID is clicked
// function optionChanged(newData){
//     plots(newData);
// };