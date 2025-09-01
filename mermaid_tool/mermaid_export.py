# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mermaid_markdowns import ER_DIAGRAM, SEQUENCE_DIAGRAM, FLOW_CHART, ARCHITECTURE_DIAGRAM, CLASS_DIAGRAM, XY_BAR_DIAGRAM, PIE_CHART, KANBAN_BOARD, TURBONOMIC_ARCH_DIAGRAM, OR_TOOL, OR_AGENT
import subprocess
import tempfile
from pathlib import Path
import re
import os
from sample_usecase_mermaid_markdown import SAMPLE_ER_DIAGRAM, DB_SCHEMA, JOIN_DIAGRAM

print(os.path.exists("./mermaid_tool"))

def estimate_density(svg_content: str):
    """Estimate diagram density based on bounding box size."""
    match_w = re.search(r'width="([\d\.]+)', svg_content)
    match_h = re.search(r'height="([\d\.]+)', svg_content)
    if match_w and match_h:
        width = float(match_w.group(1))
        height = float(match_h.group(1))
        area = width * height
        return area
    return 0


def render_mermaid(mermaid_code: str, output_file: str):
    """
    Renders Mermaid diagram from a string to an image file (PNG or SVG).
    
    Requires:
        - Node.js
        - Mermaid CLI: npm install -g @mermaid-js/mermaid-cli
    """

    dpi  = 300
    max_density = 200000
    base_node_spacing = 60
    base_rank_spacing = 100
    spacing_multiplier = 1.0
    max_node_spacing = 120   # cap to avoid arrow geometry weirdness
    max_rank_spacing = 200

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    while True:

        node_spacing = min(int(base_node_spacing * spacing_multiplier), max_node_spacing)
        rank_spacing = min(int(base_rank_spacing * spacing_multiplier), max_rank_spacing)

        # Create init block with current spacing
        init_block = f"""%%{{ init: {{ 'flowchart': {{ 
            'defaultRenderer': 'elk', 
            'nodeSpacing': {node_spacing}, 
            'rankSpacing': {rank_spacing}, 
            'rankdir': 'LR'
        }} }} }}%%\n"""

        # Merge init with Mermaid code
        if not mermaid_code.strip().startswith("%%{"):
            full_code = init_block + mermaid_code
        else:
            full_code = mermaid_code  # assumes user already handled spacing

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mmd") as tmp_mmd:
            tmp_mmd.write(full_code.encode("utf-8"))
            tmp_mmd_path = tmp_mmd.name

        #print("tmp_mmd_path ", tmp_mmd_path)
        tmp_svg_path = tmp_mmd_path.replace(".mmd", ".svg")
        #print("tmp_svg_path ", tmp_svg_path)
        density = None
        try :
            mmdc_path = r"C:\Users\vmjad\AppData\Roaming\npm\mmdc.cmd"
            # Render to SVG using Mermaid CLI
            subprocess.run([
                mmdc_path, "-i", tmp_mmd_path, "-o", tmp_svg_path, "--theme", "default"
            ], check=True)
        except FileNotFoundError:
            # Handles case where mmdc is not installed or not in PATH
            print("Error: Mermaid CLI (mmdc) not found. Ensure it is installed and in your PATH.")
            print("To install, run: npm install -g @mermaid-js/mermaid-cli")
            print("If npm is blocked, see https://nodejs.org for installation instructions.")

        except subprocess.CalledProcessError as e:
            # Handles case where mmdc command fails (e.g., invalid input file or syntax error)
            print(f"Error: Mermaid CLI command failed with exit code {e.returncode}.")
            print(f"Command output: {e.output if e.output else 'No output'}")
            print("Check the input file for valid Mermaid syntax and ensure paths are correct.")

        except OSError as e:
            # Handles OS-related errors (e.g., permission issues or file access problems)
            print(f"OS error occurred: {e}")
            print(f"Ensure you have write permissions for {tmp_svg_path} and read permissions for {tmp_mmd_path}.")

        except Exception as e:
            # Catch any other unexpected errors
            print(f"################################################## {str(e)}")
            print(f"Unexpected error: {str(e)}")
            print("Please check your setup and try again, or provide more details for troubleshooting.")
            # Read SVG content for density check
            svg_content = Path(tmp_svg_path).read_text(encoding="utf-8")
            density = estimate_density(svg_content)


        if density is not None and density >= max_density or spacing_multiplier > 3:
            # Final PNG render with *current* spacing values
            final_code = init_block + mermaid_code if not mermaid_code.strip().startswith("%%{") else mermaid_code
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mmd") as final_mmd:
                final_mmd.write(final_code.encode("utf-8"))
                final_mmd_path = final_mmd.name

            scale_factor = dpi / 96  # 96 DPI is default browser export
            subprocess.run([
                "mmdc.cmd", "-i", final_mmd_path, "-o", output_file,
                "--theme", "default",
                "--scale", str(scale_factor)
            ], check=True)

            print(f"✅ Diagram saved to {output_file} at {dpi} ppi with spacing x{spacing_multiplier}")
            break
        else:
            spacing_multiplier += 0.2  # increase spacing and retry


# Example usage:

# mermaid_code = XY_BAR_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/xybarchart_diagram.png")

# mermaid_code = PIE_CHART
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/pie_diagram.png")

# mermaid_code = KANBAN_BOARD
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/kanban_diagram.png")

# mermaid_code = FLOW_CHART
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/flowchart_diagram.png")

# mermaid_code = ARCHITECTURE_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/architecture_diagram.png")

# mermaid_code = CLASS_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/class_diagram.png")

# mermaid_code = SEQUENCE_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/sequence_diagram.png")

# mermaid_code = ER_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/er_diagram.png")

# mermaid_code = TURBONOMIC_ARCH_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/turbo_arch_diagram.png")

# mermaid_code = SAMPLE_ER_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/sample_arch/sample_er_diagram.png")

# mermaid_code = DB_SCHEMA
# render_mermaid(mermaid_code, "./mermaid_tool/sample_arch/sample_db_schema_diagram.png")

# mermaid_code = JOIN_DIAGRAM
# render_mermaid(mermaid_code, "./mermaid_tool/sample_arch/sample_join_diagram.png")

# mermaid_code = OR_TOOL
# render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/or_tool_arch_diagram.png")

mermaid_code = OR_AGENT
render_mermaid(mermaid_code, "./mermaid_tool/arch_diagram/or_tool_Agent_arch_diagram.png")