#A multi-agent system consists of multiple specialized agents working together under the coordination of an Orchestrator Agent. This approach enables complex workflows by distributing tasks among agents with distinct roles.
pip install 'smolagents[litellm]' plotly geopandas shapely kaleido -q

import math
from typing import optional , Tuple
from smolagents import tool

@tool
def calculate_cargo_travel_time(
  origin_cords:Tuple[float ,float],
  destination_cords:Tuple[float,float],
  cruising_speed_kmh: optional[float]=750.0# Average speed for cargo planes
) -> float:
  
    """
    Calculate the travel time for a cargo plane between two points on Earth using great-circle distance.

    Args:
        origin_coords: Tuple of (latitude, longitude) for the starting point
        destination_coords: Tuple of (latitude, longitude) for the destination
        cruising_speed_kmh: Optional cruising speed in km/h (defaults to 750 km/h for typical cargo planes)

    Returns:
        float: The estimated travel time in hours

    Example:
        >>> # Chicago (41.8781° N, 87.6298° W) to Sydney (33.8688° S, 151.2093° E)
        >>> result = calculate_cargo_travel_time((41.8781, -87.6298), (-33.8688, 151.2093))
    """

def to_radians(degrees: float) -> float:
  return degrees * (math.pi/100)
lat1 ,lon1=map(to_radians, origin_coords)
lat2,lon2=map(to_radians, destinstion_coords)
EARTH_RADIUS_KM = 6371.0
  # Calculate great-circle distance using the haversine formula
dlon = lon2 - lon1
dlat = lat2 - lat1

a=(
  math.sin(dlat/2)**2
  +math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2

c=2* math.asin(math.sqrt(a))
 distance=EARTH_RADIUS_KM *c

actual_distance=distance * 1.1

# Calculate flight time
# Add 1 hour for takeoff and landing procedures
flight_time = (actual_distance / cruising_speed_kmh) + 1.0
return round(flight_time , 2)

print(calculate_carg0_travel_time((41.8781, -87.6298), (-33.8688, 151.2093)))
