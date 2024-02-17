import geojson
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import os

# convert coordinates into Mercator Projection
def map2xy(long, lat, mapWidth, mapHeight):

    # get x value
    x = (long + 180) * (mapWidth / 360)

    # convert from degrees to radians
    latRad = lat * np.pi / 180

    # get y value
    mercN = np.log(np.tan((np.pi / 4) + (latRad / 2)))
    y = (mapHeight / 2) - (mapWidth * mercN / (2 * np.pi))

    return [x, -y]

# draw country shapes
def draw(type,coordinates,name):

    mapWidth = 200
    mapHeight = 100
    stroke_width = 1

    if type == 'Polygon':
        map_coords = coordinates[0]
        coords = [map2xy(coord[0],coord[1],mapWidth,mapHeight) for coord in map_coords]

        x_coords = [coord[0] for coord in coords]
        y_coords = [coord[1] for coord in coords]

        # Create a figure and axis
        fig , ax = plt.subplots(num=name)

        # Create a Polygon from the coordinates and add it to the plot
        polygon = Polygon(coords, closed=True, edgecolor='black',
                          linewidth=stroke_width, facecolor='none')
        ax.add_patch(polygon)

        # Set the aspect ratio
        ax.set_aspect("equal")

        # Adjust the axis limits based on coordinate range
        ax.set_xlim(min(x_coords), max(x_coords))
        ax.set_ylim(min(y_coords), max(y_coords))

        # Add padding around the data points
        ax.margins(0.5)

        # Hide the axes
        ax.axis('off')

    else:
        all_coords = []

        # Create a figure and axis
        fig, ax = plt.subplots(num=name)

        for region_coords in coordinates:

            map_coords = region_coords[0]
            print(map_coords)
            coords = [map2xy(coord[0], coord[1], mapWidth, mapHeight) for coord in map_coords]
            print(coords)

            all_coords = all_coords + coords
            print(all_coords)
            # Create a Polygon from the coordinates and add it to the plot
            polygon = Polygon(coords, closed=True, edgecolor='black',
                          linewidth=stroke_width, facecolor='none')
            ax.add_patch(polygon)

        x_coords = [coord[0] for coord in all_coords]
        y_coords = [coord[1] for coord in all_coords]

        # Adjust the axis limits based on coordinate range
        ax.set_xlim(min(x_coords), max(x_coords))
        ax.set_ylim(min(y_coords), max(y_coords))

        # Add padding around the data points
        ax.margins(0.5)

        # Set the aspect ratio
        ax.set_aspect("equal")

        # Hide the axes
        ax.axis('off')

    # Show the plot
    # plt.show()

    # Create a folder to save the figures in the current working directory
    folder_name = 'Countries Shape'
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Save the figure in the specified folder
    file_path = os.path.join(folder_path, f'{name}.png')
    fig.savefig(file_path)

    # Close the figure
    plt.close(fig)


data_file = "country_shapes.geojson"

with open(data_file) as f:
    data = geojson.load(f)

features = data['features']

for feature in features:
    name = feature.properties['cntry_name']
    type = feature.geometry['type']
    coords = feature.geometry['coordinates']
    print(name)
    print(type)
    print(coords)
    draw(type,coords,name)




