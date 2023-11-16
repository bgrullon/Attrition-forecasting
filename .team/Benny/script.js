import {addTooltips} from "./tooltip.js"

const response = await fetch('./us-counties-10m.json');
const us = await response.json();
const counties = topojson.feature(us, us.objects.counties)
const states = topojson.feature(us, us.objects.states)
const diplomas = [ 'NoHSB', 'HSB', 'CAD', 'BD']

const updatePlot = () => {
    const dropdownCat = d3.select("#selCategory");
    const category = dropdownCat.property("value");
    const dropdownYear = d3.select("#selYear");
    const year = dropdownYear.property("value");

    if (diplomas.includes(category)) {
        plotData(`${category}`)
    } else {
        plotData(`${category}${year}`)
    }
}

d3.selectAll("#selCategory").on("change", updatePlot);
d3.selectAll("#selYear").on("change", updatePlot);

const plotData = async (category = 'Unemployed_2020') => {
    // fetch data from flask
    const data = await fetch('http://127.0.0.1:5000/counties', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: category }),
    });

    // convert data to map
    const countyData = await data.json();
    const countyDataMap = new Map();

    for (const key in countyData) {
    if (countyData.hasOwnProperty(key)) {
        countyDataMap.set(key, countyData[key]);
    }
    }

    // set min and max
    const valuesArray = [...countyDataMap.values()]
    const maxValue = Math.max(...valuesArray);
    const minValue = Math.min(...valuesArray);


    const plotMap = Plot.plot({
        projection: "albers-usa",
        marks: [
            Plot.geo(counties, { 
                fill: (d) => countyDataMap.get(`${Number(d.id)}`),
                title: (d) => `${d.properties.name} County \n ${countyDataMap.get(`${Number(d.id)}`)} ${category.split('_')[0]}`
            }),
            Plot.geo(states, {stroke: "#fff", strokeWidth: 0.5})
        ],
        color: {
            scheme: "pubugn",
            unknown: "#ddd",
            type: "linear",
            legend: true,
            percent: true,
            domain: [minValue, maxValue]
        }
    })

    const mapDiv = document.querySelector("#map");
    mapDiv.innerHTML = ''
    mapDiv.append(addTooltips(plotMap));

    // const plotBar = Plot.plot({
    //     projection: "albers-usa",
    //     marks: [
    //         Plot.geo(counties, { 
    //             fill: (d) => countyDataMap.get(`${Number(d.id)}`),
    //             title: (d) => `${d.properties.name} County \n ${countyDataMap.get(`${Number(d.id)}`)} ${category.split('_')[0]}`
    //         }),
    //         Plot.geo(states, {stroke: "#fff", strokeWidth: 0.5})
    //     ],
    //     color: {
    //         scheme: "pubugn",
    //         unknown: "#ddd",
    //         type: "linear",
    //         legend: true,
    //         percent: true,
    //         domain: [minValue, maxValue]
    //     }
    // })

    // const barDiv = document.querySelector("#bar-plot");
    // barDiv.innerHTML = ''
    // barDiv.append(addTooltips(plotBar));
}

await plotData()