import { flasks, foodItems, weaponImbues, augmentRunes, raidBuffs, externalBuffs, potions } from "../utils/data/buffs-consumables-data.js";
import { createTooltip, addTooltipFunctionality } from "../utils/misc-functions.js";
import { createElement } from "./index.js";
import { spellToIconsMap } from "../utils/spell-to-icons-map.js";

const handleOverhealingPercentagesModal = () => {
    const button = document.getElementById("overhealing-header-paste-icon");
    const modal = document.getElementById("overhealing-percentages-modal");
    const modalContent = document.getElementById("overhealing-percentages-modal-content");
    const headerText = document.getElementById("overhealing-modal-header");
    const headerSaveButton = document.getElementById("overhealing-modal-save-button");

    let text = `Afterimage 0%
    Avenging Crusader (Crusader Strike) 0%
    Avenging Crusader (Judgment) 0%
    Barrier of Faith 0%
    Barrier of Faith (Flash of Light) 0%
    Barrier of Faith (Holy Light) 0%
    Barrier of Faith (Holy Shock) 0%
    Beacon of Light 0%
    Crusader's Reprieve 0%
    Dawnlight (AoE) 0%
    Dawnlight (HoT) 0%
    Eternal Flame 0%
    Eternal Flame (HoT) 0%
    Flash of Light 0%
    Gift of the Naaru 0%
    Glimmer of Light 0%
    Glimmer of Light (Daybreak) 0%
    Golden Path 0%
    Greater Judgment 0%
    Holy Bulwark 0%
    Holy Light 0%
    Holy Prism 0%
    Holy Reverberation 0%
    Holy Shock 0%
    Holy Shock (Divine Resonance) 0%
    Holy Shock (Divine Toll) 0%
    Holy Shock (Rising Sunlight) 0%
    Judgment of Light 0%
    Lay on Hands 0%
    Light of Dawn 0%
    Light of the Martyr 0%
    Light's Hammer 0%
    Merciful Auras 0%
    Overflowing Light 0%
    Resplendent Light 0%
    Sacred Weapon 0%
    Saved by the Light 0%
    Seal of Mercy 0%
    Sun Sear 0%
    Touch of Light 0%
    Tyr's Deliverance 0%
    Veneration 0%
    Word of Glory 0%
    Blossom of Amirdrassil Absorb 0%
    Blossom of Amirdrassil Large HoT 0%
    Blossom of Amirdrassil Small HoT 0%
    Broodkeeper's Promise 0%
    Echoing Tyrstone 0%
    Miniature Singing Stone 0%
    Rashok's Molten Heart 0%
    Restorative Sands 0%
    Smoldering Seedling 0%
    Dreaming Devotion 0%
    Larodar's Fiery Reverie 0%
    Leech 0%`;

    modalContent.value = text;

    modal.style.display = "none";
    headerSaveButton.style.display = "none";
    const updateModalContent = () => {
        let text = [];
        const items = document.querySelectorAll(".overhealing-item-container");
        items.forEach(item => {
            const name = item.querySelector(".overhealing-item-text").textContent;
            const percentage = item.querySelector(".overhealing-item-input").value;
            text.push(`${name} ${percentage}%`);
        });
        modalContent.value = text.join("\n");
    };

    const toggleModal = () => {
        const isModalVisible = modal.style.display === "flex";
        modal.style.display = isModalVisible ? "none" : "flex";
        button.classList.toggle("overhealing-header-icon-active", !isModalVisible);
        headerText.style.display = isModalVisible ? "flex" : "none";
        headerSaveButton.style.display = isModalVisible ? "none" : "flex";
    };

    button.addEventListener("click", () => {
        updateModalContent();
        toggleModal();
    });

    headerSaveButton.addEventListener("click", () => {
        text = modalContent.value.split("\n");
        const items = document.querySelectorAll(".overhealing-item-container");
        items.forEach(item => {
            const parts = text.shift().split(/ (?!.* )/);
            const newAbilityName = parts[0];
            const newPercentage = parts[1].replace("%", "");

            item.querySelector(".overhealing-item-text").textContent = newAbilityName;
            item.querySelector(".overhealing-item-input").value = newPercentage;
        });
        toggleModal();
    });

    const copyButton = document.getElementById("overhealing-header-copy-icon");
    const overhealingPercentagesCopyNotification = document.getElementById("overhealing-notification");
    copyButton.addEventListener("click", () => {
        const overhealingPercentagesString = modalContent.value.split("\n").map(line => line.trim()).join("\n");

        navigator.clipboard.writeText(overhealingPercentagesString).then(() => {
            overhealingPercentagesCopyNotification.style.opacity = "1";
            setTimeout(() => {
                overhealingPercentagesCopyNotification.style.opacity = "0";
            }, 2000);
        }).catch(err => {
            console.error("Failed to copy overhealing percentages to clipboard: ", err);
        });
    });
};

