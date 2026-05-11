import json
import random
import base64

def get_logo_base64():
    """Get the logo as base64 string"""
    try:
        with open('/mnt/user-data/uploads/1769719724566_image.png', 'rb') as img_file:
            img_data = img_file.read()
            return base64.b64encode(img_data).decode('utf-8')
    except:
        # If file not found, return empty string
        return ""

def generate_movie_data():
    """Generate comprehensive movie data with clusters, relationships, and viewer counts"""
    
    # Define 20+ movie clusters with multiple movies each
    clusters = {
        "Action": ["Die Hard", "Mad Max: Fury Road", "The Matrix"],
        "Sci-Fi": ["Blade Runner 2049", "Interstellar", "Arrival", "Ex Machina"],
        "Drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather"],
        "Comedy": ["The Grand Budapest Hotel", "Superbad", "Groundhog Day"],
        "Horror": ["The Conjuring", "A Quiet Place", "Get Out", "Hereditary"],
        "Thriller": ["Gone Girl", "Se7en", "The Silence of the Lambs"],
        "Romance": ["The Notebook", "La La Land", "Before Sunrise"],
        "Fantasy": ["The Lord of the Rings", "Pan's Labyrinth", "Spirited Away"],
        "Animation": ["Spider-Man: Into the Spider-Verse", "WALL-E", "Toy Story"],
        "Crime": ["Pulp Fiction", "The Departed", "Heat"],
        "Mystery": ["Knives Out", "Prisoners", "Zodiac"],
        "Adventure": ["Indiana Jones", "Jurassic Park", "The Revenant"],
        "War": ["1917", "Dunkirk", "Saving Private Ryan"],
        "Western": ["No Country for Old Men", "True Grit", "Django Unchained"],
        "Musical": ["Whiplash", "The Greatest Showman", "A Star is Born"],
        "Documentary": ["Free Solo", "Planet Earth", "The Social Dilemma"],
        "Biography": ["The Social Network", "Bohemian Rhapsody", "The Theory of Everything"],
        "Sports": ["Moneyball", "Rocky", "Remember the Titans"],
        "Historical": ["Schindler's List", "12 Years a Slave", "The King's Speech"],
        "Superhero": ["The Dark Knight", "Avengers: Endgame", "Logan", "Black Panther"]
    }
    
    directors = ["Christopher Nolan", "Quentin Tarantino", "Martin Scorsese", "Steven Spielberg",
                 "Denis Villeneuve", "Ridley Scott", "James Cameron", "Greta Gerwig",
                 "Wes Anderson", "David Fincher", "Jordan Peele", "Ari Aster"]
    
    # Create nodes
    nodes = []
    node_id = 0
    cluster_map = {}
    
    for cluster_name, movies in clusters.items():
        cluster_map[cluster_name] = []
        for movie in movies:
            # Generate viewer count (in millions)
            viewers = random.randint(500000, 50000000)
            
            nodes.append({
                "id": node_id,
                "name": movie,
                "cluster": cluster_name,
                "year": random.randint(1990, 2024),
                "rating": round(random.uniform(6.5, 9.5), 1),
                "director": random.choice(directors),
                "viewers": viewers,
                "description": f"A compelling {cluster_name.lower()} film that explores themes of humanity, courage, and redemption."
            })
            cluster_map[cluster_name].append(node_id)
            node_id += 1
    
    # Create "watched after" links with viewer-based strength
    links = []
    
    # Same cluster connections
    for cluster_name, node_ids in cluster_map.items():
        for i in range(len(node_ids) - 1):
            if random.random() > 0.3:
                # Connection strength based on combined viewers
                source_viewers = nodes[node_ids[i]]['viewers']
                target_viewers = nodes[node_ids[i + 1]]['viewers']
                connection_strength = (source_viewers + target_viewers) / 2
                
                links.append({
                    "source": node_ids[i],
                    "target": node_ids[i + 1],
                    "type": "same_cluster",
                    "strength": connection_strength
                })
    
    # Cross-cluster connections
    cluster_names = list(cluster_map.keys())
    for _ in range(30):
        cluster1, cluster2 = random.sample(cluster_names, 2)
        node1 = random.choice(cluster_map[cluster1])
        node2 = random.choice(cluster_map[cluster2])
        
        # Connection strength based on combined viewers
        source_viewers = nodes[node1]['viewers']
        target_viewers = nodes[node2]['viewers']
        connection_strength = (source_viewers + target_viewers) / 2
        
        links.append({
            "source": node1,
            "target": node2,
            "type": "cross_cluster",
            "strength": connection_strength
        })
    
    return {"nodes": nodes, "links": links}

