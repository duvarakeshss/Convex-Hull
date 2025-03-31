import streamlit as st
import json
import matplotlib.pyplot as plt
from main import ConvexHull
import io
import base64

def get_download_link(fig, filename="convex_hull.png", text="Download Plot"):
    """
    Generates a download link for the plot
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'
    return href

def create_plot(points, hull):
    """
    Creates a matplotlib figure with the points and hull
    """
    # Clear any existing plots
    plt.clf()
    
    # Create new figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot points
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    ax.scatter(x, y, color='blue', label='Points')
    
    # Plot hull
    if len(hull) > 2:
        hull_x = [p[0] for p in hull] + [hull[0][0]]
        hull_y = [p[1] for p in hull] + [hull[0][1]]
        ax.plot(hull_x, hull_y, 'r-', linewidth=2, label='Convex Hull')
    
    # Add labels and grid
    ax.set_title("Convex Hull using Graham Scan")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def main():
    st.title("Convex Hull Visualization")
    st.write("""
    Upload a JSON file containing points to visualize their convex hull.
    You can download the visualization and results.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a JSON file", type=['json'])
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            data = json.load(uploaded_file)
            
            # Validate the data format
            if "points" not in data:
                st.error("Error: JSON file must contain a 'points' key")
                return
                
            points = data["points"]
            
            # Create ConvexHull object and compute hull
            convex_hull = ConvexHull(points)
            hull = convex_hull.compute_hull()
            
            # Display information
            st.write(f"Number of points: {len(points)}")
            st.write(f"Number of hull points: {len(hull)}")
            
            # Create and display plot
            fig = create_plot(points, hull)
            st.pyplot(fig)
            
            # Create columns for download buttons
            col1, col2, col3 = st.columns(3)
            
            # Download plot as PNG
            with col1:
                st.markdown(get_download_link(fig, text="Download Plot"), unsafe_allow_html=True)
            
            # Download hull points as JSON
            with col2:
                hull_json = json.dumps({"hull_points": hull}, indent=4)
                st.download_button(
                    label="Download Hull Points",
                    data=hull_json,
                    file_name="hull_points.json",
                    mime="application/json"
                )
            
            # Download all points as JSON
            with col3:
                points_json = json.dumps({"points": points}, indent=4)
                st.download_button(
                    label="Download All Points",
                    data=points_json,
                    file_name="all_points.json",
                    mime="application/json"
                )
            
            # Clean up the figure to free memory
            plt.close(fig)
            
        except json.JSONDecodeError:
            st.error("Error: Invalid JSON file format")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Add example data download
    st.markdown("---")
    st.write("Try it out with example data:")
    
    example_data = {
        "points": [
            [2, 2], [4, 3], [5, 1], [6, 4], [7, 5],
            [3, 6], [1, 7], [0, 5], [1, 3], [2, 4],
            [3, 3], [4, 5], [5, 3], [3, 2], [2, 1],
            [4, 1], [6, 2], [5, 5], [4, 7], [2, 6]
        ]
    }
    
    st.download_button(
        label="Download Example Data",
        data=json.dumps(example_data, indent=4),
        file_name="example_points.json",
        mime="application/json"
    )

if __name__ == "__main__":
    main()
