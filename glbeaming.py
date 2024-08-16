import yaml
from geopy.distance import geodesic
from math import radians, sin, cos, atan2, degrees

# Function to convert grid locator to latitude and longitude
def grid_to_latlong(locator):
    # Validate the length of the locator (should be 4 or 6)
    if len(locator) not in [4, 6]:
        return None, None
    
    try:
        if len(locator) == 4:
            locator += "MM"  # Default to the center of the square if 4 digits are provided
        
        A = ord(locator[0].upper()) - ord('A')
        B = ord(locator[1].upper()) - ord('A')
        C = int(locator[2])
        D = int(locator[3])
        E = ord(locator[4].upper()) - ord('A')
        F = ord(locator[5].upper()) - ord('A')
        
        lon = (A * 20 - 180) + (C * 2) + (E / 12) + 1/24
        lat = (B * 10 - 90) + D + (F / 24) + 1/48
        
        return lat, lon
    except (IndexError, ValueError):
        return None, None

# Function to calculate azimuth between two points
def calculate_azimuth(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(dlon))
    
    azimuth = atan2(x, y)
    azimuth = degrees(azimuth)
    azimuth = (azimuth + 360) % 360
    
    # Opposite azimuth
    opposite_azimuth = (azimuth + 180) % 360
    
    return azimuth, opposite_azimuth

# Load the reference point from YAML
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

reference_locator = config['reference_point']['locator']

# Convert reference grid locator to latitude and longitude
reference_lat, reference_lon = grid_to_latlong(reference_locator)

# Loop until a valid target grid locator is entered
while True:
    target_locator = input("Enter the target grid locator (4 or 6 digits): ")
    target_lat, target_lon = grid_to_latlong(target_locator)
    
    if target_lat is not None and target_lon is not None:
        break
    else:
        print("Invalid grid locator. Please enter a valid 4 or 6-digit grid locator.")

# Calculate distance and azimuth
distance = geodesic((reference_lat, reference_lon), (target_lat, target_lon)).km
azimuth, opposite_azimuth = calculate_azimuth(reference_lat, reference_lon, target_lat, target_lon)

# Display the results
print(f"Distance: {distance:.2f} km")
print(f"Azimuth (nearest): {azimuth:.2f}°")
print(f"Azimuth (opposite): {opposite_azimuth:.2f}°")
