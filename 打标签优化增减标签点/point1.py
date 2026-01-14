def mask_to_polygon(mask: np.array, report: bool = False) -> List[int]:
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    polygons = []
    for object in contours:
        coords = []

        for point in object:
            coords.append(int(point[0][0]))
            coords.append(int(point[0][1]))
        polygons.append(coords)

    if report:
        print(f"Number of points = {len(polygons[0])}")

    return np.array(polygons).ravel().tolist()


polygons = mask_to_polygon(mask, report=True)