"""Double-click launcher for the original Flask/SQLite dashboard."""
import argparse
import json
import logging
import os
from pathlib import Path
import sys
import threading
import webbrowser

from sample_data import prepare_database


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=Path)
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data_dir = args.data_dir or Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'YouTubeChannelStats'
    data_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=data_dir / 'launcher.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    database = data_dir / 'youtube.db'
    prepare_database(database)
    os.environ['YOUTUBE_STATS_DATABASE'] = str(database.resolve())
    import app as dashboard
    if args.self_test:
        client = dashboard.app.test_client()
        for route in ['/channelInfo', '/databaseInfo', '/about', '/static/styles.css', '/static/vendor/bootstrap.min.css', '/static/vendor/bootstrap.bundle.min.js']:
            assert client.get(route).status_code == 200, route
        channel = dashboard.db.execute('SELECT author FROM videos LIMIT 1').fetchone()[0]
        response = client.post('/channelInfo', data={'channelAuthor': channel})
        assert response.status_code == 200
        assert b'General Stats' in response.data
        assert client.post('/channelInfo', data={'channelAuthor': 'missing channel'}).status_code == 302
        dashboard.db.close()
        (data_dir / 'self-test.json').write_text(json.dumps({'passed': True, 'channel': channel}), encoding='utf-8')
        return

    from werkzeug.serving import make_server, WSGIRequestHandler
    class QuietHandler(WSGIRequestHandler):
        def log(self, type, message, *args):
            logging.info(message, *args)

    # One request thread keeps the original SQLite cursor's operations sequential.
    server = make_server('127.0.0.1', args.port, dashboard.app, threaded=False, request_handler=QuietHandler)
    url = f'http://127.0.0.1:{server.server_port}'
    runtime_file = data_dir / 'runtime.json'
    runtime_file.write_text(json.dumps({'url': url, 'pid': os.getpid()}), encoding='utf-8')
    if args.headless:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
            dashboard.db.close()
            runtime_file.unlink(missing_ok=True)
        return

    import tkinter as tk
    from tkinter import ttk
    root = tk.Tk()
    root.title('YouTube Channel Stats')
    root.geometry('440x230')
    root.resizable(False, False)
    frame = ttk.Frame(root, padding=24)
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='Your dashboard is running', font=('Segoe UI', 15, 'bold')).pack(anchor='w')
    ttk.Label(frame, text='Explore channel statistics in your browser.\nClose this window to stop the dashboard.').pack(anchor='w', pady=(12, 8))
    ttk.Label(frame, text=url).pack(anchor='w', pady=(0, 16))
    buttons = ttk.Frame(frame)
    buttons.pack(anchor='w')
    ttk.Button(buttons, text='Open dashboard', command=lambda: webbrowser.open(url)).pack(side='left', padx=(0, 10))
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    def stop():
        server.shutdown()
        worker.join(timeout=5)
        server.server_close()
        dashboard.db.close()
        runtime_file.unlink(missing_ok=True)
        root.destroy()
    ttk.Button(buttons, text='Stop and close', command=stop).pack(side='left')
    root.protocol('WM_DELETE_WINDOW', stop)
    if not args.no_browser:
        root.after(250, lambda: webbrowser.open(url))
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logging.exception('Dashboard failed to start')
        if '--headless' not in sys.argv and '--self-test' not in sys.argv:
            from tkinter import messagebox
            messagebox.showerror('YouTube Channel Stats', 'The dashboard could not start. Details are in YouTubeChannelStats/launcher.log in your local app data folder.')
        sys.exit(1)
