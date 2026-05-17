import csv
import json
from pathlib import Path


def point_in_ring(point, ring):
    x, y = point
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        intersects = ((y1 > y) != (y2 > y)) and (
            x < (x2 - x1) * (y - y1) / (y2 - y1 + 0.0) + x1
        )
        if intersects:
            inside = not inside
    return inside


def point_in_polygon(point, polygon):
    if not polygon:
        return False
    if polygon[0] and isinstance(polygon[0][0], list):
        # Assumes polygon is [outer_ring, hole1, hole2, ...]
        if not point_in_ring(point, polygon[0]):
            return False
        for hole in polygon[1:]:
            if point_in_ring(point, hole):
                return False
        return True
    return False


def locate_locality(point, locality_features):
    for feature in locality_features:
        geom = feature.get("geometry") or {}
        geom_type = geom.get("type")
        coords = geom.get("coordinates")
        if geom_type == "Polygon" and coords:
            if point_in_polygon(point, coords):
                return feature.get("properties", {}).get("LOCALITY")
        elif geom_type == "MultiPolygon" and coords:
            for poly in coords:
                if point_in_polygon(point, poly):
                    return feature.get("properties", {}).get("LOCALITY")
    return None


def load_geojson(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    root = Path(__file__).resolve().parent
    points_path = root / "data" / "export.geojson"
    polygons_path = root / "data" / "LOCALITY_POLYGON.json"
    output_path = root / "data" / "cafes_by_locality.csv"

    points_geojson = load_geojson(points_path)
    polygons_geojson = load_geojson(polygons_path)

    locality_features = polygons_geojson.get("features", [])
    counts = {}
    unknown_count = 0

    for feature in points_geojson.get("features", []):
        geom = feature.get("geometry") or {}
        if geom.get("type") != "Point":
            continue

        point = tuple(geom.get("coordinates", []))
        if len(point) != 2:
            continue

        locality = locate_locality(point, locality_features)
        if not locality:
            locality = "Unknown"
            unknown_count += 1

        counts[locality] = counts.get(locality, 0) + 1

    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["LOCALITY", "cafe_count"])
        for locality, count in sorted_counts:
            writer.writerow([locality, count])

    print(f"Wrote {len(sorted_counts)} rows to {output_path}")
    print(f"Unknown locality cafes: {unknown_count}")


if __name__ == "__main__":
    main()
