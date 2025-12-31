// Sample expense data (you can replace this later)
const expenseData = [5, 7, 6, 9, 4, 3, 8];

function renderExpenseSparkline() {
    const width = 100;
    const height = 40;

    const svg = d3.select("#expense-sparkline")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const x = d3.scaleLinear()
        .domain([0, expenseData.length - 1])
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([d3.min(expenseData), d3.max(expenseData)])
        .range([height, 0]);

    const line = d3.line()
        .x((d, i) => x(i))
        .y(d => y(d))
        .curve(d3.curveMonotoneX);

    svg.append("path")
        .datum(expenseData)
        .attr("fill", "none")
        .attr("stroke", "#f87171")   // red for expenses
        .attr("stroke-width", 2)
        .attr("d", line);
}

renderExpenseSparkline();
