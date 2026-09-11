import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const StringDiagram = ({ schedule, windows, onBlockDrag }) => {
  const svgRef = useRef();

  useEffect(() => {
    if (!svgRef.current || !schedule) return;

    // Clear previous SVG content
    d3.select(svgRef.current).selectAll('*').remove();

    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const width = svgRef.current.clientWidth - margin.left - margin.right;
    const height = svgRef.current.clientHeight - margin.top - margin.bottom;

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // 1. Setup Scales
    // X-axis: Time (0-24h)
    const xScale = d3.scaleLinear()
      .domain([0, 24])
      .range([0, width]);

    // Y-axis: Chainage (Km) - Dynamic domain
    const allChainages = schedule.flatMap(b => [b.chainage_start_km, b.chainage_end_km]);
    const yMin = allChainages.length ? d3.min(allChainages) - 1 : 1000;
    const yMax = allChainages.length ? d3.max(allChainages) + 1 : 1100;

    const yScale = d3.scaleLinear()
      .domain([yMax, yMin]) // Inverted Y-axis: Higher km at top or bottom? Usually bottom is 0.
      .range([0, height]);

    // 2. Draw Axes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale).tickFormat(d => `${d}:00`))
      .attr('color', '#64748b');

    svg.append('g')
      .call(d3.axisLeft(yScale))
      .attr('color', '#64748b');

    // 3. Render Maintenance Blocks
    const deptColors = {
      'Engineering': '#ef4444', // Red
      'TRD': '#3b82f6',          // Blue
      'S&T': '#22c55e',          // Green
    };

    svg.selectAll('.block')
      .data(schedule)
      .enter()
      .append('rect')
      .attr('class', 'block cursor-pointer hover:opacity-80 transition-opacity')
      .attr('x', d => {
        // Simple parsing of "HH:mm" to float hours
        const [h, m] = d.scheduled_start.split(':').map(Number);
        return xScale(h + m/60);
      })
      .attr('y', d => yScale(d.chainage_end_km))
      .attr('width', d => {
        // Mock duration for now if not provided
        const durationHours = 4; // Default 4h window
        return xScale(durationHours);
      })
      .attr('height', d => yScale(d.chainage_start_km) - yScale(d.chainage_end_km))
      .attr('fill', d => deptColors[d.dept] || '#94a3b8')
      .attr('rx', 4)
      .on('click', (event, d) => {
        // In a real app, this would trigger a detail view
        console.log('Block clicked:', d);
      });

    // 4. Render Grid Lines (Hour marks)
    svg.append('g')
      .attr('class', 'grid')
      .attr('stroke', '#1e293b')
      .attr('stroke-width', 1)
      .selectAll('line')
      .data(d3.range(0, 25))
      .enter()
      .append('line')
      .attr('x1', d => xScale(d))
      .attr('x2', d => xScale(d))
      .attr('y1', 0)
      .attr('y2', height);

  }, [schedule, windows]);

  return (
    <div className="relative w-full h-full bg-slate-950 overflow-hidden rounded-xl border border-slate-800">
      <svg ref={svgRef} className="w-full h-full" />
      <div className="absolute top-4 right-4 flex gap-4 text-xs text-slate-400">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-red-500 rounded-sm"></div> Engineering
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-blue-500 rounded-sm"></div> TRD
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-green-500 rounded-sm"></div> S&T
        </div>
      </div>
    </div>
  );
};

export default StringDiagram;
