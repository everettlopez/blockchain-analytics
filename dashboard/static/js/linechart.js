// --- Simple D3 Line Chart Starter ---

const raw = document.getElementById("eth-data").textContent.trim(); 
const data = JSON.parse(raw).map(d => ({ timestamp: new Date(d.timestamp), price: d.price }));

// Chart dimensions
const width = 400;
const height = 200;
const margin = { top: 20, right: 30, bottom: 30, left: 40 };

// Create SVG
const svg = d3.select("#price-chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Scales
const x = d3.scaleTime()
    .domain(d3.extent(data, d => d.timestamp))
    .range([margin.left, width - margin.right]);

const y = d3.scaleLinear()
    .domain([d3.min(data, d => d.price), d3.max(data, d => d.price)])
    .range([height - margin.bottom, margin.top]);

// Line generator
const line = d3.line()
    .x(d => x(d.timestamp))
    .y(d => y(d.price));

// Draw line
svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "#4CAF50")
    .attr("stroke-width", 2)
    .attr("d", line);

// X axis
svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(5));

// Y axis
svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y));
