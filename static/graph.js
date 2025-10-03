/**
 * D3.js Graph Visualization for Entity Relationships
 * Handles the interactive graph display and manipulation
 */

// Global graph state
const GraphState = {
    data: null,
    simulation: null,
    svg: null,
    container: null,
    width: 0,
    height: 0,
    zoom: null,
    nodes: null,
    links: null,
    nodeElements: null,
    linkElements: null,
    labelElements: null
};

// Color scheme for different entity types
const entityTypeColors = {
    'PERSON': '#FF6B6B',      // Red
    'GPE': '#4ECDC4',         // Teal
    'ORG': '#45B7D1',         // Blue
    'FAC': '#96CEB4',         // Green
    'LOC': '#FFEAA7',         // Yellow
    'EVENT': '#DDA0DD',       // Plum
    'PRODUCT': '#98D8C8',     // Mint
    'WORK_OF_ART': '#F7DC6F', // Light Yellow
    'LAW': '#BB8FCE',         // Light Purple
    'LANGUAGE': '#85C1E9',    // Light Blue
    'MONEY': '#F8C471',       // Light Orange
    'CARDINAL': '#F1948A',    // Light Red
    'DATE': '#82E0AA',        // Light Green
    'TIME': '#D7BDE2',        // Light Purple
    'PERCENT': '#F9E79F',     // Light Yellow
    'ORDINAL': '#AED6F1',     // Light Blue
    'QUANTITY': '#A9DFBF',    // Light Green
    'NORP': '#FADBD8'         // Light Pink
};

/**
 * Initialize the graph visualization
 * @param {Array} relationships - Array of relationship objects
 */
function initializeGraph(relationships) {
    console.log('Initializing graph with relationships:', relationships);
    
    if (!relationships || relationships.length === 0) {
        console.log('No relationships to visualize');
        return;
    }
    
    // Process data into nodes and links
    const graphData = processGraphData(relationships);
    GraphState.data = graphData;
    
    // Setup SVG container
    setupSVG();
    
    // Create the graph
    createGraph(graphData);
    
    console.log('Graph initialization complete');
}

/**
 * Process relationship data into D3.js graph format
 * @param {Array} relationships - Array of relationship objects
 * @returns {Object} Graph data with nodes and links
 */
function processGraphData(relationships) {
    const nodesMap = new Map();
    const links = [];
    
    // Process relationships to extract nodes and links
    relationships.forEach(rel => {
        // Add subject node
        if (!nodesMap.has(rel.subject_qid)) {
            nodesMap.set(rel.subject_qid, {
                id: rel.subject_qid,
                label: rel.subject,
                type: 'entity',
                inDegree: rel.subject_in_degree || 0,
                outDegree: 0
            });
        }
        
        // Add object node
        if (!nodesMap.has(rel.object_qid)) {
            nodesMap.set(rel.object_qid, {
                id: rel.object_qid,
                label: rel.object,
                type: 'entity',
                inDegree: rel.object_in_degree || 0,
                outDegree: 0
            });
        }
        
        // Add link
        links.push({
            source: rel.subject_qid,
            target: rel.object_qid,
            predicate: rel.predicate,
            predicate_pid: rel.predicate_pid
        });
    });
    
    // Calculate out-degrees
    links.forEach(link => {
        const sourceNode = nodesMap.get(link.source);
        if (sourceNode) {
            sourceNode.outDegree++;
        }
    });
    
    const nodes = Array.from(nodesMap.values());
    
    console.log(`Processed ${nodes.length} nodes and ${links.length} links`);
    
    return { nodes, links };
}

/**
 * Setup SVG container and dimensions
 */
function setupSVG() {
    const container = document.getElementById('graphContainer');
    GraphState.container = container;
    
    // Get container dimensions
    const rect = container.getBoundingClientRect();
    GraphState.width = rect.width || 800;
    GraphState.height = rect.height || 600;
    
    // Clear existing SVG
    d3.select('#graphSvg').remove();
    
    // Create new SVG
    GraphState.svg = d3.select('#graphContainer')
        .append('svg')
        .attr('id', 'graphSvg')
        .attr('width', GraphState.width)
        .attr('height', GraphState.height);
    
    // Setup zoom behavior
    GraphState.zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', handleZoom);
    
    GraphState.svg.call(GraphState.zoom);
    
    console.log(`SVG setup complete: ${GraphState.width}x${GraphState.height}`);
}

/**
 * Create the graph visualization
 * @param {Object} data - Graph data with nodes and links
 */
