import json
import math
import matplotlib.pyplot as plt

class ConvexHull:
    """
    A class for computing the convex hull of a set of points using Graham's scan algorithm.
    
    The convex hull is the smallest convex polygon that contains all the points.
    """
    
    def __init__(self, points=None):
        """
        Initialize the ConvexHull object.
        
        Args:
            points: A list of points as (x, y) tuples/lists. If None, points must be loaded later.
        """
        self.points = points or []
        self.hull = []
    
    def compute_hull(self):
        """
        Computes the convex hull using Graham's scan algorithm.
        
        Returns:
            A list of points forming the convex hull in counterclockwise order.
        """
        if not self.points:
            raise ValueError("No points available. Add points first.")
            
        self.hull = self.graham_scan()
        return self.hull
    
    def orientation(self, p, q, r):
        """
        Determines the orientation of triplet (p, q, r).
        
        Args:
            p, q, r: Points as (x, y) tuples
            
        Returns:
            0: If points are collinear
            1: If orientation is clockwise
            2: If orientation is counterclockwise
        
        This is a key function for the Graham scan algorithm. It uses the cross product
        to determine which way three points turn.
        """
        # Calculate the cross product (q - p) × (r - q)
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or Counterclockwise
    
    def distance(self, p1, p2):
        """
        Calculates the Euclidean distance between two points.
        
        Args:
            p1, p2: Points as (x, y) tuples
            
        Returns:
            The Euclidean distance between the points
        """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def graham_scan(self):
        """
        Implements Graham's scan algorithm to find the convex hull of a set of points.
        
        The algorithm works in three main steps:
        1. Find the lowest point (anchor point)
        2. Sort the remaining points by polar angle with respect to the anchor
        3. Scan through the sorted points, maintaining a convex hull
        
        Returns:
            List of points forming the convex hull in counterclockwise order
        
        Time Complexity: O(n log n) where n is the number of points
        Space Complexity: O(n)
        """
        points = self.points
        
        # Handle edge cases
        if len(points) < 3:
            return points.copy()  # No convex hull possible with less than 3 points
        
        # Step 1: Find the point with the lowest y-coordinate (and leftmost if tied)
        # This point is guaranteed to be on the convex hull
        lowest = min(points, key=lambda p: (p[1], p[0]))
        
        # Step 2: Sort the points based on polar angle with respect to the lowest point
        def polar_angle(p):
            if p == lowest:
                return -math.inf  # Place lowest point at the beginning
            return math.atan2(p[1] - lowest[1], p[0] - lowest[0])
        
        sorted_points = sorted(points, key=polar_angle)
        
        # Handle collinear points by removing all but the farthest one
        # This ensures that the hull doesn't zigzag through collinear points
        i = 1
        while i < len(sorted_points) - 1:
            # Check if points i and i+1 make the same angle with the lowest point
            o = self.orientation(lowest, sorted_points[i], sorted_points[i+1])
            if o == 0:  # Collinear
                # Keep the farthest point and remove the closer one
                if self.distance(lowest, sorted_points[i]) < self.distance(lowest, sorted_points[i+1]):
                    sorted_points.pop(i)
                else:
                    sorted_points.pop(i+1)
            else:
                i += 1
        
        # Handle edge case: after removing collinear points, we might have fewer than 3 points
        if len(sorted_points) < 3:
            return sorted_points
        
        # Step 3: Graham scan - Initialize the hull with the first two points
        hull = [sorted_points[0], sorted_points[1]]
        
        # Process remaining points
        for i in range(2, len(sorted_points)):
            # For each new point, pop points from hull that would make a non-left turn
            # This ensures the hull remains convex
            while len(hull) > 1 and self.orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
                hull.pop()
            # Add the new point to the hull
            hull.append(sorted_points[i])
        
        return hull
    
    def add_points(self, new_points):
        """
        Add points to the existing set.
        
        Args:
            new_points: List of points as (x, y) tuples/lists
        """
        self.points.extend(new_points)
        # Reset hull since points have changed
        self.hull = []
    
    def set_points(self, points):
        """
        Set a new list of points, replacing any existing points.
        
        Args:
            points: List of points as (x, y) tuples/lists
        """
        self.points = points
        # Reset hull since points have changed
        self.hull = []
    
    def load_points_from_file(self, file_path):
        """
        Loads points from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Number of points loaded
            
        Expected JSON format:
        {
            "points": [[x1, y1], [x2, y2], ...]
        }
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.points = data["points"]
            # Reset hull since points have changed
            self.hull = []
            return len(self.points)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading points from {file_path}: {str(e)}")
    
    def save_points_to_file(self, file_path):
        """
        Saves points to a JSON file.
        
        Args:
            file_path: Path to the JSON file
        """
        with open(file_path, 'w') as f:
            json.dump({"points": self.points}, f, indent=4)
    
    def plot(self, save_path=None, show=True):
        """
        Plots the points and the convex hull.
        
        Args:
            save_path: Path to save the plot image. If None, no image is saved.
            show: Whether to display the plot.
        """
        if not self.hull:
            self.compute_hull()
            
        # Extract x and y coordinates for plotting
        x = [p[0] for p in self.points]
        y = [p[1] for p in self.points]
        
        # Create figure
        plt.figure(figsize=(10, 10))
        
        # Plot all points
        plt.scatter(x, y, color='blue')
        
        # Plot the convex hull as a closed polygon
        if len(self.hull) > 2:  # Only plot hull if it forms a polygon
            # Add the first point at the end to close the polygon
            hull_x = [p[0] for p in self.hull] + [self.hull[0][0]]
            hull_y = [p[1] for p in self.hull] + [self.hull[0][1]]
            plt.plot(hull_x, hull_y, 'r-', linewidth=2)
        
        # Add labels and grid
        plt.title("Convex Hull using Graham Scan")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        
        # Save the plot if a path is provided
        if save_path:
            plt.savefig(save_path)
        
        # Show the plot if requested
        if show:
            plt.show()
        else:
            plt.close()


def load_default_points():
    """Helper function to create default points if needed"""
    return [(0, 3), (1, 1), (2, 2), (4, 4), 
            (0, 0), (1, 2), (3, 1), (3, 3)]


if __name__ == "__main__":
    # Create a new ConvexHull object
    convex_hull = ConvexHull()
    
    # Try to load points from data.json or use default points if the file doesn't exist
    try:
        # Try to load points from data.json
        num_points = convex_hull.load_points_from_file("data/data.json")
        print(f"Loaded {num_points} points from data.json")
    except ValueError as e:
        print(f"{e}, using default points")
        # Set default points
        default_points = load_default_points()
        convex_hull.set_points(default_points)
        convex_hull.save_points_to_file("data/data.json")
        print(f"Saved {len(default_points)} default points to data.json")
    
    # Calculate the convex hull using Graham scan
    hull = convex_hull.compute_hull()
    print("Convex Hull Points:", hull)
    
    # Plot the points and the convex hull
    convex_hull.plot(save_path="convex_hull.png")
