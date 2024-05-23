<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]

<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Holy Paladin Sim</h3>

  <p align="center">
    An app that simulates healing for Holy Paladins in World of Warcraft: Dragonflight
    <br />
    <a href="https://seacelery.github.io/holy-paladin-sim/">Live website</a>

  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ul>
    <li><a href="#about">About</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#license">License</a></li>
  </ul>
</details>

## About

<img src="https://i.imgur.com/6IcXgsQ.png" alt="Image 5" style="width: 100%; height: auto; margin-bottom: 10px; border: 1px solid #3c3241">

<p align="right"><a href="#readme-top">back to top</a></p>

## Features

* Simulate a range of conditions to tailor your gameplay towards the encounter you're facing
* Change your character's loadout - including talents, equipment, group and external buffs
* Use a preset priority list or create your own to discover the optimal way to play in various situations
* Detailed graphs, tables, and a timeline overview of the encounter that lets you see the precise details of the simulation
* Preview many of the new changes from future patches in action to be prepared ahead of time
* Includes a standard dark mode theme & a more paladin-inspired dark mode theme

<p align="right"><a href="#readme-top">back to top</a></p>

## Usage
<div style="display: grid; grid-template-columns: 1fr; gap: 20px;">

  <div>
    <div style="margin-bottom: 15px; font-weight: bold">1. Options</div>
    <br>
    <div>
      <img src="https://i.imgur.com/ITrtlF5.png" alt="Image 1" style="width: 600px; height: auto; margin-bottom: 10px; border: 1px solid #3c3241">
    </div>
    <div style="margin-bottom: 5px;">
        For accuracy, always simulate with at least 100 iterations. Single iteration sims can be helpful if you just want to confirm the simulation is doing what you expect it to based on the priority list via the timeline tab.
    </div>
  </div>
    <br>
  <div>
    <div style="margin-bottom: 15px; font-weight: bold">2. Talents</div style="margin-bottom: 15px;">
    <br>
    <div>
      <img src="https://i.imgur.com/vLu8yEu.png" alt="Image 2" style="width: 600px; height: auto; margin-bottom: 10px; border: 1px solid #3c3241">
    </div>
    <div style="margin-bottom: 5px;">
        Left click an icon to add a talent point, right click to remove them.
    </div>
  </div>
    <br>
  <div>
    <div style="margin-bottom: 15px; font-weight: bold">3. Equipment</div style="margin-bottom: 15px;">
    <br>
    <div>
      <img src="https://i.imgur.com/SDG6kJw.png" alt="Image 3" style="width: 600px; height: auto; margin-bottom: 10px; border: 1px solid #3c3241">
    </div>
    <div style="margin-bottom: 5px;">
        For accuracy, always simulate with at least 100 iterations. Single iteration sims can be helpful if you just want to confirm the simulation is doing what you expect it to based on the priority list via the timeline tab.
    </div>
  </div>
    <br>
  <div>
    <div style="margin-bottom: 15px; font-weight: bold">4. Buffs & Consumables</div style="margin-bottom: 15px;">
    <br>
    <div>
      <img src="https://i.imgur.com/Hfev4ZQ.png" alt="Image 4" style="width: 600px; height: auto; margin-bottom: 10px; border: 1px solid #3c3241">
    </div>
    <div style="margin-bottom: 5px;">
        Some buffs like Innervate and Power Infusion have timer options where you can set each specific timer or press the repeat button to use it on cooldown after the first specified time.
    </div>
  </div>
    <br>
  <div>
    <div style="margin-bottom: 15px; font-weight: bold">5. Priority List</div style="margin-bottom: 15px;">
    <br>
    <div>
      <img src="https://i.imgur.com/ItpkVJc.png" alt="Image 5" style="width: 600px; height: auto; margin-bottom: 10px; border: 1px solid #3c3241">
    </div>
    <div style="margin-bottom: 5px;">
        There are some helpful buttons in the top right to aid you in creating priority lists:
        <br>
        <br>
        Presets: 
        it's recommended to stick with a preset priority list at first as it can get very complicated. 
        <br>
        Copy: this allows you to copy your current priority list in text form.
        <br>
        Paste: here you can paste a priority list or write it from scratch, which will be displayed in the UI when it's saved.
        <br>
        Help: for when you want to create your own priority list - it contains all of the conditions and operations that can be used in the priority list, with some examples.
    </div>
  </div>
  
  <div>
    <div style="margin-bottom: 15px; font-weight: bold">6. Optionally give your simulation a name, then press Simulate and take a look at the results!</div style="margin-bottom: 15px;">
    <br>
  </div>

</div>


## Installation

If you have PyPy3 installed, you can use "pypy3" in place of "python" in the following commands for a performance increase, but it's not required.

#### 1. Clone the local repository found here: https://github.com/seacelery/holy-paladin-sim-local
```bash
  git clone https://github.com/seacelery/holy-paladin-sim-local.git
  cd holy-paladin-sim-local
```
#### 2. Create & activate a virtual environment:
```bash
    python -m venv .venv
    .venv\Scripts\activate
```
#### 3. Install dependencies:
```bash
    cd backend
    pip install -r requirements.txt
```
#### 4. Obtain a free Battle.net API key from https://develop.battle.net/access/clients & create a .env file in the root directory with your client ID and client secret included:
```bash
    CLIENT_ID="your id here"
    CLIENT_SECRET="your secret here"
```
#### 5. Run the flask server:
```bash
    python run.py
```
#### 6. In a new terminal, navigate back to holy-paladin-sim-local and run an HTTP server:
```bash
    python -m http.server 5500
```
#### 7. Access the application:

Finally, go to http://127.0.0.1:5500/frontend/public/ to use the app.

<p align="right"><a href="#readme-top">back to top</a></p>

## License

Distributed under the MIT License. See LICENSE.txt for more information.

<p align="right"><a href="#readme-top">back to top</a></p>