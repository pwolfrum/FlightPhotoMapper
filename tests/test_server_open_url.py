from gpsimagestomap import server


def test_open_url_prefers_wslview_in_wsl(monkeypatch) -> None:
    monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
    monkeypatch.setattr(server.os, "name", "posix", raising=False)

    launch_calls: list[list[str]] = []

    def fake_run(command, stdout=None, stderr=None, check=False):
        launch_calls.append(command)

        class Result:
            returncode = 0

        return Result()

    browser_calls: list[str] = []

    monkeypatch.setattr(server.subprocess, "run", fake_run)
    monkeypatch.setattr(
        server.webbrowser,
        "open",
        lambda url: browser_calls.append(url) or True,
    )

    server._open_url("http://localhost:5000")

    assert launch_calls
    assert launch_calls[0][0] == "wslview"
    assert browser_calls == []


def test_open_url_prints_manual_hint_when_all_launchers_fail(
    monkeypatch, capsys
) -> None:
    monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
    monkeypatch.setattr(server.os, "name", "posix", raising=False)

    def failing_run(command, stdout=None, stderr=None, check=False):
        class Result:
            returncode = 1

        return Result()

    monkeypatch.setattr(server.subprocess, "run", failing_run)
    monkeypatch.setattr(server.webbrowser, "open", lambda _url: False)

    url = "http://localhost:5000"
    server._open_url(url)

    output = capsys.readouterr().out
    assert "Could not open browser automatically" in output
    assert url in output
