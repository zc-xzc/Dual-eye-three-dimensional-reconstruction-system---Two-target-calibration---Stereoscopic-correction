def reduce_polygon(polygon: np.array, angle_th: int = 0, distance_th: int = 0) -> np.array(List[int]):
    angle_th_rad = np.deg2rad(angle_th)
    points_removed = [0]
    while len(points_removed):
        points_removed = list()
        for i in range(0, len(polygon) - 2, 2):
            v01 = polygon[i - 1] - polygon[i]
            v12 = polygon[i] - polygon[i + 1]
            d01 = np.linalg.norm(v01)
            d12 = np.linalg.norm(v12)
            if d01 < distance_th and d12 < distance_th:
                points_removed.append(i)
                continue
                angle = np.arccos(np.sum(v01 * v12) / (d01 * d12))
                if angle < angle_th_rad:
                    points_removed.append(i)
        polygon = np.delete(polygon, points_removed, axis=0)
    return polygon


def show_result_reducing(polygon: List[List[int]]) -> List[Tuple[int, int]]:
    original_polygon = np.array([[x, y] for x, y in zip(polygon[0::2], polygon[1::2])])

    tic = time()
    reduced_polygon = reduce_polygon(original_polygon, angle_th=1, distance_th=20)
    toc = time()

    fig = plt.figure(figsize=(16, 5))
    axes = fig.subplots(nrows=1, ncols=2)
    axes[0].scatter(original_polygon[:, 0], original_polygon[:, 1], label=f"{len(original_polygon)}", c='b', marker='x',
                    s=2)
    axes[1].scatter(reduced_polygon[:, 0], reduced_polygon[:, 1], label=f"{len(reduced_polygon)}", c='b', marker='x',
                    s=2)
    axes[0].invert_yaxis()
    axes[1].invert_yaxis()

    axes[0].set_title("Original polygon")
    axes[1].set_title("Reduced polygon")
    axes[0].legend()
    axes[1].legend()

    plt.show()

    print("\n\n", f'[bold black] Original_polygon length[/bold black]: {len(original_polygon)}\n',
          f'[bold black] Reduced_polygon length[/bold black]: {len(reduced_polygon)}\n'
          f'[bold black]Running time[/bold black]: {round(toc - tic, 4)} seconds')

    return reduced_polygon