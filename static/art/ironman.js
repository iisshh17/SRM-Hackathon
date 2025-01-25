const imgfaceplate = document.getElementById("face-plate")
const buttonfaceplate = document.getElementById("buttonfaceplate")

buttonfaceplate.oninput = () =>{
  imgfaceplate.style.fill = buttonfaceplate.value; 
}

const imghelmet = document.getElementById("helmet")
const buttonhelmet = document.getElementById("buttonhelmet")

buttonhelmet.oninput = () =>{
  imghelmet.style.fill = buttonhelmet.value; 
}

const imgeyes = document.getElementById("eyes")
const buttoneyes = document.getElementById("buttoneyes")

buttoneyes.oninput = () =>{
  imgeyes.style.fill = buttoneyes.value; 
}

const imgbackground = document.getElementById("background")
const buttonbackground = document.getElementById("buttonbackground")

buttonbackground.oninput = () =>{
  imgbackground.style.fill = buttonbackground.value; 
}






function changeLanguage(language) {
    const translations = {
        english: {
            artTherapy: "Art Therapy",
            completeArt: "Complete this art using the color palette",
            colorPalette: "Color Palette",
            faceplate: "Face Plate",
            helmet: "Helmet",
            eyes: "Eyes",
            background: "Background",
        },
        hindi: {
            artTherapy: "कला चिकित्सा",
            completeArt: "इस कला को रंग पैलेट का उपयोग करके पूरा करें",
            colorPalette: "रंग पैलेट",
            faceplate: "चेहरे की प्लेट",
            helmet: "हेलमेट",
            eyes: "आंखें",
            background: "पृष्ठभूमि",
        },
        marathi: {
            artTherapy: "कला उपचार",
            completeArt: "रंग पॅलेट वापरून ही कला पूर्ण करा",
            colorPalette: "रंग पॅलेट",
            faceplate: "चेहरा प्लेट",
            helmet: "हेल्मेट",
            eyes: "आंखा",
            background: "पार्श्वभूमी",
        },
        tamil: {
            artTherapy: "கலை சிகிச்சை",
            completeArt: "இந்தக் கலைக்கான நிறத் தொகுப்பைப் பயன்படுத்தி முழுமைப்படுத்தவும்",
            colorPalette: "நிறத் தொகுப்பு",
            faceplate: "முகப் பலகை",
            helmet: "ஹெல்மெட்",
            eyes: "கண்",
            background: "பின்புலம்",
        },
        bengali: {
            artTherapy: "শিল্প থেরাপি",
            completeArt: "এই শিল্পটি রঙের প্যালেট ব্যবহার করে সম্পূর্ণ করুন",
            colorPalette: "রঙের প্যালেট",
            faceplate: "মুখের প্লেট",
            helmet: "হেলমেট",
            eyes: "চোখ",
            background: "পটভূমি",
        }
    };

    const selectedTranslations = translations[language];

    document.getElementById('artTherapy').textContent = selectedTranslations.artTherapy;
    document.getElementById('completeArt').textContent = selectedTranslations.completeArt;
    document.getElementById('colorPaletteText').textContent = selectedTranslations.colorPalette;

    document.getElementById('text-faceplate').textContent = selectedTranslations.faceplate;
    document.getElementById('text-helmet').textContent = selectedTranslations.helmet;
    document.getElementById('text-eyes').textContent = selectedTranslations.eyes;
    document.getElementById('text-background').textContent = selectedTranslations.background;
}

const closeBtn = document.getElementById("close")
closeBtn.addEventListener("click",()=>{
  window.location.href="/";
})