from typing import List, Tuple  # Import the Tuple class from the typing module

class Side:
    """
    Represents a side of an object.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Side class.

        Args:
            name (str): The name of the side.
        """
        self.name = name
        self.points = []  # List to store the points of the side
        self.surfaces = []  # List to store the surfaces of the side

def parse_side(filename: str) -> List[Side]:
    """
    Parses the sides of an object from a file.

    Args:
        filename (str): The path to the file.

    Returns:
        List[Side]: The list of sides parsed from the file.
    """
    sides = []  # List to store the parsed sides
    current_side = None  # Variable to keep track of the current side being parsed

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('o '):
                if current_side is not None:
                    sides.append(current_side)  # Add the previous side to the list of sides
                current_side = Side(line.split()[1].replace('obj', ''))  # Create a new Side object with the name extracted from the line
            elif line.startswith('v '):
                coordinates = list(map(float, line.split()[1:]))  # Extract the point coordinates from the line
                converted_coordinates = [round(coord * 2.54, 1) for coord in coordinates]  # Convert the coordinates to centimeters and round to 1 decimal point
                converted_coordinates = [coord if coord != -0.0 else 0.0 for coord in converted_coordinates] # Convert negative zero to positive zero
                current_side.points.append(converted_coordinates)  # Add the converted coordinates to the current side's points list
            elif line.startswith('f '):
                current_side.surfaces.append(list(map(int, line.split()[1:])))  # Extract the surface indices from the line and add them to the current side's surfaces list

        if current_side is not None:
            sides.append(current_side)  # Add the last side to the list of sides

    return sides

def find_panels(sides: List[Side]) -> List[List[Side]]:
    """
    Finds panels in a list of sides.

    Args:
        sides (List[Side]): The list of sides.

    Returns:
        List[List[Side]]: The list of panels found.
    """
    panels = []  # List to store the found panels
    for i in range(len(sides) - 5):
        group = sides[i:i+6]  # Get a group of 6 consecutive sides
        all_points = [tuple(point) for side in group for point in side.points]  # Flatten the points of all sides in the group into a single list
        all_surfaces = [surface for side in group for surface in side.surfaces]  # Flatten the surfaces of all sides in the group into a single list
        if (all(len(side.points) == 4 for side in group) and  # Check if all sides in the group have 4 points
            all(len(side.surfaces) == 2 for side in group) and  # Check if all sides in the group have 2 surfaces
            len(set(all_points)) == 8 and  # Check if there are 8 unique points in the group
            len(set(tuple(surface) for surface in all_surfaces)) == 12):  # Check if there are 12 unique surfaces in the group
            panels.append(group)  # Add the group of sides as a panel
    return panels

def calculate_panel_properties(panel: List[Side]) -> Tuple[Tuple[float, float, float], float, float, float]:
    """
    Calculates the properties of a panel.

    Args:
        panel (List[Side]): The panel.

    Returns:
        Tuple[Tuple[float, float, float], float, float, float]: The properties of the panel.
    """
    all_points = [tuple(point) for side in panel for point in side.points]  # Flatten the points of all sides in the panel into a single list
    min_x = min(point[0] for point in all_points)  # Find the minimum x-coordinate
    min_y = min(point[1] for point in all_points)  # Find the minimum y-coordinate
    min_z = min(point[2] for point in all_points)  # Find the minimum z-coordinate
    max_x = max(point[0] for point in all_points)  # Find the maximum x-coordinate
    max_y = max(point[1] for point in all_points)  # Find the maximum y-coordinate
    max_z = max(point[2] for point in all_points)  # Find the maximum z-coordinate

    origin = (min_x, min_y, min_z)  # The origin point of the panel
    dimensions = sorted([max_x - min_x, max_y - min_y, max_z - min_z])  # Calculate the dimensions of the panel
    length, width, height = round(dimensions[2], 1), round(dimensions[1], 1), round(dimensions[0], 1)  # Round the dimensions to 1 decimal point

    return origin, length, width, height

def main():
    """
    The main function.
    """
    #sides = parse_side('simple.obj')  # Parse the sides from the specified file
    sides = parse_side('complex.obj') # Parse the sides from the specified file

    panels = find_panels(sides)  # Find the panels in the parsed sides

    #for side in sides:
    #    print(f"Side: {side.name}")  # Print the name of each side
    #    print(f"Points: {side.points}")  # Print the points of each side
    #    print(f"Surfaces: {side.surfaces}")  # Print the surfaces of each side
    #    print()

    #for i, panel in enumerate(panels):
    #    print(f"Panel {i+1}:")  # Print the panel number
    #    for side in panel:
    #        print(f"  Side: {side.name}")  # Print the name of each side in the panel
    #        print(f"  Points: {side.points}")  # Print the points of each side in the panel
    #        print(f"  Surfaces: {side.surfaces}")  # Print the surfaces of each side in the panel
    #    print()

    panel_properties = {}  # Dictionary to store the panel properties

    sorted_panels = sorted(panels, key=lambda panel: (calculate_panel_properties(panel)[3], calculate_panel_properties(panel)[1] * calculate_panel_properties(panel)[2]), reverse=True)  # Sort the panels based on their height and area

    for panel in sorted_panels:
        origin, length, width, height = calculate_panel_properties(panel)  # Calculate the properties of each panel
        properties = (length, width, height)  # Create a tuple of the panel properties
        
        if properties in panel_properties:
            panel_properties[properties].append(origin)  # Add the origin to the list of origins for the panel properties
        else:
            panel_properties[properties] = [origin]  # Create a new list of origins for the panel properties

    for properties, origins in panel_properties.items():
        length, width, height = properties
        if len(origins) == 1:
            print(f"  {len(origins)} Panel:")  # Print the number of panels (singular form)
        else:
            print(f"  {len(origins)} Panels:")  # Print the number of panels (plural form)
        print(f"  Length: {length}")  # Print the length of the panel
        print(f"  Width: {width}")  # Print the width of the panel
        print(f"  Height: {height}")  # Print the height of the panel
        if len(origins) == 1:
            print(f"  Origin: {origins[0]}")  # Print the origin of the panel (singular form)
        else:
            print(f"  Origins: {origins}")  # Print the origins of the panel (plural form)
        print()

if __name__ == "__main__":
    main()  # Call the main function