def create_html_file(output_filename="movie_network.html"):
    """Generate a complete HTML file with D3.js visualization"""
    
    print("Generating movie data...")
    data = generate_movie_data()
    
    print("Loading custom logo...")
    logo_base64 = get_logo_base64()
    
    # Convert data to JSON string
    data_json = json.dumps(data, indent=2)
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOD Movie Network Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #000000;
            overflow: hidden;
            color: #fff;
        }}
        
        #logo {{
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 1000;
        }}
        
        #logo img {{
            height: 60px;
            width: auto;
            filter: drop-shadow(0 0 15px rgba(255, 193, 7, 0.6));
        }}
        
        svg {{
            width: 100vw;
            height: 100vh;
            cursor: grab;
        }}
        
        svg:active {{
            cursor: grabbing;
        }}
        
        .node {{
            cursor: pointer;
            stroke: #fff;
            stroke-width: 2px;
            transition: all 0.3s ease;
        }}
        
        .node:hover {{
            stroke-width: 3px;
        }}
        
        .node.selected {{
            stroke: #ffc107;
            stroke-width: 4px;
            filter: drop-shadow(0 0 20px rgba(255, 193, 7, 1)) drop-shadow(0 0 40px rgba(255, 193, 7, 0.8));
        }}
        
        .node.dimmed {{
            opacity: 0.1;
        }}
        
        .node.connected {{
            opacity: 1;
        }}
        
        .link {{
            stroke-opacity: 0.4;
            transition: all 0.3s ease;
        }}
        
        .link.same_cluster {{
            stroke: #00d4ff;
        }}
        
        .link.cross_cluster {{
            stroke: #ff6b9d;
        }}
        
        .link.dimmed {{
            opacity: 0;
        }}
        
        .link.highlighted {{
            stroke-opacity: 0.8;
            stroke: #ffc107;
        }}
        
        .node-label {{
            font-size: 11px;
            font-weight: 600;
            fill: #ffffff;
            text-anchor: middle;
            pointer-events: none;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            transition: opacity 0.3s ease;
        }}
        
        .node-label.dimmed {{
            opacity: 0.1;
        }}
        
        #tooltip {{
            position: absolute;
            background: rgba(20, 20, 20, 0.98);
            border: 3px solid #ffc107;
            border-radius: 15px;
            padding: 25px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            max-width: 400px;
            box-shadow: 0 0 30px rgba(255, 193, 7, 0.6), 0 0 60px rgba(255, 193, 7, 0.3);
            z-index: 2000;
        }}
        
        #tooltip.visible {{
            opacity: 1;
        }}
        
        #tooltip h3 {{
            color: #ffc107;
            margin-bottom: 15px;
            font-size: 22px;
            font-weight: 700;
            border-bottom: 2px solid #ffc107;
            padding-bottom: 10px;
            text-shadow: 0 0 10px rgba(255, 193, 7, 0.5);
        }}
        
        #tooltip .info-row {{
            margin: 10px 0;
            font-size: 14px;
            line-height: 1.6;
        }}
        
        #tooltip .label {{
            color: #aaa;
            font-weight: 700;
            display: inline-block;
            width: 90px;
        }}
        
        #tooltip .value {{
            color: #fff;
            font-weight: 500;
        }}
        
        #tooltip .description {{
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #444;
            color: #ccc;
            font-size: 14px;
            line-height: 1.8;
            font-style: italic;
        }}
        
        #legend {{
            position: absolute;
            bottom: 30px;
            right: 30px;
            background: rgba(20, 20, 20, 0.85);
            padding: 25px;
            border-radius: 15px;
            border: 2px solid rgba(255, 193, 7, 0.3);
            z-index: 1000;
            max-height: 450px;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(255, 193, 7, 0.2);
        }}
        
        #legend h4 {{
            color: #ffc107;
            margin-bottom: 20px;
            font-size: 18px;
            font-weight: 700;
            text-align: center;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 10px 0;
            font-size: 13px;
            font-weight: 500;
        }}
        
        .legend-color {{
            width: 18px;
            height: 18px;
            border-radius: 50%;
            margin-right: 12px;
            border: 2.5px solid #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }}
        
        .controls {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(20, 20, 20, 0.85);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(255, 193, 7, 0.3);
            z-index: 1000;
            box-shadow: 0 0 20px rgba(255, 193, 7, 0.2);
        }}
        
        .controls button {{
            background: rgba(255, 193, 7, 0.15);
            color: #ffc107;
            border: 2px solid rgba(255, 193, 7, 0.4);
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            font-size: 14px;
            transition: all 0.3s ease;
            margin: 5px;
            box-shadow: 0 0 15px rgba(255, 193, 7, 0.1);
        }}
        
        .controls button:hover {{
            background: rgba(255, 193, 7, 0.25);
            border-color: rgba(255, 193, 7, 0.6);
            box-shadow: 0 0 25px rgba(255, 193, 7, 0.4);
            transform: translateY(-2px);
        }}
        
        .controls button:active {{
            transform: translateY(0);
        }}
        
        /* Custom scrollbar for legend */
        #legend::-webkit-scrollbar {{
            width: 8px;
        }}
        
        #legend::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }}
        
        #legend::-webkit-scrollbar-thumb {{
            background: #ffc107;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div id="logo">
        <img src="data:image/png;base64,{logo_base64}" alt="TOD Logo">
    </div>
    
    <div class="controls">
        <button onclick="resetView()">🔄 Reset View</button>
        <button onclick="saveHTML()">💾 Save HTML</button>
    </div>
    
    <svg id="graph"></svg>
    
    <div id="tooltip"></div>
    
    <div id="legend">
        <h4>📊 Movie Clusters</h4>
        <div id="legend-content"></div>
    </div>
    
    <script>
        // Movie data
        const graphData = {data_json};
        
        // Setup
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        const svg = d3.select("#graph")
            .attr("width", width)
            .attr("height", height);
        
        // Color scale
        const clusters = [...new Set(graphData.nodes.map(d => d.cluster))];
        const colorScale = d3.scaleOrdinal()
            .domain(clusters)
            .range([
                "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
                "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B88B", "#AAB7B8",
                "#52B788", "#F4A261", "#E76F51", "#2A9D8F", "#E9C46A",
                "#F4978E", "#8D99AE", "#EF476F", "#FFD166", "#06FFA5"
            ]);
        
        // Calculate radius based on viewers (scale from 8 to 25)
        const minViewers = d3.min(graphData.nodes, d => d.viewers);
        const maxViewers = d3.max(graphData.nodes, d => d.viewers);
        const radiusScale = d3.scaleSqrt()
            .domain([minViewers, maxViewers])
            .range([8, 25]);
        
        // Calculate link width based on connection strength
        const minStrength = d3.min(graphData.links, d => d.strength);
        const maxStrength = d3.max(graphData.links, d => d.strength);
        const linkWidthScale = d3.scaleLinear()
            .domain([minStrength, maxStrength])
            .range([1, 5]);
        
        // Build legend
        const legendContent = d3.select("#legend-content");
        clusters.forEach(cluster => {{
            const item = legendContent.append("div")
                .attr("class", "legend-item");
            item.append("div")
                .attr("class", "legend-color")
                .style("background-color", colorScale(cluster));
            item.append("span")
                .text(cluster);
        }});
        
        // Force simulation
        const simulation = d3.forceSimulation(graphData.nodes)
            .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(120))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => radiusScale(d.viewers) + 5));
        
        // Container for zoom
        const g = svg.append("g");
        
        // Zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.1, 5])
            .on("zoom", (event) => {{
                g.attr("transform", event.transform);
            }});
        
        svg.call(zoom);
        
        // Links
        const link = g.append("g")
            .selectAll("line")
            .data(graphData.links)
            .enter()
            .append("line")
            .attr("class", d => "link " + d.type)
            .attr("stroke-width", d => linkWidthScale(d.strength));
        
        // Track selected node
        let selectedNode = null;
        
        // Nodes
        const node = g.append("g")
            .selectAll("circle")
            .data(graphData.nodes)
            .enter()
            .append("circle")
            .attr("class", "node")
            .attr("r", d => radiusScale(d.viewers))
            .attr("fill", d => colorScale(d.cluster))
            .on("click", (event, d) => {{
                event.stopPropagation();
                
                // If clicking the same node, deselect
                if (selectedNode && selectedNode.id === d.id) {{
                    resetHighlight();
                    return;
                }}
                
                // Select new node and highlight connections
                selectedNode = d;
                highlightConnections(d);
                showTooltip(event, d);
            }})
            .on("mouseout", () => {{
                // Only hide tooltip if no node is selected
                if (!selectedNode) {{
                    hideTooltip();
                }}
            }})
            .call(d3.drag()
                .on("start", dragStarted)
                .on("drag", dragged)
                .on("end", dragEnded));
        
        // Labels
        const labels = g.append("g")
            .selectAll("text")
            .data(graphData.nodes)
            .enter()
            .append("text")
            .attr("class", "node-label")
            .text(d => d.name.length > 25 ? d.name.substring(0, 25) + "..." : d.name)
            .attr("dy", d => radiusScale(d.viewers) + 16);
        
        // Function to highlight connections
        function highlightConnections(selectedNode) {{
            // Get connected node IDs
            const connectedNodeIds = new Set();
            connectedNodeIds.add(selectedNode.id);
            
            // Find all connected links and nodes
            const connectedLinks = [];
            graphData.links.forEach(link => {{
                const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
                const targetId = typeof link.target === 'object' ? link.target.id : link.target;
                
                if (sourceId === selectedNode.id) {{
                    connectedNodeIds.add(targetId);
                    connectedLinks.push(link);
                }} else if (targetId === selectedNode.id) {{
                    connectedNodeIds.add(sourceId);
                    connectedLinks.push(link);
                }}
            }});
            
            // Update nodes
            node.classed("selected", d => d.id === selectedNode.id)
                .classed("connected", d => connectedNodeIds.has(d.id))
                .classed("dimmed", d => !connectedNodeIds.has(d.id));
            
            // Update links
            link.classed("highlighted", l => {{
                    const sourceId = typeof l.source === 'object' ? l.source.id : l.source;
                    const targetId = typeof l.target === 'object' ? l.target.id : l.target;
                    return sourceId === selectedNode.id || targetId === selectedNode.id;
                }})
                .classed("dimmed", l => {{
                    const sourceId = typeof l.source === 'object' ? l.source.id : l.source;
                    const targetId = typeof l.target === 'object' ? l.target.id : l.target;
                    return sourceId !== selectedNode.id && targetId !== selectedNode.id;
                }});
            
            // Update labels
            labels.classed("dimmed", d => !connectedNodeIds.has(d.id));
        }}
        
        // Function to reset highlight
        function resetHighlight() {{
            selectedNode = null;
            node.classed("selected", false)
                .classed("connected", false)
                .classed("dimmed", false);
            link.classed("highlighted", false)
                .classed("dimmed", false);
            labels.classed("dimmed", false);
            hideTooltip();
        }}
        
        // Tooltip functions
        const tooltip = d3.select("#tooltip");
        
        function formatNumber(num) {{
            if (num >= 1000000) {{
                return (num / 1000000).toFixed(1) + 'M';
            }} else if (num >= 1000) {{
                return (num / 1000).toFixed(1) + 'K';
            }}
            return num.toString();
        }}
        
        function showTooltip(event, d) {{
            tooltip.html(`
                <h3>${{d.name}}</h3>
                <div class="info-row">
                    <span class="label">Cluster:</span>
                    <span class="value">${{d.cluster}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Year:</span>
                    <span class="value">${{d.year}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Rating:</span>
                    <span class="value">⭐ ${{d.rating}}/10</span>
                </div>
                <div class="info-row">
                    <span class="label">Director:</span>
                    <span class="value">${{d.director}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Viewers:</span>
                    <span class="value">👥 ${{formatNumber(d.viewers)}}</span>
                </div>
                <div class="description">${{d.description}}</div>
            `)
            .style("left", (event.pageX + 20) + "px")
            .style("top", (event.pageY + 20) + "px")
            .classed("visible", true);
        }}
        
        function hideTooltip() {{
            tooltip.classed("visible", false);
        }}
        
        // Click outside to deselect
        svg.on("click", function(event) {{
            if (event.target === this) {{
                resetHighlight();
            }}
        }});
        
        // Simulation tick
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
            
            labels
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        }});
        
        // Drag functions
        function dragStarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragEnded(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        // Control functions
        function resetView() {{
            svg.transition()
                .duration(750)
                .call(zoom.transform, d3.zoomIdentity);
            simulation.alpha(1).restart();
            resetHighlight();
        }}
        
        function saveHTML() {{
            const blob = new Blob([document.documentElement.outerHTML], {{ type: 'text/html' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'tod_movie_network_' + Date.now() + '.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            alert('HTML file saved successfully!');
        }}
    </script>
</body>
</html>"""
    
    print(f"Writing HTML file to: {output_filename}")
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"\n✅ SUCCESS! HTML file created: {output_filename}")
    print(f"🎨 Enhanced Features:")
    print(f"   - Node sizes based on viewer count")
    print(f"   - Connection thickness based on combined viewers")
    print(f"   - Click node to highlight ONLY connected nodes")
    print(f"   - Unconnected nodes disappear when filtering")
    print(f"   - Golden glow on selected node")
    print(f"   - Glowing buttons matching logo style")
    print(f"📊 Total nodes: {len(data['nodes'])}")
    print(f"🔗 Total links: {len(data['links'])}")
    print(f"🎬 Total clusters: {len(set(node['cluster'] for node in data['nodes']))}")
    print(f"\n💡 Click any movie to see only its connections!")

if __name__ == "__main__":
    try:
        create_html_file("movie_network.html")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
