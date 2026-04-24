from app import create_app
import webview

app = create_app()

if __name__ == "__main__":
    webview.create_window(
        "Management QuickPlan",
        app,
        width=1400,
        height=900,
        resizable=True
    )
    webview.start()