import time

from selenium import webdriver

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument('user-data-dir=/home/md/.config/google-chrome')
options.add_argument('profile-directory=Profile 7')

driver = Chrome(executable_path='/usr/bin/chromedriver', options=options)
driver.get('https://classroom.google.com')

# Wait for course name to start
course_name = input("Press enter when ready...")

# Time to sleep in seconds
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
reached_bottom_checks = 0

ids_done = []
item_links = []
video_links = []

while reached_bottom_checks < 20:

    # Get urls all clickable items
    items = driver.find_elements_by_css_selector('div[jsmodel=PTCFbe][jsaction]')

    for item in items:
        id = item.get_attribute('data-stream-item-id')
        
        if id not in ids_done:
            ids_done.append(id)

            # Open item page
            item.click()

            # Save it's link
            item_links.append(driver.current_url)

            # Go back to course page
            driver.back()


    # Check all non-clickable items
    items = driver.find_elements_by_css_selector('div[jsmodel=PTCFbe]:not([jsaction])')

    for item in items:
        video_anchors = item.find_elements_by_css_selector('a[aria-label^="Allegato: Video:"]')

        for video_link in video_anchors:
            href = video_link.get_attribute('href')
            if href not in video_links:
                video_links.append(href)

    # Scroll down to bottom
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    # Wait for ajax load
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        reached_bottom_checks += 1
    else:
        reached_bottom_checks = 0

    last_height = new_height


# Process each item
for link in item_links:
    driver.get(link)

    time.sleep(5)

    video_anchors = driver.find_elements_by_css_selector('a[aria-label^="Allegato: Video:"]')

    for video_link in video_anchors:
        href = video_link.get_attribute('href')
        if href not in video_links:
            video_links.append(href)


# Download all videos
for video_link in video_links:
    print(video_link)

    driver.get(video_link)
    
    time.sleep(3)

    video_title = driver.title.replace(' - Google Drive', '')
    filename = "".join(c for c in video_title if c.isalnum() or c in [' ', '.', '_']).rstrip()
    
    driver.find_element_by_css_selector('div[data-tooltip=Riproduci]').click()

    time.sleep(3)

    # Change quality to best available
    driver.switch_to.frame(driver.find_element_by_id('drive-viewer-video-player-object-0'))
    driver.find_element_by_css_selector('button.ytp-button.ytp-settings-button').click()
    time.sleep(2)
    driver.find_element_by_css_selector('div.ytp-popup.ytp-settings-menu div.ytp-menuitem:last-child').click()
    time.sleep(2)
    driver.find_element_by_css_selector('div.ytp-popup.ytp-settings-menu div.ytp-menuitem:first-child').click()
    time.sleep(2)

    # Get video source url and open the video page first because chrome doesn't like cross origin download link
    video_source = driver.find_element_by_tag_name('video').get_attribute('src')
    driver.get(video_source)

    # Trigger video download
    driver.execute_script('const a = document.createElement("a");a.innerHTML = "Download";a.href = "' + video_source + '";a.download = "' + filename + '.mp4";document.body.appendChild(a);a.click()')

    time.sleep(20)
