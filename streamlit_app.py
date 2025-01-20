import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}


@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options,
        desired_capabilities=capabilities,
    )


url = st.text_input("Enter a URL:")

if url:
    driver = get_driver()
    driver.get(url)
    screenshot = driver.get_screenshot_as_png()
    logs = driver.get_log("performance")
    st.image(screenshot)
    st.write("Logs:")
    for entry in logs:
        message = entry["message"]
        try:
            # Parse JSON để lấy URL
            url = eval(message)["message"]["params"]["request"]["url"]
            st.code(url)
        except:
            continue

    driver.quit()
