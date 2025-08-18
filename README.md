# Architect Agent

A Python toolkit for rendering and exporting architecture diagrams using [Mermaid](https://mermaid-js.github.io/mermaid/#/) and the Mermaid CLI.  
Supports exporting diagrams as SVG and high-resolution PNG files.

## Features

- Render Mermaid diagrams from Python strings
- Export diagrams as SVG and PNG (300ppi)
- Automatic layout adjustment for readability
- Supports flowcharts, sequence diagrams, ER diagrams, and architecture diagrams

## Requirements

- Python 3.8+
- Node.js
- Mermaid CLI (`npm install -g @mermaid-js/mermaid-cli`)
- See `requirements.txt` for Python dependencies

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kiranfegade19/architecture_agent.git
   cd architect_agent
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Mermaid CLI:**
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

## Usage

Example to render and export a diagram:

```python
from mermaid_tool.mermaid_export import render_mermaid
from mermaid_tool.mermaid_markdowns import FLOW_CHART

render_mermaid(FLOW_CHART, "output/diagram.png")
```

## Mermaid Diagram Types Supported

- `SEQUENCE_DIAGRAM`
- `ER_DIAGRAM`
- `FLOW_CHART`
- `ARCHITECTURE_DIAGRAM`
- `CLASS_DIAGRAM`
- `XY_BAR_DIAGRAM`
- `PIE_CHART`
- `KANBAN_BOARD`

All diagram templates are available in `mermaid_tool/mermaid_markdowns.py`.

## Troubleshooting

- If you see `import cairosvg could not be resolved`, ensure your Python interpreter matches the environment where you installed dependencies.
- For best results, use VS Code and select the correct Python interpreter.
