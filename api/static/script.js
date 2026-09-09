async function fetchSign() {
    try {
        const response = await fetch("/get_sign");
        
        if (response && response.ok) {
            const data = await response.json();
            const sign = data.sign;
            const confidence = data.confidence;
            document.getElementById("sign-output").textContent = sign;
            document.getElementById("confidence-output").textContent = confidence;
        } else {
            console.error("Error fetching sign:", response ? response.status : "No response");
        }
    } catch (error) {
        console.error("Error fetching sign:", error);
    }
}

setInterval(fetchSign, 500);
