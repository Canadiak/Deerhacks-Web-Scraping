# Deerhacks NBA prediction

[Live Preview](https://deerhacks-landing-page.vercel.app/)

### Introduction

This is our submission for Deerhacks 2022. It is a python based application to predict who would win the next NBA game.

### Technologies

* Flask
* Selenium
* Scikit Learn
* Numpy
* React

### Tools

* Visual Studio Code
* Jupyter Notebook
* Terminal
* Git and GitHub

### Webscraping

The project used Python Selenium to gather reference data from basketball-reference.com. Using XPath to identify HTML elements in tables based off their relative position to the names of the playoffs team, automation was used to gather the League stats for years 1990-2019. The script then pulled the text content from each HTML element, which would be the raw data the ML model would need, and wrote it into an easy to read CSV.

## Contributers

👤 **Manik Rana**
* [Jeremy](https://github.com/Canadiak) Scraped the web 
* [Arhum](https://github.com/ArhumAhmad) Build ML model and flask backend
* [Manik](https://github.com/Maniktherana) Developed frontend
* [James](https://github.com/jameskimdev) Developed frontend
