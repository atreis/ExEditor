pyinstaller -D --clean --noconsole --distpath winexe --icon images/logo.ico RxEditor.py
mkdir winexe\RxEditor\images
xcopy images winexe\RxEditor\images /s /e
