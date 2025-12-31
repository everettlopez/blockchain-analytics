// Sample income data (replace with real data later)
const incomeData = [10, 12, 8, 15, 20, 18, 25];

function renderIncomeSparkline() {
    const width = 100;
    const height = 40;

    const svg = d3.select("#income-sparkline")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const x = d3.scaleLinear()
        .domain([0, incomeData.length - 1])
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([d3.min(incomeData), d3.max(incomeData)])
        .range([height, 0]);

    const line = d3.line()
        .x((d, i) => x(i))
        .y(d => y(d))
        .curve(d3.curveMonotoneX);

    svg.append("path")
        .datum(incomeData)
        .attr("fill", "none")
        .attr("stroke", "#4ade80")   // green for income
        .attr("stroke-width", 2)
        .attr("d", line);
}

renderIncomeSparkline();
