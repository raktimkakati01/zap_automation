from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CREDENTIALS, LOGIN_URL

def perform_login():
    driver = webdriver.Chrome()

    try:
        # Open the login page
        driver.get(LOGIN_URL)

        # Expand login dropdown
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logindropdown"))
        )
        dropdown_button.click()

        # Wait for login fields
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "LoginForm_email"))
        )
        password_field = driver.find_element(By.ID, "LoginForm_password")
        login_button = driver.find_element(By.ID, "loginbtn")

        # Interact with the fields
        email_field.send_keys(CREDENTIALS["username"])
        password_field.send_keys(CREDENTIALS["password"])
        login_button.click()

        # Wait for successful login
        WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
        print("Login successful!")

    except Exception as e:
        print(f"An error occurred during login: {e}")

    finally:
        driver.quit()
