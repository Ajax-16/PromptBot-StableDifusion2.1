from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from tqdm import tqdm

driver = webdriver.Chrome('chromedriver')

driver.get("https://huggingface.co/spaces/stabilityai/stable-diffusion")

element = WebDriverWait(driver, 10)

iframe = driver.find_element(By.XPATH, "//div[@class='SVELTE_HYDRATER contents']//iframe")

driver.switch_to.frame(iframe)

input_space = driver.find_elements(By.TAG_NAME, "input")

file_prompts = open("prompts.txt", "r")

prompts = file_prompts.readlines()

for prompt in prompts:

    input_space[0].send_keys(prompt)

    generate_button = driver.find_elements(By.TAG_NAME, "button")

    generate_button[0].click()

    for i in tqdm(range(100), desc="Progress for prompt " + prompt[0:int(len(prompt)-1)]):

        time.sleep(.5)

    image = driver.find_elements(By.TAG_NAME, "img")

    index = 0

    with open("index.txt", "r+") as index_file:

        index = index_file.read()

        index_file.truncate(0)

        index_file.seek(0)
    
        index_file.write(str(int(index)+1))

        index_file.close()

    os.mkdir("prompt" + str(index) + str(prompt[0:int(len(prompt)-1)]))


    for i in range(0, len(image)):

        file_list = []

        file_list.append(open("./prompt" + str(index) + prompt[0:int(len(prompt)-1)] + "/file"+ str(i) + ".png", "wb"))

        image[i].screenshot("./prompt" + str(index) + prompt[0:int(len(prompt)-1)] + "/file"+ str(i) + ".png".lower())

        if i == len(image)-3:
            break
    
    input_space[0].clear()

    print("Prompt: " + prompt[0:int(len(prompt)-1)] + " generated succesfully")

driver.quit()