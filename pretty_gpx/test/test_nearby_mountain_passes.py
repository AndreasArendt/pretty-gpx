"""Offline coverage of the temporary nearby peak allowance."""
from unittest.mock import patch
from overpy import Node, Result

from pretty_gpx.common.gpx.gpx_track import GpxTrack
from pretty_gpx.common.request.overpass_request import OverpassQuery
from pretty_gpx.rendering_modes.mountain.data.mountain_passes import process_mountain_passes


def test_nearby_peaks_use_general_550_metre_limit(tmp_path) -> None:
    result = Result()
    for i, name in enumerate(['Nearby summit', 'Distant summit']):
        result.append(Node(node_id=i + 1, lat=37., lon=-3. + i * .01,
                           tags={'name': name, 'ele': '3000'}, attributes={}, result=result))
    query = OverpassQuery(query_unprocessed_results={'mountain_passes': result})
    track = GpxTrack()
    with patch.object(track, 'get_distances_m', return_value=[506., 551.]):
        with patch('pretty_gpx.rendering_modes.mountain.data.mountain_passes.MOUNTAIN_PASS_CACHE.get_path',
                   return_value=str(tmp_path / 'peaks.pkl')):
            points = process_mountain_passes(query, track)
    assert [p.name for p in points] == ['Nearby summit\n(3000 m)']


def test_same_named_osm_entries_merge_but_distinct_peaks_remain() -> None:
    from pretty_gpx.common.drawing.utils.scatter_point import ScatterPoint, ScatterPointCategory
    from pretty_gpx.rendering_modes.mountain.data.mountain_passes import deduplicate_named_passes

    def point(name, lat):
        return ScatterPoint(name=name, lat=lat, lon=-3.65, category=ScatterPointCategory.MOUNTAIN_PASS)

    first = point('Puerto del Suspiro del Moro\n(865 m)', 37.0683)
    closer = point('Puerto del Suspiro del Moro\n(865 m)', 37.0707)
    different = point('Other summit\n(870 m)', 37.071)
    distant = point(first.name, 37.1)
    track = GpxTrack()
    with patch.object(track, 'get_distances_m', return_value=[44., 4., 10., 20.]):
        assert deduplicate_named_passes([first, closer, different, distant], track) == [closer, different, distant]


def test_cached_passes_are_deduplicated(tmp_path) -> None:
    from pretty_gpx.common.drawing.utils.scatter_point import ScatterPoint, ScatterPointCategory
    from pretty_gpx.common.utils.pickle_io import write_pickle

    points = [ScatterPoint(name='Same pass\n(865 m)', lat=lat, lon=-3.65,
                           category=ScatterPointCategory.MOUNTAIN_PASS) for lat in [37.0683, 37.0707]]
    cache = tmp_path / 'peaks.pkl'
    write_pickle(str(cache), points)
    query = OverpassQuery(query_cached_results={'mountain_pass': str(cache)})
    track = GpxTrack()
    with patch.object(track, 'get_distances_m', return_value=[44., 4.]):
        assert process_mountain_passes(query, track) == [points[1]]
