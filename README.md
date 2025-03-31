# Convex Hull Implementation with Graham Scan

This project implements the Graham Scan algorithm to find the convex hull of a set of 2D points, with both a core implementation and an interactive web interface.

## What is a Convex Hull?
A convex hull is the smallest convex polygon that contains all points in a given set. Think of it as stretching a rubber band around all the points - the shape it forms is the convex hull.

## Project Structure
```
Convex-HULL/
│
├── main.py                 # Core ConvexHull class implementation
├── app.py                  # Streamlit web interface
|├── data/                  #input data
||    └── data.json
|├── outputs/               #Output data
||    └── convex_hull.png
└── requirements.txt         # Project dependencies
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/duvarakeshss/Convex-Hull
cd convex-hull
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface
1. Start the Streamlit app:
```bash
streamlit run app.py
```
2. Open your web browser to the displayed URL (typically http://localhost:8501)
3. Upload a JSON file containing points or use the example data
4. View the visualization and download results

### Python API
```python
from main import ConvexHull

# Create a ConvexHull object with points
points = [[0, 0], [1, 1], [0, 2], [2, 1]]
ch = ConvexHull(points)

# Compute the hull
hull = ch.compute_hull()

# Visualize the result
ch.plot()
```

## Input Format
The JSON input file should have the following structure:
```json
{
    "points": [
        [x1, y1],
        [x2, y2],
        ...
    ]
}
```

## Algorithm Details

### Graham Scan Algorithm
The implementation uses the Graham Scan algorithm, which works in three steps:
1. Find the lowest point (anchor point)
2. Sort points by polar angle relative to anchor point
3. Build the hull by processing points in order

### Complexity
- Time Complexity: O(n log n)
- Space Complexity: O(n)
where n is the number of points

## Features
- Efficient Graham Scan implementation
- Interactive web interface using Streamlit
- JSON input/output support
- Visualization with matplotlib
- Error handling and input validation
- Example data provided

## Example Code

### Loading Points from File
```python
convex_hull = ConvexHull()
convex_hull.load_points_from_file("data.json")
hull = convex_hull.compute_hull()
convex_hull.plot()
```

### Direct Point Input
```python
points = [(0, 3), (1, 1), (2, 2), (4, 4), 
          (0, 0), (1, 2), (3, 1), (3, 3)]
convex_hull = ConvexHull(points)
hull = convex_hull.compute_hull()
convex_hull.plot(save_path="convex_hull.png")
```

## Methods Reference

### ConvexHull Class
- `__init__(points=None)`: Initialize with optional points
- `compute_hull()`: Calculate the convex hull
- `plot(save_path=None, show=True)`: Visualize the points and hull
- `load_points_from_file(file_path)`: Load points from JSON
- `save_points_to_file(file_path)`: Save points to JSON
- `add_points(new_points)`: Add points to existing set
- `set_points(points)`: Replace all points