const handleOverhealingAbilitiesModal = () => {
    const button = document.querySelector(".overhealing-abilities-button");
    const modal = document.getElementById("overhealing-abilities-modal");
    modal.style.display = "none";

    const overhealingCheckbox = document.getElementById("enable-overhealing-option");
    overhealingCheckbox.addEventListener("change", () => {
        if (overhealingCheckbox.checked) {
            button.style.display = "flex";
        } else {
            button.style.display = "none";
            modal.style.display = "none";
        };
    });

    button.addEventListener("click", () => {
        modal.style.display = modal.style.display === "none" ? "flex" : "none";
    });

    const createOverhealingItem = (name) => {
        const container = createElement("div", "overhealing-item-container", null);
        const image = createElement("img", "overhealing-item-image", null);
        image.src = spellToIconsMap[name];
        image.draggable = false;
        container.appendChild(image);

        const text = createElement("div", "overhealing-item-text", null);
        text.textContent = name;
        container.appendChild(text);

        const inputContainer = createElement("div", "overhealing-item-input-container", null);
        const input = createElement("input", "overhealing-item-input", null);
        input.value = 0;
        const percentage = createElement("span", "overhealing-item-percentage", null);
        percentage.textContent = "%";
        inputContainer.appendChild(input);
        inputContainer.appendChild(percentage);
        container.appendChild(inputContainer);

        return container;
    };

    const abilitiesList = document.getElementById("overhealing-abilities-list");
    const trinketsList = document.getElementById("overhealing-trinkets-list");
    const miscellaneousList = document.getElementById("overhealing-miscellaneous-list");

    const abilities = [
        "Afterimage",
        "Avenging Crusader (Crusader Strike)",
        "Avenging Crusader (Judgment)",
        "Barrier of Faith",
        "Barrier of Faith (Flash of Light)",
        "Barrier of Faith (Holy Light)",
        "Barrier of Faith (Holy Shock)",
        "Beacon of Light",
        "Crusader's Reprieve",
        "Dawnlight (AoE)",
        "Dawnlight (HoT)",
        "Eternal Flame",
        "Eternal Flame (HoT)",
        "Flash of Light",
        "Gift of the Naaru",
        "Glimmer of Light", 
        "Glimmer of Light (Daybreak)",
        "Golden Path",
        "Greater Judgment",
        "Holy Bulwark",
        "Holy Light",
        "Holy Prism",
        "Holy Reverberation",
        "Holy Shock",
        "Holy Shock (Divine Resonance)",
        "Holy Shock (Divine Toll)",
        "Holy Shock (Rising Sunlight)",
        "Judgment of Light",
        "Lay on Hands",
        "Light of Dawn",
        "Light of the Martyr",
        "Light's Hammer",
        "Merciful Auras",
        "Overflowing Light",
        "Resplendent Light",
        "Sacred Weapon",
        "Saved by the Light",
        "Seal of Mercy",
        "Sun Sear",
        "Touch of Light",
        "Tyr's Deliverance",
        "Veneration",
        "Word of Glory"
    ];
    const trinkets = [
        "Blossom of Amirdrassil Absorb",
        "Blossom of Amirdrassil Large HoT",
        "Blossom of Amirdrassil Small HoT",
        "Broodkeeper's Promise",
        "Echoing Tyrstone",
        "Miniature Singing Stone",
        "Rashok's Molten Heart",
        "Restorative Sands",
        "Smoldering Seedling",
    ];
    const miscellaneous = [
        "Dreaming Devotion",
        "Larodar's Fiery Reverie",
        "Leech"
    ];

    for (const spell of abilities) {
        const overhealingItem = createOverhealingItem(spell);
        abilitiesList.appendChild(overhealingItem);
    };

    for (const spell of trinkets) {
        const overhealingItem = createOverhealingItem(spell);
        trinketsList.appendChild(overhealingItem);
    };

    for (const spell of miscellaneous) {
        const overhealingItem = createOverhealingItem(spell);
        miscellaneousList.appendChild(overhealingItem);
    };

    handleOverhealingPercentagesModal();
};

