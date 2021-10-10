# Google Classroom Video Downloader

Badly written script that uses Selenium to download all videos from a Google Classroom class stream.

Works on Google Classroom in Italian, it's very easy to adapt to other languages just check the code.

It uses `Google Chrome` with `chromedriver`, again it's very easy to adapt to use a different browser/webdriver.

## Usage

Install `Google Chrome`.

Download `chromedriver` to `/usr/bin/chromedriver`.

```bash
git clone https://github.com/marcedavi/google-classroom-video-downloader.git
cd google-classroom-video-downloader
pip install -r requirements.txt
```

Before running open `Google Chrome` and create a new profile, login to `Google Classroom` so that `Chrome` will keep you logged in.

Find the folder where the `Google Chrome` profile you created is stored and update the location inside the script.

```bash
python src/main.py
```

Chrome will open on `classroom.google.com`, open the class stream you're interested in.

Then go back to the terminal and press any key.

The script will start doing it's thing and is going to save you a lot of time.

The videos will be downloaded in your `~/Downloads` folder.