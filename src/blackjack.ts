const gameState = document.getElementById("gameState") as HTMLParagraphElement;
const startBtn = document.getElementById("startBtn") as HTMLButtonElement;
const hitBtn = document.getElementById("hitBtn") as HTMLButtonElement;
const stayBtn = document.getElementById("stayBtn") as HTMLButtonElement;

async function startGame() {
    const response = await fetch("/blackjack/start");
    const data = await response.json();
    gameState.innerText = `New Game Started! 
    Your cards: ${data.user_cards.join(", ")} (Score: ${data.user_score}) 
    Dealer's cards: ${data.dealer_cards.join(", ")}`;
}

async function hit() {
    const response = await fetch("/blackjack/hit", { method: "POST" });
    const data = await response.json();
    gameState.innerText = `${data.message} 
    Your cards: ${data.user_cards.join(", ")} (Score: ${data.user_score}) 
    Dealer's cards: ${data.dealer_cards.join(", ")}`;
}

async function stay() {
    const response = await fetch("/blackjack/stay", { method: "POST" });
    const data = await response.json();
    console.log("Final Game State:", data);

    gameState.innerText = `
        ${data.message}
        Your cards: ${data.user_cards.join(", ")} (Score: ${data.user_score})
        Dealer's cards: ${data.dealer_cards.join(", ")} (Score: ${data.dealer_score})
        Fool's cards: ${data.fool_cards.join(", ")} (Score: ${data.fool_score})
    `;
}

startBtn.addEventListener("click", startGame);
hitBtn.addEventListener("click", hit);
stayBtn.addEventListener("click", stay);