const getOverhealingPercentages = () => {
    const percentages = {};

    const overhealingItems = document.querySelectorAll(".overhealing-item-container");
    overhealingItems.forEach(item => {
        const name = item.querySelector(".overhealing-item-text").textContent;
        const percentage = Number(item.querySelector(".overhealing-item-input").value) / 100;
        percentages[name] = percentage;

        if (name.includes("Glimmer of Light")) {
            percentages["Glimmer of Light (Divine Toll)"] = percentage;
            percentages["Glimmer of Light (Rising Sunlight)"] = percentage;
            percentages["Glimmer of Light (Glistening Radiance (Light of Dawn))"] = percentage;
            percentages["Glimmer of Light (Glistening Radiance (Word of Glory))"] = percentage;
        };

        if (name.includes("Sacred Weapon")) {
            percentages["Sacred Weapon 1"] = percentage;
            percentages["Sacred Weapon 2"] = percentage;
        };

        if (name.includes("Afterimage")) {
            percentages["Afterimage (Word of Glory)"] = percentage;
            percentages["Afterimage (Eternal Flame)"] = percentage;
            percentages["Afterimage"] = 0;
        };
    });

    return percentages;
};

const setSimulationOptionsFromImportedData = (importedData) => {
    const importedRace = importedData.race;

    const raceImages = document.querySelectorAll(".race-image");
    raceImages.forEach(image => {
        if (image.getAttribute("data-race") === importedRace) {
            image.classList.remove("race-unselected");
            image.classList.add("race-selected");
        } else {
            image.classList.add("race-unselected");
            image.classList.remove("race-selected");
        };
    });
};

const colourStatWords = (text) => {
    let words = ["intellect", "haste", "crit", "mastery", "versatility", "critical strike", "leech", "healing", "damage", "mana"];
    let styledText = text;

    words.forEach(word => {
        let colourVariable = `var(--stat-${word.toLowerCase()})`;
        if (word === "critical strike") {
            colourVariable = "var(--stat-crit)";
        } else if (word === "healing") {
            colourVariable = "var(--healing-font)";
        } else if (word === "damage") {
            colourVariable = "var(--red-font-hover)";
        } else if (word === "mana") {
            colourVariable = "var(--mana)";
        };

        const regex = new RegExp(`\\b${word}\\b`, "gi");
        styledText = styledText.replace(regex, (match) => `<span style="color: ${colourVariable}">${match}</span>`);
});

    return styledText;
};

