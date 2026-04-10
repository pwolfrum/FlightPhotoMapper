from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from gpsimagestomap.image_discovery import ImageInfo
from gpsimagestomap.main import _run_gui_request, handle_timezone_uncertainty


def _uncertain_image() -> ImageInfo:
    return ImageInfo(
        path=Path("IMG_0001.jpg"),
        timestamp=datetime(2025, 5, 1, 12, 0, tzinfo=timezone.utc),
        has_gps=False,
        tz_certain=False,
    )


def test_handle_timezone_uncertainty_no_stdin_uses_gui_choice_no(monkeypatch):
    images = [_uncertain_image()]

    monkeypatch.setattr("gpsimagestomap.main._stdin_available", lambda: False)
    monkeypatch.setattr(
        "gpsimagestomap.main.detect_timezone_correction",
        lambda tracks, imgs: timedelta(hours=1),
    )
    monkeypatch.setattr("gpsimagestomap.main._count_images_in_tracks", lambda *args: 1)
    monkeypatch.setattr(
        "gpsimagestomap.main._ask_timezone_correction_gui",
        lambda hours, current, corrected: False,
    )

    result = handle_timezone_uncertainty([], images)
    assert result == images


def test_handle_timezone_uncertainty_no_stdin_gui_cancel_exits(monkeypatch):
    images = [_uncertain_image()]

    monkeypatch.setattr("gpsimagestomap.main._stdin_available", lambda: False)
    monkeypatch.setattr(
        "gpsimagestomap.main.detect_timezone_correction",
        lambda tracks, imgs: timedelta(hours=1),
    )
    monkeypatch.setattr("gpsimagestomap.main._count_images_in_tracks", lambda *args: 1)
    monkeypatch.setattr(
        "gpsimagestomap.main._ask_timezone_correction_gui",
        lambda hours, current, corrected: None,
    )

    with pytest.raises(SystemExit):
        handle_timezone_uncertainty([], images)


def test_run_gui_request_geotag_passes_session_log_to_viewer(monkeypatch, tmp_path):
    captured: dict = {}

    monkeypatch.setattr("gpsimagestomap.main._is_valid_directory", lambda path: True)

    def fake_geotag(input_dir, time_offset_minutes=0):
        print("IGNORED: 2 image(s) without EXIF timestamp")
        print("  - foo.jpg")
        return True

    monkeypatch.setattr("gpsimagestomap.main.geotag", fake_geotag)

    import gpsimagestomap.server as server

    def fake_serve(input_dir, **kwargs):
        captured["input_dir"] = input_dir
        captured.update(kwargs)

    monkeypatch.setattr(server, "serve", fake_serve)

    _run_gui_request(
        {
            "mode": "geotag",
            "input_dir": tmp_path,
            "port": 5000,
            "image_mode": "panel",
            "time_offset_minutes": 0.0,
            "include_sequence_line": True,
            "output_dir": None,
            "do_preview": False,
        }
    )

    assert captured["input_dir"] == tmp_path
    assert captured["show_control_window"] is True
    assert "IGNORED: 2 image(s) without EXIF timestamp" in captured["session_log"]
    assert (
        "Close the viewer control window to stop the application."
        in captured["session_log"]
    )


def test_run_gui_request_browse_disables_sequence_line(monkeypatch, tmp_path):
    captured: dict = {}

    monkeypatch.setattr("gpsimagestomap.main._is_valid_directory", lambda path: True)

    def fake_prepare(input_dir):
        print("Ready - 3 image(s)")
        return True

    monkeypatch.setattr("gpsimagestomap.main._prepare_gps_images", fake_prepare)

    import gpsimagestomap.server as server

    def fake_serve(input_dir, **kwargs):
        captured["input_dir"] = input_dir
        captured.update(kwargs)

    monkeypatch.setattr(server, "serve", fake_serve)

    _run_gui_request(
        {
            "mode": "browse",
            "input_dir": tmp_path,
            "port": 5001,
            "image_mode": "panel",
            "time_offset_minutes": 0.0,
            "include_sequence_line": False,
            "output_dir": None,
            "do_preview": False,
        }
    )

    assert captured["input_dir"] == tmp_path
    assert captured["include_tracks"] is False
    assert captured["include_image_sequence_track"] is False
    assert captured["show_control_window"] is True
    assert "Image sequence line disabled" in captured["session_log"]