function createGraph(data) {
    const { nodes, links } = data;
    
    // Create force simulation
    GraphState.simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(GraphState.width / 2, GraphState.height / 2))
        .force('collision', d3.forceCollide().radius(30));
    
    // Create link elements
    GraphState.linkElements = GraphState.svg.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(links)
        .enter().append('line')
        .attr('stroke', '#999')
        .attr('stroke-opacity', 0.6)
        .attr('stroke-width', 2)
        .attr('marker-end', 'url(#arrowhead)');
    
    // Create node elements
    GraphState.nodeElements = GraphState.svg.append('g')
        .attr('class', 'nodes')
        .selectAll('circle')
        .data(nodes)
        .enter().append('circle')
        .attr('r', d => calculateNodeSize(d))
        .attr('fill', d => getNodeColor(d))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));
    
    // Create label elements
    GraphState.labelElements = GraphState.svg.append('g')
        .attr('class', 'labels')
        .selectAll('text')
        .data(nodes)
        .enter().append('text')
        .text(d => d.label)
        .attr('font-size', '12px')
        .attr('font-family', 'Arial, sans-serif')
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('fill', '#333');
    
    // Add arrow markers for directed edges
    GraphState.svg.append('defs').append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 15)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', '#999');
    
    // Update positions on simulation tick
    GraphState.simulation.on('tick', updatePositions);
    
    // Add hover effects
    addHoverEffects();
    
    console.log('Graph creation complete');
}

/**
 * Calculate node size based on in-degree
 * @param {Object} node - Node data
 * @returns {number} Node radius
 */
function calculateNodeSize(node) {
    const baseSize = 15;
    const maxSize = 60;
    const inDegree = node.inDegree || 0;
    
    if (inDegree === 0) return baseSize;
    
    // Find max in-degree in the dataset
    const maxInDegree = Math.max(...GraphState.data.nodes.map(n => n.inDegree || 0));
    
    if (maxInDegree === 0) return baseSize;
    
    // Scale based on in-degree (as specified: 4x difference between min and max)
    const scale = 1 + (inDegree / maxInDegree) * 3; // 1x to 4x
    return Math.max(baseSize, Math.min(maxSize, baseSize * scale));
}

/**
 * Get node color based on entity type
 * @param {Object} node - Node data
 * @returns {string} Color code
 */
function getNodeColor(node) {
    // For now, use a default color scheme
    // In the future, we can add entity type detection
    return entityTypeColors['PERSON'] || '#667eea';
}

/**
 * Update node and link positions
 */
function updatePositions() {
    GraphState.linkElements
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
    
    GraphState.nodeElements
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
    
    GraphState.labelElements
        .attr('x', d => d.x)
        .attr('y', d => d.y);
}

/**
 * Handle zoom events
 * @param {Object} event - Zoom event
 */
function handleZoom(event) {
    GraphState.svg.selectAll('g').attr('transform', event.transform);
}

/**
 * Add hover effects to nodes
 */
function addHoverEffects() {
    GraphState.nodeElements
        .on('mouseover', function(event, d) {
            // Highlight connected nodes
            highlightConnectedNodes(d);
            
            // Show tooltip
            showTooltip(event, d);
        })
        .on('mouseout', function(event, d) {
            // Remove highlighting
            removeHighlighting();
            
            // Hide tooltip
            hideTooltip();
        });
}

/**
 * Highlight nodes connected to the hovered node
 * @param {Object} hoveredNode - The node being hovered
 */
function highlightConnectedNodes(hoveredNode) {
    const connectedNodeIds = new Set();
    
    // Find connected nodes
    GraphState.data.links.forEach(link => {
        if (link.source.id === hoveredNode.id || link.target.id === hoveredNode.id) {
            connectedNodeIds.add(link.source.id);
            connectedNodeIds.add(link.target.id);
        }
    });
    
    // Update node opacity
    GraphState.nodeElements
        .style('opacity', d => connectedNodeIds.has(d.id) ? 1 : 0.3);
    
    // Update link opacity
    GraphState.linkElements
        .style('opacity', d => 
            connectedNodeIds.has(d.source.id) && connectedNodeIds.has(d.target.id) ? 1 : 0.1);
}

/**
 * Remove highlighting from all nodes and links
 */
function removeHighlighting() {
    GraphState.nodeElements.style('opacity', 1);
    GraphState.linkElements.style('opacity', 0.6);
}

/**
 * Show tooltip for node
 * @param {Object} event - Mouse event
 * @param {Object} node - Node data
 */
function showTooltip(event, node) {
    // This will be implemented in a future step
    console.log('Tooltip for:', node.label);
}

/**
 * Hide tooltip
 */
function hideTooltip() {
    // This will be implemented in a future step
}

/**
 * Drag event handlers
 */
function dragstarted(event, d) {
    if (!event.active) GraphState.simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragended(event, d) {
    if (!event.active) GraphState.simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

/**
 * Reset graph view to initial state
 */
function resetGraphView() {
    if (GraphState.zoom) {
        GraphState.svg.transition().duration(750).call(
            GraphState.zoom.transform,
            d3.zoomIdentity
        );
    }
}

/**
 * Clear the graph
 */
function clearGraph() {
    if (GraphState.svg) {
        GraphState.svg.selectAll('*').remove();
    }
    GraphState.data = null;
    GraphState.simulation = null;
}

// Make functions available globally
window.initializeGraph = initializeGraph;
window.clearGraph = clearGraph;
window.resetGraphView = resetGraphView;
