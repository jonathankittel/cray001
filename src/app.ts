const form = document.getElementById("userForm") as HTMLFormElement;
const input = document.getElementById("userInput") as HTMLInputElement;
const output = document.getElementById("output") as HTMLParagraphElement;

form.addEventListener("submit", async (event: Event) => {
    event.preventDefault(); // Prevent page reload

    const userText: string = input.value.trim();
    const endpoint: string = form.dataset.endpoint || ""; // Get the endpoint from the form

    if (userText && endpoint) {
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_input: userText }),
            });

            if (response.ok) {
                const result = await response.json();
                output.innerText = result.message || `Response: ${JSON.stringify(result)}`;
            } else {
                output.innerText = "Error: Failed to communicate with the server.";
            }
        } catch (err) {
            output.innerText = `Error: ${err}`;
        }
    } else {
        output.innerText = "Please enter valid input.";
    }
});