const generateBuffsConsumablesImages = () => {
    const flaskFilterContainer = document.getElementById("flask-filter-container");
    const flaskTooltip = createTooltip("flask-tooltip", "option-image-tooltip");

    for (const flask in flasks) {
        const flaskImage = createElement("img", "flask-image", null);
        flaskImage.src = flasks[flask].image;
        flaskImage.draggable = false;
        flaskImage.setAttribute("data-flask", flask);
        flaskFilterContainer.appendChild(flaskImage);

        const flaskInnerHTML = `${flask}<br><br>` + colourStatWords(flasks[flask].effect);
        addTooltipFunctionality(flaskImage, flaskTooltip, null, flaskInnerHTML);
    };

    const foodFilterContainer = document.getElementById("food-filter-container");
    const foodTooltip = createTooltip("food-tooltip", "option-image-tooltip");
    for (const food in foodItems) {
        const foodImage = createElement("img", "food-image", null);
        foodImage.src = foodItems[food].image;
        foodImage.draggable = false;
        foodImage.setAttribute("data-food", food);
        foodFilterContainer.appendChild(foodImage);

        const foodInnerHTML = `${food}<br><br>` + colourStatWords(foodItems[food].effect);
        addTooltipFunctionality(foodImage, foodTooltip, null, foodInnerHTML);
    };

    const weaponImbueFilterContainer = document.getElementById("weapon-imbue-filter-container");
    const weaponImbueTooltip = createTooltip("weapon-imbue-tooltip", "option-image-tooltip");
    for (const weaponImbue in weaponImbues) {
        const weaponImbueImage = createElement("img", "weapon-imbue-image", null);
        weaponImbueImage.src = weaponImbues[weaponImbue].image;
        weaponImbueImage.draggable = false;
        weaponImbueImage.setAttribute("data-weapon-imbue", weaponImbue);
        weaponImbueFilterContainer.appendChild(weaponImbueImage);

        const weaponImbueInnerHTML = `${weaponImbue}<br><br>` + colourStatWords(weaponImbues[weaponImbue].effect);
        addTooltipFunctionality(weaponImbueImage, weaponImbueTooltip, null, weaponImbueInnerHTML);
    };

    const augmentRuneFilterContainer = document.getElementById("augment-rune-filter-container");
    const augmentRuneTooltip = createTooltip("augment-rune-tooltip", "option-image-tooltip");
    for (const augmentRune in augmentRunes) {
        const augmentRuneImage = createElement("img", "augment-rune-image", null);
        augmentRuneImage.src = augmentRunes[augmentRune].image;
        augmentRuneImage.draggable = false;
        augmentRuneImage.setAttribute("data-augment-rune", augmentRune);
        augmentRuneFilterContainer.appendChild(augmentRuneImage);

        const augmentRuneInnerHTML = `${augmentRune}<br><br>` + colourStatWords(augmentRunes[augmentRune].effect);
        addTooltipFunctionality(augmentRuneImage, augmentRuneTooltip, null, augmentRuneInnerHTML);
    };

    const manaPotionContainer = document.getElementById("aerated-mana-potion-container");
    const manaPotionTooltip = createTooltip("mana-potion-tooltip", "option-image-tooltip");
    const manaPotionImage = manaPotionContainer.querySelector(".potion-image");
    manaPotionImage.src = potions["Aerated Mana Potion"].image;
    manaPotionImage.draggable = false;
    manaPotionImage.setAttribute("data-potion", "Aerated Mana Potion");

    const manaPotionInnerHTML = `Aerated Mana Potion<br><br>` + colourStatWords(potions["Aerated Mana Potion"].effect);
    addTooltipFunctionality(manaPotionImage, manaPotionTooltip, null, manaPotionInnerHTML);

    const intellectPotionContainer = document.getElementById("elemental-potion-of-ultimate-power-container");
    const intellectPotionTooltip = createTooltip("intellect-potion-tooltip", "option-image-tooltip");
    const intellectPotionImage = intellectPotionContainer.querySelector(".potion-image");
    intellectPotionImage.src = potions["Elemental Potion of Ultimate Power"].image;
    intellectPotionImage.draggable = false;
    intellectPotionImage.setAttribute("data-potion", "Elemental Potion of Ultimate Power");

    const intellectPotionInnerHTML = `Elemental Potion of Ultimate Power<br><br>` + colourStatWords(potions["Elemental Potion of Ultimate Power"].effect);
    addTooltipFunctionality(intellectPotionImage, intellectPotionTooltip, null, intellectPotionInnerHTML);

    const raidBuffsFilterContainer = document.getElementById("raid-buffs-filter-container");
    const raidBuffTooltip = createTooltip("raid-buff-tooltip", "option-image-tooltip");
    for (const raidBuff in raidBuffs) {
        const raidBuffImage = createElement("img", "raid-buff-image", null);
        raidBuffImage.src = raidBuffs[raidBuff].image;
        raidBuffImage.draggable = false;
        raidBuffImage.setAttribute("data-raid-buff", raidBuff);
        raidBuffsFilterContainer.appendChild(raidBuffImage);

        const raidBuffsInnerHTML = `${raidBuff}<br><br>` + colourStatWords(raidBuffs[raidBuff].effect);
        addTooltipFunctionality(raidBuffImage, raidBuffTooltip, null, raidBuffsInnerHTML);
    };

    const powerInfusionContainer = document.getElementById("power-infusion-container");
    const powerInfusionTooltip = createTooltip("power-infusion-tooltip", "option-image-tooltip");
    const powerInfusionImage = powerInfusionContainer.querySelector(".external-buff-image");
    powerInfusionImage.src = externalBuffs["Power Infusion"].image;
    powerInfusionImage.draggable = false;
    powerInfusionImage.setAttribute("data-external-buff", "Power Infusion");

    const powerInfusionInnerHTML = `Power Infusion<br><br>` + colourStatWords(externalBuffs["Power Infusion"].effect);
    addTooltipFunctionality(powerInfusionImage, powerInfusionTooltip, null, powerInfusionInnerHTML);

    const innervateContainer = document.getElementById("innervate-container");
    const innervateTooltip = createTooltip("innervate-tooltip", "option-image-tooltip");
    const innervateImage = innervateContainer.querySelector(".external-buff-image");
    innervateImage.src = externalBuffs["Innervate"].image;
    innervateImage.draggable = false;
    innervateImage.setAttribute("data-external-buff", "Innervate");

    const innervateInnerHTML = `Innervate<br><br>` + colourStatWords(externalBuffs["Innervate"].effect);
    addTooltipFunctionality(innervateImage, innervateTooltip, null, innervateInnerHTML);

    const sourceOfMagicContainer = document.getElementById("source-of-magic-container");
    const sourceOfMagicTooltip = createTooltip("source-of-magic-tooltip", "option-image-tooltip");
    const sourceOfMagicImage = sourceOfMagicContainer.querySelector(".external-buff-image");
    sourceOfMagicImage.src = externalBuffs["Source of Magic"].image;
    sourceOfMagicImage.draggable = false;
    sourceOfMagicImage.setAttribute("data-external-buff", "Source of Magic");

    const sourceOfMagicInnerHTML = `Source of Magic<br><br>` + colourStatWords(externalBuffs["Source of Magic"].effect);
    addTooltipFunctionality(sourceOfMagicImage, sourceOfMagicTooltip, null, sourceOfMagicInnerHTML);
};

export { handleOverhealingAbilitiesModal, getOverhealingPercentages, setSimulationOptionsFromImportedData, generateBuffsConsumablesImages };