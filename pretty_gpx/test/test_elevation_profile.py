"""Regression tests for markers on distance-based elevation profiles."""
import numpy as np
import pytest

from pretty_gpx.common.drawing.components.elevation_profile import ElevationProfile
from pretty_gpx.common.drawing.utils.scatter_point import ScatterPoint, ScatterPointCategory
from pretty_gpx.common.gpx.gpx_track import GpxTrack


@pytest.mark.parametrize('n_points', [20, 1000])
def test_marker_uses_distance_with_uneven_recording(n_points: int) -> None:
    distances = np.linspace(0, 1, 100) ** 3
    track = GpxTrack(list_lon=distances.tolist(), list_lat=[37.] * 100,
                     list_ele_m=(1000 + distances * 100).tolist(),
                     list_cumul_dist_km=(distances * 90).tolist())
    point = ScatterPoint(name='Peak', lon=track.list_lon[70], lat=37.,
                         category=ScatterPointCategory.MOUNTAIN_PASS)
    profile = ElevationProfile.from_track(track.get_bounds(), track, [point], .45, n_points=n_points)
    index = profile.scatter_indices[point.category][0]
    assert abs(profile.rel_poly_lon[index] - distances[70]) <= 1 / min(n_points, 100)


def test_draw_labels_peaks_and_omits_climbing_suffix() -> None:
    from unittest.mock import MagicMock
    from pretty_gpx.rendering_modes.mountain.drawing.mountain_params import MountainParams

    track = GpxTrack(list_lon=[0., 1., 2.], list_lat=[37., 37.1, 37.],
                     list_ele_m=[1000., 2000., 1000.], list_cumul_dist_km=[0., 10., 20.],
                     uphill_m=1000.)
    peak = ScatterPoint(name='Summit\n(2000 m)', lon=1., lat=37.1,
                        category=ScatterPointCategory.MOUNTAIN_PASS)
    start = ScatterPoint(name='Start', lon=0., lat=37., category=ScatterPointCategory.START)
    profile = ElevationProfile.from_track(track.get_bounds(), track, [start, peak], .45)
    drawing = MagicMock()
    profile.draw(drawing, MountainParams.default())
    texts = [call.kwargs['s'] for call in drawing.text.call_args_list]
    assert texts == ['20.00 km - 1000 m']
    assert drawing.profile_labels.call_args.kwargs['points'][0][2] == peak.name
    assert profile.peak_labels == [(1, peak.name)]
    assert profile.rel_poly_lat[1] < .9  # Headroom for the summit label.


@pytest.mark.parametrize('offsets, expected', [
    ([-.02, 0., .02, 0., -.02], [1, 3]),  # Out and back across the same summit.
    ([-.02, 0., 0., 0., .02], [1]),  # Pausing at a summit is one visit.
    ([-.02, .0061, .0063, .0061, -.02], [1]),  # Small boundary excursions.
])
def test_peak_labels_each_separate_visit(offsets, expected) -> None:
    track = GpxTrack(list_lon=offsets, list_lat=[37.] * len(offsets),
                     list_ele_m=[1000., 2000., 1000., 2000., 1000.],
                     list_cumul_dist_km=[0., 2., 4., 6., 8.])
    peak = ScatterPoint(name='Summit', lon=0., lat=37., category=ScatterPointCategory.MOUNTAIN_PASS)
    points = [peak]
    profile = ElevationProfile.from_track(track.get_bounds(), track, points, .45)
    assert profile.scatter_indices[peak.category] == expected
    assert profile.peak_labels == [(index, peak.name) for index in expected]
    assert points == [peak]  # Map markers remain a single geographic point.


@pytest.mark.parametrize('furthest_distance, expected', [(726., [0]), (1200., [0, 2])])
def test_turnaround_near_peak_is_one_visit(furthest_distance, expected) -> None:
    from unittest.mock import patch

    track = GpxTrack(list_lon=[0., .01, 0.], list_lat=[37.] * 3,
                     list_ele_m=[3200., 3250., 3200.],
                     list_cumul_dist_km=[46.8, 47.4, 48.0])
    peak = ScatterPoint(name='Summit', lon=0., lat=37., category=ScatterPointCategory.MOUNTAIN_PASS)
    with patch('pretty_gpx.common.drawing.components.elevation_profile.get_pairwise_distance_m',
               return_value=np.array([[506., furthest_distance, 507.]])):
        profile = ElevationProfile.from_track(track.get_bounds(), track, [peak], .45)
    assert profile.scatter_indices[peak.category] == expected


def test_vertical_profile_labels_do_not_overlap() -> None:
    import matplotlib.pyplot as plt
    from pretty_gpx.common.drawing.utils.drawing_figure import DrawingFigure
    from pretty_gpx.common.gpx.gpx_bounds import GpxBounds
    from pretty_gpx.common.layout.paper_size import PAPER_SIZES
    from pretty_gpx.rendering_modes.mountain.drawing.mountain_params import MountainParams

    x = np.linspace(0, 1, 101)
    track = GpxTrack(list_lon=x.tolist(), list_lat=[37.] * len(x),
                     list_ele_m=(1000 + 1000 * np.sin(np.pi * x)).tolist(),
                     list_cumul_dist_km=(100 * x).tolist())
    points = [ScatterPoint(name=f'Nearby mountain {i}\n(2000 m)', lon=lon, lat=37.,
                            category=ScatterPointCategory.MOUNTAIN_PASS)
              for i, lon in enumerate([.495, .50, .505])]
    bounds = GpxBounds(0., 1., 0., .22)
    profile = ElevationProfile.from_track(bounds, track, points, .45)
    fig, ax = plt.subplots()
    try:
        with DrawingFigure(PAPER_SIZES['A4'], GpxBounds(0., 1., 0., 1.), fig, ax) as drawing:
            profile.draw(drawing, MountainParams.default())
        fig.canvas.draw()
        boxes = [label.get_window_extent(fig.canvas.get_renderer()) for label in ax.texts[:-1]]
        assert len(boxes) == 3
        assert all(label.get_rotation() == 90 for label in ax.texts[:-1])
        assert all(label.arrow_patch is None for label in ax.texts[:-1])
        assert not any(a.overlaps(b) for i, a in enumerate(boxes) for b in boxes[i + 1:])
        ordered = sorted(boxes, key=lambda box: box.x0)
        # At least 2 mm of breathing room on A4, even for almost coincident markers.
        gap_px = 2 / 25.4 * fig.dpi
        assert all(b.x0 - a.x1 >= gap_px - .1 for a, b in zip(ordered, ordered[1:]))
    finally:
        plt.close(fig)
