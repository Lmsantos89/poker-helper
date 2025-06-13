// Poker Tournament Helper JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const pokerForm = document.getElementById('pokerForm');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSection = document.getElementById('loadingSection');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    // Results elements
    const strengthProgress = document.getElementById('strengthProgress');
    const strengthValue = document.getElementById('strengthValue');
    const recommendation = document.getElementById('recommendation');
    const additionalInfo = document.getElementById('additionalInfo');
    
    // Form elements
    const card1Rank = document.getElementById('card1Rank');
    const card1Suit = document.getElementById('card1Suit');
    const card2Rank = document.getElementById('card2Rank');
    const card2Suit = document.getElementById('card2Suit');
    const numPlayers = document.getElementById('numPlayers');
    
    // Community card elements
    const communityRanks = document.querySelectorAll('.community-rank');
    const communitySuits = document.querySelectorAll('.community-suit');
    
    // Form submission handler
    pokerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Hide previous results and errors
        resultsSection.classList.add('d-none');
        errorSection.classList.add('d-none');
        
        // Show loading indicator
        loadingSection.classList.remove('d-none');
        
        // Validate hole cards
        if (!card1Rank.value || !card1Suit.value || !card2Rank.value || !card2Suit.value) {
            showError('Please select both hole cards completely.');
            return;
        }
        
        // Get position
        const positionRadios = document.getElementsByName('position');
        let position = 'middle';
        for (const radio of positionRadios) {
            if (radio.checked) {
                position = radio.value;
                break;
            }
        }
        
        // Collect community cards
        const communityCards = [];
        for (let i = 0; i < communityRanks.length; i++) {
            const rank = communityRanks[i].value;
            const suit = communitySuits[i].value;
            
            if (rank && suit) {
                communityCards.push(rank + suit);
            } else if (rank || suit) {
                showError(`Community card ${i+1} is incomplete. Please select both rank and suit.`);
                return;
            }
        }
        
        // Validate community cards sequence
        if (communityCards.length > 0) {
            // First 3 should be flop
            if (communityCards.length >= 1 && communityCards.length < 3) {
                if (communityCards[0] && (!communityCards[1] || !communityCards[2])) {
                    showError('If any flop card is specified, all 3 flop cards must be specified.');
                    return;
                }
            }
            
            // If turn is specified (index 3), all flop cards must be specified
            if (communityCards.length >= 4 && (!communityCards[0] || !communityCards[1] || !communityCards[2])) {
                showError('If turn is specified, all flop cards must be specified.');
                return;
            }
            
            // If river is specified (index 4), turn and all flop cards must be specified
            if (communityCards.length === 5 && !communityCards[3]) {
                showError('If river is specified, turn and all flop cards must be specified.');
                return;
            }
        }
        
        // Prepare data for API call
        const data = {
            numPlayers: parseInt(numPlayers.value),
            card1: card1Rank.value + card1Suit.value,
            card2: card2Rank.value + card2Suit.value,
            communityCards: communityCards,
            position: position
        };
        
        // Add big blinds if provided
        const bigBlindsInput = document.getElementById('bigBlinds');
        if (bigBlindsInput && bigBlindsInput.value) {
            const bigBlinds = parseInt(bigBlindsInput.value);
            if (isNaN(bigBlinds) || bigBlinds <= 0) {
                showError('Big blinds must be a positive number');
                return;
            }
            data.bigBlinds = bigBlinds;
        }
        
        // Make API call
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred during calculation.');
                });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            loadingSection.classList.add('d-none');
            
            // Update results
            strengthProgress.style.width = `${data.handStrength}%`;
            strengthValue.textContent = `${data.handStrength}%`;
            
            recommendation.textContent = data.recommendation;
            
            // Set color based on recommendation
            if (data.recommendation === "Fold") {
                recommendation.style.color = "#e74c3c"; // Red
            } else if (data.recommendation === "Call") {
                recommendation.style.color = "#f39c12"; // Orange
            } else {
                recommendation.style.color = "#27ae60"; // Green
            }
            
            additionalInfo.textContent = data.info;
            
            // Show results section
            resultsSection.classList.remove('d-none');
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            showError(error.message);
        });
    });
    
    // Helper function to show error message
    function showError(message) {
        loadingSection.classList.add('d-none');
        errorMessage.textContent = message;
        errorSection.classList.remove('d-none');
    }
});
